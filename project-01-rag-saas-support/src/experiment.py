"""Day 5 — controlled retrieval-tuning experiment.

Vary one knob at a time, re-measure. Here: chunk_size (256 / 512 / 1024) and
then top_k on the best size. Apples-to-apples on the same golden set.

Run:  python -m src.experiment
"""

from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding

from src.ingest import load_documents
from src.eval import load_answerable

Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")


def build_index(docs, chunk_size, overlap=50):
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return VectorStoreIndex.from_documents(docs, transformations=[splitter])


def score(index, items, k=5):
    hits = {1: 0, 3: 0, 5: 0}
    recall5 = rr = 0.0
    retr = index.as_retriever(similarity_top_k=k)
    for d in items:
        files = [n.node.metadata.get("file_name") for n in retr.retrieve(d["question"])]
        exp = set(d["expected_sources"])
        rank = next((i + 1 for i, f in enumerate(files) if f in exp), None)
        rr += (1.0 / rank) if rank else 0.0
        for kk in (1, 3, 5):
            if rank and rank <= kk:
                hits[kk] += 1
        recall5 += len(exp & set(files[:5])) / len(exp)
    n = len(items)
    return {1: hits[1] / n, 3: hits[3] / n, 5: hits[5] / n,
            "recall5": recall5 / n, "mrr": rr / n}


def line(label, m):
    return (f"{label:<16} hit@1={m[1]:.1%}  hit@3={m[3]:.1%}  hit@5={m[5]:.1%}  "
            f"recall@5={m['recall5']:.1%}  MRR={m['mrr']:.3f}")


def main():
    docs = load_documents()
    items = load_answerable()
    print(f"Tuning on {len(items)} answerable questions.\n")

    print("== Experiment 1: chunk_size (overlap=50, top_k=5) ==")
    indexes = {}
    for size in (256, 512, 1024):
        idx = build_index(docs, size)
        indexes[size] = idx
        print(line(f"chunk={size}", score(idx, items, k=5)))

    print("\n== Experiment 2: top_k on chunk=512 ==")
    for k in (5, 10):
        print(line(f"chunk=512 k={k}", score(indexes[512], items, k=k)))


if __name__ == "__main__":
    main()
