# Eval Results — retrieval

Tracks retrieval metrics across configs so we can show before/after. Run with
`python -m src.eval`. Scored over the 13 answerable golden questions.

## Baseline — Week 3 Day 2 (2026-06-18)
**Config:** chunk_size=512, chunk_overlap=50, embed=text-embedding-3-small, top_k=5.

| Metric | Score |
|---|---|
| hit-rate@1 | 53.8% (7/13) |
| hit-rate@3 | 69.2% (9/13) |
| hit-rate@5 | 76.9% (10/13) |
| MRR | 0.635 |

### Misses / weak (to diagnose Day 4)
- **Q2** (empty results → RLS): rank 4. Vocabulary gap — "empty results" doesn't sound like "row level security".
- **Q4** (anon vs service_role): MISS vs tag `roles.mdx`, but retrieved `signing-keys.mdx` repeatedly — **possible bad answer-key tag**, not a retrieval failure. VERIFY.
- **Q17** (OAuth + RLS, multi-doc): MISS — retrieved `token-security.mdx` only.
- **Q21** (SSR auth): MISS vs `server-side.mdx` — retrieved `sessions.mdx`/`advanced-guide.mdx` (possibly also relevant). VERIFY tag.
- **Q5** (upload): rank 2. **Q18** (storage+RLS): rank 2.

### Notes
- Multi-doc questions (Q17, Q18, Q21) are hardest — they need ≥2 docs and the query is broad.
- Before tuning, verify the questionable answer-key tags (Q4, Q21) — some "misses" may be tagging errors, not retrieval errors.

## Generation eval — Day 3 baseline vs Day 4 (after fixes)
Judge = claude-sonnet-4-6; system = claude-opus-4-8.

| Metric | Day 3 (baseline) | Day 4 (after fixes) | Note |
|---|---|---|---|
| Correctness (answerable, n=13) | 73% | 80.8% | + run variance |
| Faithfulness grounded (n=13) | 38.5% | no violations found | 38.5% was a JUDGE TRUNCATION BUG (`context[:4000]` → `[:16000]`) |
| Critical escalation (account/destructive: Q22-25) | 3/4 (Q23 failed) | **4/4** | Q23 safety guardrail added to system prompt |
| Out-of-corpus "escalation" (Q7-11,15,19,20) | ~2/8 | ~2/8 | LABEL DISAGREEMENT — judge thinks answering from adjacent docs is fine. Open design decision, not a bug. |

**Fixes applied (Day 4):**
1. `eval.py` judge context truncation 4000 → 16000 chars (faithfulness was under-measured).
2. `generate.py` SYSTEM prompt: added safety guardrails (decline destructive / account-action / billing requests regardless of retrieved context). Verified Q23 now declines.

**Honest caveats:** report faithfulness as "no violations found (n=13)", not "100%" — small sample. Don't average critical + ambiguous escalation into one number; they mean different things.

## RETRIEVAL tuning experiment — Day 5
Same golden set, one knob at a time (`src/experiment.py`).

| Config | hit@1 | hit@3 | hit@5 | recall@5 | MRR |
|---|---|---|---|---|---|
| chunk=256 | 38.5% | 69.2% | 69.2% | 65.4% | 0.513 |
| **chunk=512 (baseline)** | 53.8% | 69.2% | 76.9% | 73.1% | 0.631 |
| chunk=1024 | 61.5% | 69.2% | 76.9% | 73.1% | 0.669 |
| chunk=512, top_k=10 | 53.8% | 69.2% | 76.9% | 73.1% | 0.639 |

**Decision: keep chunk=512. Do NOT adopt 1024.** Reasoning:
- 1024 improved hit@1 (54%→62%) and MRR, BUT **recall@5 and hit@5 are identical** to 512. The generator consumes the top-5, so 1024 hands the model the *same docs* — it only reshuffled ranking. No end-to-end answer-quality gain.
- 1024 = bigger chunks = more tokens/query = higher cost + more noise. Paying for a vanity metric.
- 256 is clearly worse (too fragmented) — matches theory.
- top_k=10 added nothing — the misses aren't "just outside top-5", they're absent entirely.

**Real conclusion — chunk size is the wrong lever.** The bottleneck is the ~23% of
questions whose expected doc never reaches top-5 (Q4, Q17, Q21). Next levers (Week 4+):
1. **Verify tags** — Q4 retrieved `signing-keys.mdx` (may be the *correct* source; `roles.mdx` tag may be wrong); Q21 tag may be too strict.
2. **Hybrid retrieval** (keyword + vector) for semantic misses (Q2 "empty results"→RLS, Q17 broad multi-doc) where vocabulary differs from the docs.
3. **Parent-document retrieval** to keep small-chunk precision + big-chunk context.

**Headline (honest):** measured 4 retrieval configs; found chunk-size tuning moves @1 but not recall@5 (what feeds generation); identified recall@5 and tag quality as the true bottlenecks, and hybrid retrieval as the next experiment.
**Config:** _tbd_

| Metric | Baseline | Tuned | Δ |
|---|---|---|---|
| hit-rate@1 | 53.8% | | |
| hit-rate@3 | 69.2% | | |
| hit-rate@5 | 76.9% | | |
| MRR | 0.635 | | |
