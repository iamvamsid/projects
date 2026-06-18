# Day 5 — Golden-question pass: findings

**Date:** 2026-06-18
**What:** Ran all 25 golden questions through `generate.answer()` (see `golden-run.md` for full answers). This is a manual smell-test, not automated scoring (that's Week 3).

## Headline
The system works end-to-end: grounded, cited answers on most questions, and a **perfect escalation record**. A handful of factual questions expose **retrieval gaps** worth fixing.

## What works
- **Escalation guardrail: 4/4.** All `should-escalate` questions (Q22–25) declined and recommended a human; retrieval scores 0.30–0.45 (correctly low — nothing relevant found).
- **Strong factual answers:** RLS (Q1, 0.685), Storage upload (Q5, 0.714), DB connection (Q13, 0.669), Edge Function secrets (Q15), anon vs service_role (Q4) — all accurate, idiomatic, cited.

## Weaknesses (Week 3 fuel)
Low retrieval score → weaker/hedged answer. Candidates:
| Q | Topic | Top score | Issue |
|---|---|---|---|
| 9 | Pagination | 0.333 | Answered with SQL `LIMIT/OFFSET` + hedged; expected the JS client `.range()`. Retrieval surfaced the wrong passage. |
| 2 | Empty results (RLS gotcha) | 0.354 | Low score — check whether the "RLS with no policy returns 0 rows" gotcha was actually retrieved. |
| 8 | Filtering rows | 0.368 | Low score — likely didn't surface the JS client `.eq()` filter docs. |

**Hypothesis:** "how do I (client task)" questions retrieve poorly — the concept exists in the corpus but chunking/embedding isn't surfacing the JS-SDK passages. Likely levers: chunk size, query rephrasing, or a hybrid keyword+vector retriever. This is exactly what Week 3 eval + tuning addresses.

## Meta-lesson
The first analysis script had a bug — it scanned each whole result block (which contained my own annotation text with the word "escalate") instead of just the answer, so it reported "escalated = True" for all 25. **Eval tooling needs validating as much as the system under test.** Good interview anecdote.

## To do (carry-over)
- [ ] Read `golden-run.md` in full and fill the per-question verdict checkboxes (human eyeball — the real Day-5 task).
- [ ] Verify the low-score factual answers (Q2/Q8/Q9) against live docs — are they wrong, or just less idiomatic?
- [ ] Week 3: build automated scoring (retrieval hit-rate + faithfulness/correctness) and tune retrieval on these weak spots.
