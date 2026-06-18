# Project 1 — RAG for B2B SaaS Support

> An AI assistant that answers customer support questions for a B2B software product by retrieving from the product's documentation and resolved issues, **with citations**. Built to deflect repetitive support tickets without giving customers wrong answers.

**Status:** ✅ Working end-to-end (Week 2). Ask a question → grounded, cited answer over the Supabase docs, with escalation when the answer isn't in the corpus. Automated eval + retrieval tuning lands Week 3.

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

**1. Build the knowledge base** (clean → chunk → embed → persist the index):

```bash
python -m src.ingest            # full build (embeds + persists to storage/)
python -m src.ingest --stats    # local only: cleanup + chunk counts, no API calls
```

**2. Inspect retrieval** (which chunks come back for a query):

```bash
python -m src.retrieve "how do I enable row level security?"
```

**3. Ask a question** (grounded, cited answer; escalates if not in the corpus):

```bash
python -m src.generate "how do I enable row level security?"
```

**4. Run the golden-question eval pass:**

```bash
python -m src.run_golden        # writes evals/golden-run.md
```

### Example

```
$ python -m src.generate "How do I enable row level security on a table?"

Answer:
You can enable Row Level Security (RLS) on a table using:
    alter table "table_name" enable row level security;
Once enabled, no data is accessible until you create policies [1]. ...

Sources:
  [1] row-level-security.mdx  (score 0.689)
  ...
```

A question with no answer in the corpus (e.g. a billing/refund request) is **declined and escalated** rather than answered — see `evals/day5-findings.md`.

## Success metrics (what we'll measure)

- **Retrieval hit rate** — did the right chunk make it into top-k?
- **Answer faithfulness** — is the answer grounded in retrieved context (no hallucination)?
- **Answer correctness** — does it match the gold answer?
- **Deflection rate** — % of questions answerable without a human (the business metric).

## Roadmap

- **Project 1 (this repo):** RAG over docs + resolved issues, grounded answers with citations.
- **Project 2:** multi-step support *agent* (tool use, account lookup, escalation, guardrails).
- **Project 3:** production system (eval in CI, feedback loop, latency/cost dashboards).
