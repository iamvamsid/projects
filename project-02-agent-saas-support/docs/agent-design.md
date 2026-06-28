# Agent Design — B2B SaaS Support Agent (Project 2)

**Status:** Week 6 — shipped. Blueprint below; see "Week 6 — what actually shipped" at the
bottom for how reality diverged (notably: a third tool, `get_plan_features`).

## The job
A **customer support agent** for a B2B SaaS product that handles a ticket end-to-end:
understand the question → look up whatever live information it needs (via tools) →
either resolve the question or escalate to a human.

Difference from Project 1: Project 1 *answered from documents* (a straight line:
retrieve → generate). Project 2 *fetches live state and acts* — the model drives a
**loop**, choosing tools until it can finish.

## The agent loop (the core concept)
```
user message
  -> model decides: answer directly, OR call a tool
       -> (tool call) our code runs the tool, returns the result
            -> model continues with the result
                 -> final answer, or another tool call ...
```

## Build approach — learn all three, in order
We will implement the SAME agent three ways, increasing abstraction each time, to
understand what each layer hides:
1. **Manual loop (raw Anthropic SDK)** — Week 5. Write the loop by hand: send tools,
   detect `stop_reason == "tool_use"`, run the tool, send the `tool_result` back, repeat
   until `end_turn`. Maximum understanding.
2. **SDK tool runner** (`@beta_tool` + `tool_runner`) — rebuild the same agent letting the
   SDK run the loop. See how much it collapses.
3. **Agent framework** — the most abstracted version, for comparison.

## Tool surface
**Week 5 — ONE tool (happy path):**
- `get_account_status(account_id)` — mock. Returns canned data: plan tier, billing
  status, whether there's an active incident. Chosen first because looking up *live state
  the model cannot know* is the clearest demonstration of the agent concept.

**Week 6 — add more tools:**
- `search_docs(query)` — reuse Project 1's retrieval as a tool (ties the two projects
  together).
- maybe `lookup_order(order_id)`, `create_escalation(...)`.

### Tool definition sketch (Week 5)
```
name: get_account_status
description: Look up a customer's account status (plan, billing state, active incidents)
             by account id. Use when the question depends on the customer's specific
             account, not on general documentation.
input: { account_id: string (required) }
output: { plan, billing_status, active_incident }   # mock/canned
```

## Guardrails (from day one)
- **Read, don't act.** The agent may *look up* status but must NOT take destructive or
  billing actions (refunds, plan changes, deletions). Those require a human.
- **Escalate when unsure** or when the request needs a real account change — reuse the
  safety instinct from Project 1's destructive-request fix.
- The agent explains; it does not perform irreversible operations on the customer's behalf.

## "Done" definition
The agent is finished when it has either (a) answered the customer's question using the
information it looked up, or (b) escalated to a human with a clear reason. No silent
dead-ends.

## Week 5 happy-path scenarios to test
1. **Needs the tool:** "Is my account (acct_123) on a plan that includes priority support?"
   → agent calls `get_account_status` → answers from the result.
2. **No tool needed:** "What does 'priority support' generally mean?" → answers directly
   (or, once search_docs exists, uses that) — should NOT call the account tool.
3. **Should escalate:** "Please downgrade my plan to Free." → declines the *action*,
   escalates.

## Out of scope (Week 5)
Multiple tools, error recovery when a tool fails, memory across turns, observability —
all Week 6–7.

---

## Week 6 — what actually shipped
All three build styles done in Week 5 (`agent.py` manual, `agent_toolrunner.py`,
`agent_framework.py`). Week 6 built on the manual loop:

**Tools — ended with THREE, not two.** The planned `search_docs` exposed a gap: the agent
knew the *plan name* (from `get_account_status`) and *features* (from docs), but no source
**joined** them. Searching product docs for "what does Pro include" returned junk, and the
agent (correctly) escalated instead of guessing. Fix: added `get_plan_features(plan)` — an
**entitlements** source (support level, priority support, SLA, seats, SSO). "What a plan
includes" is entitlements data, not product docs. `lookup_order` / `create_escalation` were
*not* needed and dropped.

**Multi-step / chaining.** "Does my plan acct_123 include priority support?" chains
`get_account_status` → `get_plan_features` (dependency order — can't ask what Pro includes
until you learn the plan is Pro). Independent lookups (account + docs) fire in parallel.

**Error recovery.** `run_tool` never raises — unknown tool, bad/missing args (TypeError),
unknown plan, and in-tool exceptions all return helpful error dicts (echo input / list valid
options). The loop tags any error result `is_error: true` so the model adapts.

**Hardening.** Loop guard (repeated identical call → escalate) + max-steps fallback, both
returning a customer-facing escalation message, never a developer string. Edge cases proven:
gibberish id → ask for a valid one; ambiguous question → clarify; lookup + forbidden action →
do the read, refuse + escalate the action *in the same turn*.

**Proof.** `evals/scenarios.py` — 8 scenarios (routing, chaining, failure modes), 8/8 pass;
any exception from the loop is a crash-fail.

---

## Week 7 — memory + observability
Week 6 made the agent robust; Week 7 makes it operable.

**Memory (`src/conversation.py`).** A `Conversation` owns the `messages` list across turns
(vs `run()`, which starts fresh each call), so follow-ups resolve without re-asking. The
assistant's final answer is appended to history (so the next turn remembers it), and the
loop guard resets per-turn (re-calling a tool in a later turn is legitimate). Bounded by
`max_turns` (default 6): `_trim()` keeps the most recent N **customer** turns and cuts ONLY
at a customer-turn boundary — never between a `tool_use` and its `tool_result`, which would
orphan the result and make the API reject the history. Verified by a deterministic
`_valid_pairing()` check plus a live continuity test (guardrail + routing hold mid-conversation).

**Observability (`src/trace.py`, `src/trace_view.py`).** `run(..., collect_trace=True)` builds a
structured `Trace`: ordered steps (model `stop_reason`, input/output tokens from the API `usage`
field, latency) and per-step tool calls (name, input, result, `is_error`, latency), plus the
`outcome`. Tokens → **$ cost** via `PRICES_PER_MTOK` (opus-4-8 $5/$25 per MTok). One run → one
JSON under `traces/` (gitignored — run artifacts). `trace_view` renders the timeline + the
operational summary (steps · tools · tokens · cost · latency). The scenario suite emits traces
with `--trace`. Tracing is opt-in, so default behavior and the 8/8 suite are unaffected.

**Trace format (one run):**
```
Trace { user_input, model, started_at, outcome, total_latency_ms,
        steps: [ Step { n, stop_reason, input_tokens, output_tokens, model_latency_ms,
                        tool_calls: [ ToolCall { name, input, result, is_error, latency_ms } ] } ],
        final_text }
  + roll-ups: total_input_tokens, total_output_tokens, total_cost_usd, tools_used
```
