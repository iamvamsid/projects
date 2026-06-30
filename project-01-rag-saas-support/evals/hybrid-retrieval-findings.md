# Hybrid retrieval — findings (Week 9)

**Question:** does adding a BM25 keyword retriever (fused with the vector retriever via
Reciprocal Rank Fusion) beat pure vector retrieval on the golden set?

**Short answer:** not clearly. It improves coverage at k=3/5 but leaves **recall@5 —
the metric that actually feeds generation — unchanged**, and slightly hurts top-rank
precision (hit@1, MRR). On n=13 answerable questions, every ±7.7pp swing is one
question, i.e. within noise. Verdict: keep the implementation as an option; the real
bottleneck remains **corpus coverage** (Week-3 finding), not retrieval method.

## Method
- **Vector:** existing `retrieve()` — OpenAI `text-embedding-3-small`, cosine top-k.
- **BM25:** `rank_bm25.BM25Okapi` over the *same* chunks (from the index docstore).
- **Fusion:** Reciprocal Rank Fusion — `score = Σ 1/(rrf_k + rank)` over both lists.
  RRF uses only *rank*, so the incomparable cosine vs BM25 score scales never get mixed.
- Eval: same harness (`python -m src.eval --hybrid`), golden set, top_k=5, n=13 answerable.

## Results (golden set, n=13)

| config | hit@1 | hit@3 | hit@5 | **recall@5** | MRR |
|---|---|---|---|---|---|
| **vector (baseline)** | 53.8% | 69.2% | 76.9% | **73.1%** | 0.635 |
| hybrid, rrf_k=60 (textbook default) | 46.2% | 76.9% | 76.9% | 69.2% | 0.590 |
| **hybrid, rrf_k=10 (chosen)** | 46.2% | 76.9% | **84.6%** | **73.1%** | 0.605 |
| hybrid, pool10 rrf_k=10 | 46.2% | 69.2% | 76.9% | 69.2% | 0.579 |
| hybrid, rrf_k=10, vector-weighted 2:1 | 46.2% | 76.9% | 76.9% | 73.1% | 0.577 |

## What the numbers say
- **rrf_k matters a lot.** The textbook `rrf_k=60` is *worse* than baseline (it flattens
  ranks so a mediocre-in-both chunk beats an excellent-vector-only one). `rrf_k=10` fixes
  that and is the best-balanced config.
- **Coverage up, precision down.** hit@3 and hit@5 improve (+7.7pp each) — one more
  question gets a relevant page into the top results. But hit@1 and MRR drop — BM25
  occasionally promotes a keyword-y but less-relevant chunk into the very top slot.
- **recall@5 is unchanged (73.1% → 73.1%).** This is the metric that feeds the generator
  (the top-5 context), so the answer quality input is no better with hybrid.
- **n=13 is tiny.** ±7.7pp = one question. None of these deltas is significant.

## Decision
- Set `retrieve_hybrid` default to **rrf_k=10** (clearly better than 60).
- **Keep vector as the production default for generation** — recall@5 is tied and hybrid
  costs top-rank precision. Hybrid stays available (`--hybrid`) and documented.
- Reaffirms the Week-3 conclusion: the lever for *this* corpus is coverage (ingesting the
  topics the golden questions actually ask about), not the retrieval algorithm. A keyword
  retriever can't surface a page that was never indexed.

## What would change the verdict
- A larger, more diverse golden set (n≫13) to move deltas out of the noise band.
- A corpus with more exact-term queries (error codes, function names, CLI flags) where
  BM25's exact-match strength pays off more than on conceptual "how do I…" questions.
