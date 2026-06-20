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

## After tuning — (Day 5, to fill)
**Config:** _tbd_

| Metric | Baseline | Tuned | Δ |
|---|---|---|---|
| hit-rate@1 | 53.8% | | |
| hit-rate@3 | 69.2% | | |
| hit-rate@5 | 76.9% | | |
| MRR | 0.635 | | |
