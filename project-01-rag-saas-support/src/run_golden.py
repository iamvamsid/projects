"""Day 5 — run every golden question through the pipeline and save results.

Parses evals/golden-questions.md, runs each question through generate.answer(),
records the answer + sources + top retrieval score, and writes a review file
to evals/golden-run.md. This is a manual smell-test, not automated scoring
(that's Week 3).

Run:  python -m src.run_golden
"""

from datetime import date
from pathlib import Path

from src.generate import answer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_FILE = PROJECT_ROOT / "evals" / "golden-questions.md"
OUTPUT_FILE = PROJECT_ROOT / "evals" / "golden-run.md"


def parse_questions(md_path: Path):
    """Pull (number, question, type) from the markdown tables."""
    rows = []
    for line in md_path.read_text().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or not cells[0].isdigit():
            continue  # skip headers, separators, template placeholder rows
        num, question, qtype = cells[0], cells[1], cells[-1]
        if not question or question.startswith("_"):
            continue  # skip empty/placeholder questions
        rows.append((num, question, qtype))
    return rows


def main() -> None:
    questions = parse_questions(QUESTIONS_FILE)
    print(f"Running {len(questions)} golden questions...\n")

    out = [f"# Golden-question run — {date.today()}\n",
           f"Ran {len(questions)} questions through `generate.answer()`. "
           "Eyeball each: correct? grounded? cited? did escalation cases decline?\n"]

    for num, question, qtype in questions:
        print(f"[{num}] ({qtype}) {question[:70]}...")
        text, sources = answer(question)
        top_score = sources[0][2] if sources else 0.0

        out.append(f"\n---\n\n## Q{num} — `{qtype}`")
        out.append(f"**Question:** {question}\n")
        out.append(f"**Top retrieval score:** {top_score:.3f}  "
                   f"_(low score on a `should-escalate` = good; low score on a "
                   f"`factual` = retrieval miss)_\n")
        out.append(f"**Answer:**\n\n{text}\n")
        out.append("**Sources:** " + ", ".join(f"{s[1]} ({s[2]:.2f})" for s in sources))
        out.append("\n**My verdict:** _[ ] correct  [ ] partial  [ ] wrong — notes:_\n")

    OUTPUT_FILE.write_text("\n".join(out))
    print(f"\n✅ Wrote results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
