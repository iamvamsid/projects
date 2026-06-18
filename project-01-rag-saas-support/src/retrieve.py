"""Retrieval — find the most relevant chunks for a query.

Loads the persisted vector index, embeds the query, and returns the top-k
most similar chunks (with their source metadata for citations).

Run:  python -m src.retrieve "how do I enable row level security?"
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.openai import OpenAIEmbedding

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = PROJECT_ROOT / "storage"

# MUST match the model used in ingest.py — the query is embedded with the same
# model the chunks were, or the vectors aren't comparable.
EMBED_MODEL = "text-embedding-3-small"

_index = None


def get_index():
    """Load the persisted index once and cache it."""
    global _index
    if _index is None:
        if not INDEX_DIR.exists():
            raise FileNotFoundError(
                f"No index at {INDEX_DIR}. Run `python -m src.ingest` first."
            )
        Settings.embed_model = OpenAIEmbedding(model=EMBED_MODEL)
        storage_context = StorageContext.from_defaults(persist_dir=str(INDEX_DIR))
        _index = load_index_from_storage(storage_context)
    return _index


def retrieve(query: str, k: int = 5):
    """Return the top-k most similar chunks (NodeWithScore objects)."""
    retriever = get_index().as_retriever(similarity_top_k=k)
    return retriever.retrieve(query)


def main() -> None:
    query = " ".join(sys.argv[1:]) or "How do I enable row level security on a table?"
    print(f"Q: {query}\n")
    for n in retrieve(query):
        snippet = n.node.get_content()[:160].replace("\n", " ")
        print(f"[score {n.score:.3f}] {n.node.metadata.get('file_name')}")
        print(f"    {snippet} ...\n")


if __name__ == "__main__":
    main()
