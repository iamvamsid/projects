"""Hybrid retrieval (Week 9) — vector + BM25 keyword, fused with Reciprocal Rank Fusion.

Vector search finds *semantic* matches (meaning), but can miss exact terms the
embedding smooths over — error codes, function names, rare keywords like "RLS" or
"pgbouncer". BM25 is the opposite: it nails exact-term matches but is blind to
paraphrase. Hybrid retrieval runs both and merges their ranked lists.

We fuse with **Reciprocal Rank Fusion (RRF)** rather than mixing raw scores: vector
cosine similarity and BM25 scores live on different scales and aren't comparable, so
adding them is meaningless. RRF only uses each document's *rank* in each list —
score = sum over retrievers of 1 / (rrf_k + rank) — so no calibration is needed.

Returns the same NodeWithScore shape as src.retrieve.retrieve(), so the eval harness
works unchanged (drop-in: just swap the function).

Run:  python -m src.retrieve_hybrid "how do I enable row level security?"
"""

import re
import sys
from functools import lru_cache

from llama_index.core.schema import NodeWithScore
from rank_bm25 import BM25Okapi

from src.retrieve import get_index, retrieve as vector_retrieve

_TOKEN = re.compile(r"[A-Za-z0-9_]+")


def _tok(text: str) -> list[str]:
    """Simple word/identifier tokenizer (keeps things like get_account_status, rls)."""
    return [t.lower() for t in _TOKEN.findall(text)]


@lru_cache(maxsize=1)
def _bm25():
    """Build the BM25 index once over the SAME chunks the vector index holds."""
    docs = list(get_index().docstore.docs.values())
    corpus = [_tok(n.get_content()) for n in docs]
    return BM25Okapi(corpus), docs


def _bm25_top(query: str, pool: int):
    bm25, docs = _bm25()
    scores = bm25.get_scores(_tok(query))
    order = sorted(range(len(docs)), key=lambda i: scores[i], reverse=True)[:pool]
    return [docs[i] for i in order]


def retrieve_hybrid(query: str, k: int = 5, pool: int = 20, rrf_k: int = 10):
    """Vector + BM25, fused via RRF. Returns top-k NodeWithScore (same shape as retrieve).

    rrf_k=10 (not the textbook 60): with a 20-doc pool, a large rrf_k flattens the
    rank curve so much that a mediocre-but-in-both-lists chunk outranks an
    excellent-vector-only chunk. rrf_k=10 lets top ranks dominate — measured best on
    the golden set (see evals/hybrid-retrieval-findings.md). Even so, the gain over
    pure vector is marginal/within-noise on this corpus.
    """
    vec_nodes = [nw.node for nw in vector_retrieve(query, k=pool)]
    bm_nodes = _bm25_top(query, pool)

    fused: dict[str, float] = {}
    by_id: dict[str, object] = {}
    for ranked in (vec_nodes, bm_nodes):
        for rank, node in enumerate(ranked):
            fused[node.node_id] = fused.get(node.node_id, 0.0) + 1.0 / (rrf_k + rank + 1)
            by_id[node.node_id] = node

    top = sorted(fused, key=fused.get, reverse=True)[:k]
    return [NodeWithScore(node=by_id[nid], score=fused[nid]) for nid in top]


def main() -> None:
    query = " ".join(sys.argv[1:]) or "How do I enable row level security on a table?"
    print(f"Q: {query}  (hybrid: vector + BM25 + RRF)\n")
    for n in retrieve_hybrid(query):
        snippet = n.node.get_content()[:160].replace("\n", " ")
        print(f"[rrf {n.score:.4f}] {n.node.metadata.get('file_name')}")
        print(f"    {snippet} ...\n")


if __name__ == "__main__":
    main()
