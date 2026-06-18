# Project 1 — RAG for B2B SaaS Support

> An AI assistant that answers customer support questions for a B2B software product by retrieving from the product's documentation and resolved issues, **with citations**. Built to deflect repetitive support tickets without giving customers wrong answers.

**Status:** 🚧 Week 1 — scaffold only. Retrieval/generation logic lands Week 2; eval harness Week 3.

---

## The problem

Every B2B SaaS company's support team scales linearly with its customer base. Most incoming questions are already answered somewhere in the docs or in past resolved tickets — but customers don't find those answers, so engineers burn time on repeat Tier-1 questions. The goal: **deflect the repetitive questions accurately**, with visible citations so trust is preserved.

See the customer-facing framing in [`docs/one-pager.md`](docs/one-pager.md).

## Domain & data

- **Domain anchor:** Customer Support / Internal Knowledge — flavor **B2B SaaS support**.
- **Knowledge base (corpus):** public documentation of an OSS-friendly B2B SaaS product (default: **Supabase**; alternatives: Prisma, Postgres, Twilio).
- **Eval questions:** a mix of (a) *real* Q→resolution pairs mined from the product's public GitHub Issues/Discussions, and (b) *synthetic* tickets generated with Claude against the KB, each with a gold answer + source chunk.

All sources are public — no NDA/data-access constraints.

## Architecture (planned)

```
ingest.py    →  crawl/clean docs → chunk → embed → vector store
retrieve.py  →  query → top-k relevant chunks
generate.py  →  Claude answers, grounded in retrieved chunks, WITH citations
eval.py      →  score retrieval (hit rate) + answer (faithfulness, correctness)
```

| Module | Responsibility | Lands |
|---|---|---|
| `src/ingest.py` | Build the knowledge base (chunk + embed + store) | Week 2 |
| `src/retrieve.py` | Retrieve relevant chunks for a query | Week 2 |
| `src/generate.py` | Grounded answer generation with citations | Week 2 |
| `src/eval.py` | Evaluation harness | Week 3 |

## Tech

- Python 3.11+
- `anthropic` (Claude — default model `claude-opus-4-8`)
- `openai` (embeddings / comparison)
- No RAG framework for now — vanilla SDKs, to learn the internals. (Reassess in Week 2.)

## Setup

```bash
cd project-01-rag-saas-support
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your API keys
```

## Usage

_Placeholder — wired up in Week 2._

```bash
python -m src.ingest      # build the knowledge base
python -m src.generate    # ask a question
python -m src.eval        # run the eval harness
```

## Success metrics (what we'll measure)

- **Retrieval hit rate** — did the right chunk make it into top-k?
- **Answer faithfulness** — is the answer grounded in retrieved context (no hallucination)?
- **Answer correctness** — does it match the gold answer?
- **Deflection rate** — % of questions answerable without a human (the business metric).

## Roadmap

- **Project 1 (this repo):** RAG over docs + resolved issues, grounded answers with citations.
- **Project 2:** multi-step support *agent* (tool use, account lookup, escalation, guardrails).
- **Project 3:** production system (eval in CI, feedback loop, latency/cost dashboards).
