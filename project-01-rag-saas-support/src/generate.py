"""Generation — answer a question, grounded in retrieved context, with citations.

Week 2: take the top-k chunks from retrieve.py and ask Claude to answer
ONLY from that context, citing sources, and to say "I don't know / escalate"
when the context doesn't contain the answer.

Placeholder for now.
"""


def answer(query: str) -> str:
    raise NotImplementedError("Generation lands in Week 2.")


if __name__ == "__main__":
    answer("placeholder")
