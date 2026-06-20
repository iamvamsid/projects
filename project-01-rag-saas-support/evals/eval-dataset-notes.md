# Eval dataset — scope decision & the corpus-coverage finding (Week 3, Day 1)

**Canonical dataset:** `evals/golden_set.json` (machine-readable; what `eval.py` consumes).
`evals/golden-questions.md` is the human-readable origin; `golden_set.json` is the source of truth for scoring.

## The finding (Day 1)
While tagging each question with its **expected source file** (ground truth for retrieval), grepping the corpus revealed that **the corpus only covers `auth/`, `database/`, `storage/`** — but several golden questions ask about **topics not in the corpus**: Realtime, Edge Functions, and the JS-client API reference.

So the Week-2 "retrieval gaps" (Q9 pagination etc.) were **not** retrieval-tuning problems — the answers simply **aren't in the knowledge base**. This is a **corpus-coverage** issue, a different diagnosis with a different fix. Conflating "the info isn't there" with "retrieval is bad" is exactly the trap good evaluation prevents.

> **FDE lesson:** the #1 cause of "the AI gave a bad answer" in real deployments is a mismatch between what users ask and what the knowledge base actually contains. Eval surfaces it.

## The decision
**Scope the golden set to the corpus.** Keep the corpus as-is (auth/database/storage) and **reclassify out-of-corpus questions as `should-escalate`** — the system *should* say "I don't have that information." This:
- keeps retrieval metrics clean (only measure questions the corpus can answer),
- turns the gap into a robust test of the escalation guardrail (12 escalation cases).

## Final composition (25 questions)
| Bucket | IDs | Count |
|---|---|---|
| Factual (in-corpus, has expected source) | 1,2,3,4,5,6,12,13,14,16 | 10 |
| Multi-doc (in-corpus) | 17,18,21 | 3 |
| should-escalate (reclassified, out-of-corpus) | 7,8,9,10,11,15,19,20 | 8 |
| should-escalate (original) | 22,23,24,25 | 4 |

**Answerable (retrieval-scored): 13 · Escalation-tested: 12.**

## To verify (low-confidence tags)
- Q3 (signup) and Q12 (password reset) → tagged `passwords.mdx` by best inference; confirm against the file.
- Spot-check that the multi-doc expected sources are the *best* pair, not just *a* plausible pair.
