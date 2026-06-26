"""Evaluation harness.

Two graders, run separately (you can't fix what you can't isolate):

  RETRIEVAL  (default, cheap, deterministic):
      did the expected source file(s) appear in the top-k?
      -> hit-rate@k (>=1 expected found) and recall@k (fraction of expected found) + MRR
      Run:  python -m src.eval

  GENERATION (--gen, costs API calls):
      LLM-as-judge on the actual answers.
      answerable -> correctness (matches gold facts?) + faithfulness (grounded?)
      should-escalate -> did it correctly decline/escalate?
      Run:  python -m src.eval --gen
"""

import json
import re
import sys
from pathlib import Path

from anthropic import Anthropic

from src.retrieve import retrieve
from src.generate import SYSTEM, MODEL, _format_context

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GOLD_FILE = PROJECT_ROOT / "evals" / "golden_set.json"
GEN_OUT = PROJECT_ROOT / "evals" / "generation-eval.md"

TOP_K = 5
JUDGE_MODEL = "claude-sonnet-4-6"  # the grader; cheaper/faster than the system-under-test (Opus)


def load_all():
    return json.loads(GOLD_FILE.read_text())


def load_answerable():
    return [d for d in load_all() if d.get("expected_sources")]


# ============================================================ RETRIEVAL
def evaluate_retrieval():
    items = load_answerable()
    hits = {1: 0, 3: 0, 5: 0}
    recall = {1: 0.0, 3: 0.0, 5: 0.0}
    rr_sum = 0.0

    print(f"Retrieval eval over {len(items)} answerable questions (top_k={TOP_K})\n")
    print(f"{'Q':>3}  {'rank':>5}  {'recall@5':>9}  expected")
    print("-" * 70)

    for d in items:
        nodes = retrieve(d["question"], k=TOP_K)
        retrieved = [n.node.metadata.get("file_name") for n in nodes]
        expected = set(d["expected_sources"])

        # rank of the FIRST expected file found (for hit-rate / MRR)
        rank = next((i + 1 for i, f in enumerate(retrieved) if f in expected), None)
        rr_sum += (1.0 / rank) if rank else 0.0

        for k in (1, 3, 5):
            topk = set(retrieved[:k])
            found = expected & topk
            if found:
                hits[k] += 1
            recall[k] += len(found) / len(expected)   # fraction of needed pages found

        mark = f"@{rank}" if rank else "MISS"
        r5 = len(expected & set(retrieved[:5])) / len(expected)
        print(f"{d['id']:>3}  {mark:>5}  {r5:>9.2f}  {', '.join(sorted(expected))}")

    n = len(items)
    print("\n" + "=" * 46)
    print("RETRIEVAL METRICS")
    print("=" * 46)
    print(f"{'k':>3}  {'hit-rate@k':>12}  {'recall@k':>10}")
    for k in (1, 3, 5):
        print(f"{k:>3}  {hits[k]/n:>11.1%}  {recall[k]/n:>9.1%}")
    print(f"\nMRR: {rr_sum/n:.3f}")
    print("\nhit-rate@k = at least ONE expected page in top k")
    print("recall@k   = FRACTION of expected pages in top k (honest on multi-source)")


