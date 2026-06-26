# Agent Design — B2B SaaS Support Agent (Project 2)

**Status:** Week 5 Day 1 — design. No code yet. This is the blueprint.

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

## Out of scope this week
Multiple tools, error recovery when a tool fails, memory across turns, observability —
all Week 6–7.
