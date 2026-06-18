# Golden Questions (eval seed)

> **Day 7 task — do this BEFORE writing RAG code.** Write 20–30 questions you'd want the system to answer correctly. This is your evaluation foundation: you cannot fix what you cannot measure.

For each question capture:
- **Q** — the question (phrased like a real support ticket).
- **Expected answer** — or the key facts the answer must contain.
- **Source** — where in the corpus the answer lives (doc page / issue #), if known.
- **Type** — `factual` (single doc) · `multi-doc` (needs ≥2 sources) · `should-escalate` (not answerable → system must say so, not guess).

Aim for a mix: mostly factual, several multi-doc, and a few should-escalate (these test that the system refuses to hallucinate).

---

| # | Q | Expected answer / key facts | Source | Type |
|---|---|------------------------------|--------|------|
| 1 | | | | factual |
| 2 | | | | factual |
| 3 | | | | multi-doc |
| 4 | | | | should-escalate |
| ... | | | | |

<!-- Tip: mine real questions straight from the product's GitHub Issues/Discussions — those come with real answers and make a partially-real eval set, which is stronger than fully synthetic. -->