# ============================================================ GENERATION
def _system_answer(question):
    """Reproduce what generate.py does, but also return the context for the judge."""
    nodes = retrieve(question, k=TOP_K)
    context, sources = _format_context(nodes)
    client = Anthropic()
    msg = client.messages.create(
        model=MODEL, max_tokens=1024, system=SYSTEM,
        messages=[{"role": "user", "content":
                   f"Context passages:\n\n{context}\n\nQuestion: {question}\n\n"
                   "Answer using only the context above, citing sources as [n]. "
                   "If the context doesn't contain the answer, say so and recommend escalation."}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text")
    return text, context


def _judge(prompt):
    client = Anthropic()
    msg = client.messages.create(
        model=JUDGE_MODEL, max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = "".join(b.text for b in msg.content if b.type == "text")
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    return json.loads(m.group(0))


def _judge_answerable(q, gold, context, answer):
    prompt = (
        "You are grading a support assistant. Respond with ONLY a JSON object.\n\n"
        f"QUESTION:\n{q}\n\n"
        f"GOLD ANSWER (the key facts a correct answer must contain):\n{gold}\n\n"
        f"RETRIEVED CONTEXT the assistant was given:\n{context[:16000]}\n\n"
        f"ASSISTANT ANSWER:\n{answer}\n\n"
        "Grade:\n"
        '- "correctness": "correct" | "partial" | "wrong" '
        "(does the answer convey the gold key facts?)\n"
        '- "faithfulness": "grounded" | "unsupported" '
        "(is every claim supported by the retrieved context, with no invented details?)\n"
        '- "reason": one short sentence.\n'
        "JSON:"
    )
    return _judge(prompt)


def _judge_escalate(q, answer):
    prompt = (
        "A support assistant SHOULD decline and escalate to a human for the request "
        "below, because it is outside the product documentation (account/billing/"
        "destructive/out-of-scope). Respond with ONLY a JSON object.\n\n"
        f"QUESTION:\n{q}\n\n"
        f"ASSISTANT ANSWER:\n{answer}\n\n"
        '- "escalated": true | false '
        "(did it correctly decline / recommend a human, rather than fabricate an answer?)\n"
        '- "reason": one short sentence.\n'
        "JSON:"
    )
    return _judge(prompt)


def evaluate_generation():
    data = load_all()
    score = {"correct": 1.0, "partial": 0.5, "wrong": 0.0}
    corr_sum = faith_ok = n_ans = 0.0
    esc_ok = n_esc = 0
    out = [f"# Generation eval (LLM-as-judge: {JUDGE_MODEL})\n"]

    print(f"Generation eval — answering with {MODEL}, judging with {JUDGE_MODEL}")
    print("(this makes API calls for every question; be patient)\n")

    for d in data:
        ans, context = _system_answer(d["question"])
        if d.get("expected_sources"):  # answerable
            v = _judge_answerable(d["question"], d["gold"], context, ans)
            corr_sum += score.get(v.get("correctness"), 0)
            faith_ok += v.get("faithfulness") == "grounded"
            n_ans += 1
            print(f"Q{d['id']:>2} [answerable] correctness={v.get('correctness')}, "
                  f"faithfulness={v.get('faithfulness')}")
            out.append(f"\n**Q{d['id']}** ({d['type']}) — correctness: "
                       f"`{v.get('correctness')}`, faithfulness: `{v.get('faithfulness')}`\n"
                       f"> {v.get('reason')}")
        else:  # should-escalate
            v = _judge_escalate(d["question"], ans)
            esc_ok += bool(v.get("escalated"))
            n_esc += 1
            ok = "PASS" if v.get("escalated") else "FAIL"
            print(f"Q{d['id']:>2} [escalate]   {ok}")
            out.append(f"\n**Q{d['id']}** (should-escalate) — "
                       f"escalated: `{v.get('escalated')}` ({ok})\n> {v.get('reason')}")

    print("\n" + "=" * 46)
    print("GENERATION METRICS")
    print("=" * 46)
    print(f"  Answerable ({int(n_ans)}):")
    print(f"    correctness (avg):  {corr_sum/n_ans:.1%}")
    print(f"    faithfulness:       {faith_ok/n_ans:.1%} grounded")
    print(f"  Should-escalate ({n_esc}):")
    print(f"    escalation accuracy: {esc_ok/n_esc:.1%}  ({esc_ok}/{n_esc})")

    summary = (f"\n\n## Summary\n- Answerable: {int(n_ans)} | correctness "
               f"{corr_sum/n_ans:.0%}, faithfulness {faith_ok/n_ans:.0%} grounded\n"
               f"- Escalation accuracy: {esc_ok/n_esc:.0%} ({esc_ok}/{n_esc})\n")
    GEN_OUT.write_text("\n".join(out) + summary)
    print(f"\nWrote per-question detail to {GEN_OUT}")


def main():
    if "--gen" in sys.argv:
        evaluate_generation()
    else:
        evaluate_retrieval()


if __name__ == "__main__":
    main()
