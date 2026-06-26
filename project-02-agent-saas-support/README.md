# Project 2 — B2B SaaS Support Agent

> An AI **agent** that handles a customer support ticket end-to-end: it understands the question, **looks up live information using tools**, and either resolves the question or escalates to a human. Where Project 1 *answered from documents*, this one *acts*.

**Status:** 🚧 Week 5 — agent design done, first tool built. The agent loop lands Day 3.

## Project 1 vs Project 2

| | Project 1 (RAG) | Project 2 (Agent) |
|---|---|---|
| Shape | a straight line: retrieve → generate | a **loop** the model drives |
| Does | answers from documents | fetches live state + acts via tools |
| Who picks the steps | you (fixed) | the model |

## The agent loop (planned)

```
user message
  → model decides: answer directly, OR call a tool
       → (tool call) our code runs the tool, returns the result
            → model continues with the result
                 → final answer, or another tool call …
```

## Tools

| Tool | What it does | Status |
|---|---|---|
| `get_account_status(account_id)` | Mock: returns plan, billing status, active incident | ✅ Day 2 |
| `search_docs(query)` | Reuse Project 1's retrieval as a tool | Week 6 |

See [`docs/agent-design.md`](docs/agent-design.md) for the full design (workflow, guardrails, "done" definition).

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
python -m src.tools     # Day 2: sanity-check the first tool (no model yet)
# python -m src.agent   # Day 3: the agent loop (coming)
```
