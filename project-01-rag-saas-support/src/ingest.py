"""Ingestion — build the knowledge base.

Pipeline:  load files -> clean -> chunk into nodes -> embed -> persist index.

Run:  python -m src.ingest          (full build: embeds + persists)
      python -m src.ingest --stats  (local only: clean + chunk counts, no API)
"""

import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from llama_index.core import (
    Document,
    Settings,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = PROJECT_ROOT / "data" / "corpus"
INDEX_DIR = PROJECT_ROOT / "storage"          # persisted vector index lives here

# --- Deliberate choices (documented in notes/under-the-hood.md) ---
EMBED_MODEL = "text-embedding-3-small"        # cheap, 1536-dim, strong baseline
CHUNK_SIZE = 512                              # tokens per chunk — small enough to be precise
CHUNK_OVERLAP = 50                            # tokens shared between adjacent chunks (keeps context across the seam)


def _clean(text: str) -> str:
    """Strip non-content noise so only real prose gets embedded."""
    # YAML frontmatter block at the top: --- ... ---
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    # MDX/JSX comments: {/* ... */}
    text = re.sub(r"\{/\*.*?\*/\}", "", text, flags=re.DOTALL)
    # MDX import/export lines
    text = re.sub(r"^(import|export)\s.*$", "", text, flags=re.MULTILINE)
    # collapse 3+ blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_documents():
    """Load .md/.mdx files, drop template/partial files, and clean the text."""
    if not CORPUS_DIR.exists():
        raise FileNotFoundError(
            f"Corpus not found at {CORPUS_DIR}. Run the sparse-checkout step first."
        )

    docs = SimpleDirectoryReader(
        input_dir=str(CORPUS_DIR),
        required_exts=[".md", ".mdx"],
        recursive=True,
    ).load_data()

    kept, dropped = [], 0
    for d in docs:
        name = d.metadata.get("file_name", "")
        if name.startswith("_"):          # _flow-template.mdx, partials, includes
            dropped += 1
            continue
        cleaned = _clean(d.text)
        if not cleaned:                   # nothing left after cleaning
            dropped += 1
            continue
        # Document.text is read-only — build a fresh Document with cleaned text,
        # preserving metadata (file_path -> citations) and id.
        kept.append(Document(text=cleaned, metadata=d.metadata, id_=d.id_))

    print(f"Loaded {len(docs)} files -> kept {len(kept)}, dropped {dropped} (templates/empty).")
    return kept


def build_index() -> None:
    """Full build: chunk -> embed -> persist."""
    docs = load_documents()

    # Configure the two models/components globally for this build.
    Settings.embed_model = OpenAIEmbedding(model=EMBED_MODEL)
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    print(f"Embedding with {EMBED_MODEL}; chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}...")
    index = VectorStoreIndex.from_documents(
        docs,
        transformations=[splitter],
        show_progress=True,
    )

    index.storage_context.persist(persist_dir=str(INDEX_DIR))
    print(f"\n✅ Index built and persisted to {INDEX_DIR}")


def stats() -> None:
    """Local-only: show how many chunks the corpus produces. No API calls."""
    docs = load_documents()
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    nodes = splitter.get_nodes_from_documents(docs)
    print(f"\nChunking: {len(docs)} docs -> {len(nodes)} chunks "
          f"(chunk_size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print("\nExample chunk (nodes[0]):")
    print(f"  source: {nodes[0].metadata.get('file_name')}")
    print(f"  chars : {len(nodes[0].text)}")
    print("  text  :", nodes[0].text[:200].replace("\n", " "), "...")


def main() -> None:
    if "--stats" in sys.argv:
        stats()
    else:
        build_index()


if __name__ == "__main__":
    main()
