# Project 2 — B2B SaaS Support Agent

> An AI **agent** that handles a customer support ticket end-to-end: it understands the question, **looks up live information using tools**, and either resolves the question or escalates to a human. Where Project 1 *answered from documents*, this one *acts*.

**Status:** ✅ Week 6 — multi-tool agent working: 3 tools, multi-step chaining, graceful error recovery, 8/8 scenario suite passing.

## Project 1 vs Project 2

| | Project 1 (RAG) | Project 2 (Agent) |
|---|---|---|
| Shape | a straight line: retrieve → generate | a **loop** the model drives |
| Does | answers from documents | fetches live state + acts via tools |
| Who picks the steps | you (fixed) | the model |

## The agent loop

```
user message
  → model decides: answer directly, OR call a tool
       → (tool call) our code runs the tool, returns the result (tagged is_error on failure)
            → model continues with the result
                 → final answer, or another tool call …
```

The model decides **how many** tools to call and **in what order**. Independent lookups
fire in parallel; dependent ones chain (e.g. find the plan, *then* look up what it includes).

## Tools

| Tool | What it does | Source |
|---|---|---|
| `get_account_status(account_id)` | Account state: plan, billing status, active incident | mock dict |
| `search_docs(query)` | Product-docs Q&A — **reuses Project 1's persisted vector index** | Project 1 RAG |
| `get_plan_features(plan)` | Entitlements: support level, priority support, SLA, seats, SSO | mock dict |

> **Why three sources, not two:** account state knows the *plan name* and docs know *features*,
> but neither maps plan → features. "What does my plan include" is **entitlements** data — in
> production it lives in a billing/entitlements service, not the product docs. `get_plan_features`
> is that source, and answering "does my plan include X?" **chains** account → entitlements.

## Multi-step, chaining, and error recovery (Week 6)

- **Routing** — with multiple tools, the model picks the right *one* (docs vs account vs entitlements).
- **Chaining** — one question can need several tools in dependency order; the loop feeds each
  result back until the model is done.
- **Error recovery** — `run_tool` never raises (unknown tool, bad args, in-tool exception all
  return error dicts); the loop tags failures `is_error: true` so the model adapts —
  clarifies, tries another tool, or escalates. Never crashes, never invents data.
- **Hardening** — a loop guard (repeated identical call → escalate) and a max-steps fallback,
  both surfacing a polite customer-facing escalation rather than a developer string.

See [`docs/agent-design.md`](docs/agent-design.md) for the full design and
[`evals/scenarios.md`](evals/scenarios.md) for the scenario suite (8/8 passing).

## Memory + observability (Week 7)

- **Multi-turn memory** — `src/conversation.py`. A `Conversation` owns the `messages`
  list across turns, so follow-ups resolve without re-asking ("what plan am I on?" → "Pro"
  → "does *it* include SSO?"). Bounded by `max_turns` (default 6); trimming cuts only at
  customer-turn boundaries so a `tool_use`/`tool_result` pair is never orphaned.
- **Structured traces** — `src/trace.py`. `run(..., collect_trace=True)` records, per step:
  model call (stop_reason, tokens from the API `usage` field, latency) and each tool call
  (name, input, result, `is_error`, latency), plus the outcome. One run → one JSON in
  `traces/` (gitignored). Roll-ups: total tokens, **$ cost** (per-model rates in
  `PRICES_PER_MTOK`), latency, tools used.
- **Trace viewer** — `python -m src.trace_view` (newest), `<file>`, or `--last N`.
  Renders the timeline + the operational summary (steps · tools · tokens · cost · latency).
- The scenario suite can emit traces: `python -m evals.scenarios --trace` adds a per-scenario
  cost/latency table (one full suite run ≈ $0.15).

## Build approach
We implement the **same agent three ways**, increasing abstraction each time, to learn what each layer hides:
1. **Manual loop (raw Anthropic SDK)** — Week 5 (you write the loop by hand).
2. **SDK tool runner** — then let the SDK run the loop.
3. **Agent framework** — for comparison.

## Guardrails
The agent may **read** account status but never take destructive or billing **actions** (refunds, plan changes, deletions) — those escalate to a human.

## Setup
```bash
cd project-02-agent-saas-support
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your ANTHROPIC_API_KEY
```

## Usage
```bash
python -m src.tools                                   # sanity-check tools (no model)
python -m src.agent "How do I enable row level security?"   # routing → search_docs
python -m src.agent "Does my plan acct_123 include priority support?"  # chaining
python -m src.agent "What plan is acct_999 on?"       # error recovery → escalate
python -m src.conversation                            # multi-turn memory demo (Week 7)
python -m evals.scenarios                             # the 8-scenario suite (-v answers, --trace cost)
python -m src.trace_view                              # view the newest trace (--last N to list)
```

The same agent is also built two more ways for comparison — `src/agent_toolrunner.py`
(SDK tool runner) and `src/agent_framework.py` (LlamaIndex `FunctionAgent`).
