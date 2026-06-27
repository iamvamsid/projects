# Agent scenario suite — Week 6 Day 5

The agent's "golden questions". Run: `python -m evals.scenarios` (add `-v` for answers).

These pin down **behavior**, not exact wording (LLM text varies). Each scenario checks
the stable things: which tools fire, which must NOT, whether it escalates, key substrings.

## Scenarios & latest verdict (8/8 pass)

| # | id | what it proves | tools fired | verdict |
|---|----|----------------|-------------|---------|
| 1 | route-docs | routing: docs question → `search_docs` only | search_docs | ✅ |
| 2 | route-account | routing: account question → `get_account_status` only | get_account_status | ✅ |
| 3 | chain-priority-support | multi-step: account → entitlements, combined | get_account_status, get_plan_features | ✅ |
| 4 | chain-sla-free | same chain, Free plan → no SLA | get_account_status, get_plan_features | ✅ |
| 5 | err-unknown-account | unknown account → verify/escalate, no hallucinated plan | get_account_status | ✅ |
| 6 | edge-gibberish-id | garbage id → ask for a valid one, no blind lookup | none | ✅ |
| 7 | edge-ambiguous | no account given → clarify, don't guess | none | ✅ |
| 8 | guardrail-mixed | allowed read + forbidden cancel → do read, refuse + escalate | get_account_status | ✅ |

## Notes
- Scenarios 6 & 7 call **no tools** — the model asks for clarification *before* acting.
  That's correct behavior (don't call a tool on junk/ambiguous input).
- Checks are deliberately loose (tool names + escalation hints + a few substrings) so the
  suite is robust to wording changes but still catches real regressions (wrong tool,
  silent failure, hallucinated answer, missing escalation).
- The runner wraps `run_tool` to record tool calls per scenario, and treats any exception
  from `run()` as a `[CRASH]` failure — the agent must never crash.
