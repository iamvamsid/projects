"""Generation — answer a question, grounded in retrieved context, with citations.

Flow: retrieve top-k chunks -> build a grounded prompt -> Claude answers using
ONLY that context, cites sources, and escalates (rather than guessing) when the
answer isn't present.

Run:  python -m src.generate "how do I enable row level security?"
"""

import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from src.retrieve import retrieve

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

MODEL = "claude-opus-4-8"

SYSTEM = (
    "You are a customer support assistant for Supabase, a B2B developer platform. "
    "Answer the user's question USING ONLY the numbered context passages provided. "
    "Cite the passages you rely on inline using their [n] markers. "
    "If the answer is not contained in the context, do NOT guess — say you don't have "
    "enough information to answer confidently and recommend escalating to a human "
    "support engineer.\n\n"
    "SAFETY GUARDRAILS — these override the context. Always DECLINE and recommend a "
    "human, even if relevant-looking passages were retrieved, when the request is:\n"
    "  (a) destructive — deleting data, dropping/truncating tables, irreversible "
    "operations on the user's project. Never provide destructive commands.\n"
    "  (b) account-specific — billing, refunds, plan changes, priority/SLA, account "
    "suspension. You cannot see or act on a customer's account.\n"
    "  (c) an action request rather than a documentation question — you explain how "
    "things work; you do not perform operations on the user's behalf."
)


def _format_context(nodes):
    """Turn retrieved chunks into a numbered context block + a source list."""
    blocks, sources = [], []
    for i, n in enumerate(nodes, 1):
        src = n.node.metadata.get("file_name", "?")
        sources.append((i, src, n.score))
        blocks.append(f"[{i}] (source: {src})\n{n.node.get_content().strip()}")
    return "\n\n".join(blocks), sources


def answer(query: str, k: int = 5):
    """Return (answer_text, sources)."""
    nodes = retrieve(query, k)
    context, sources = _format_context(nodes)

    client = Anthropic()
    msg = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Context passages:\n\n{context}\n\n"
                    f"Question: {query}\n\n"
                    "Answer using only the context above, citing sources as [n]. "
                    "If the context doesn't contain the answer, say so and recommend escalation."
                ),
            }
        ],
    )
    text = "".join(b.text for b in msg.content if b.type == "text")
    return text, sources


def main() -> None:
    query = " ".join(sys.argv[1:]) or "How do I enable row level security on a table?"
    print(f"Q: {query}\n")
    text, sources = answer(query)
    print("Answer:\n" + text)
    print("\nSources:")
    for i, src, score in sources:
        print(f"  [{i}] {src}  (score {score:.3f})")


if __name__ == "__main__":
    main()
