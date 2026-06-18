# Under the Hood — how this RAG pipeline actually works

> **Why this file exists:** I used LlamaIndex (a framework) to move fast. This note is where I prove to myself — and to an interviewer — that I understand what the framework does *for* me. If I can't explain a section here in my own words, I don't understand it yet.
>
> _Draft — rewrite each section in your own words._

## The pipeline in one line
`raw docs → clean → chunk into nodes → embed each chunk → store vectors in an index → (later) retrieve nearest chunks for a query → ground an LLM answer in them, with citations`

---

## 1. Loading & cleaning
- **Source:** Supabase docs (`auth/`, `database/`, `storage/`), 210 `.mdx` files → one `Document` each.
- **Cleaning matters more than the model.** We dropped `_`-prefixed template files and stripped YAML frontmatter + MDX/JSX syntax. Junk in the corpus → junk chunks retrieved → hallucinated answers. Retrieval quality is mostly a *data* problem.
- Result: 210 files → **209 real documents**.

## 2. Chunking (Document → Nodes)
- A whole doc is too big to retrieve usefully — embedding 18,000 chars into one vector blurs its meaning. So we split each doc into smaller **nodes (chunks)**.
- **Choices made:** `chunk_size=512` tokens, `chunk_overlap=50` tokens (via `SentenceSplitter`).
  - *Why 512:* small enough to be a precise, single-topic passage; big enough to hold a coherent idea.
  - *Why overlap:* a 50-token overlap means an idea spanning a chunk boundary isn't cut in half — the adjacent chunk repeats the seam, so context isn't lost.
- Result: 209 docs → **1,137 chunks**.
- **Tradeoff to remember:** smaller chunks = more precise retrieval but more fragments; larger chunks = more context per hit but fuzzier matching. 512 is a common starting point, not a law — tune it with the eval set.

## 3. Embedding (text → vectors) — the heart of retrieval
- An **embedding** turns a chunk of text into a vector (a list of numbers) that captures its *meaning*. Texts with similar meaning land near each other in vector space.
- **Model used:** OpenAI `text-embedding-3-small` (1,536 dimensions). Cheap, fast, strong baseline.
- This is how "find relevant docs" becomes math: embed the query the same way, then find the chunks whose vectors are **closest** (cosine similarity) to the query vector.
- Cost reality: embedding all 1,137 chunks cost ~1–2 cents and took ~17s.

## 4. The index (storage)
- The 1,137 vectors + their chunk text + metadata are stored as a **vector index**, persisted to `storage/` so we don't re-embed every run.
- Files: `default__vector_store.json` (the vectors), `docstore.json` (chunk text + metadata), `index_store.json` (structure).

## 5. Two distinct models, two distinct jobs (don't blur these!)
| Role | Model | Job |
|---|---|---|
| **Embedding model** | OpenAI `text-embedding-3-small` | text → vectors, for *finding* relevant chunks |
| **Generation model (LLM)** | Claude `claude-opus-4-8` | *read* the retrieved chunks → *write* the grounded answer |
- **Embeddings find; the LLM answers.** This is the single most important RAG concept.

## 6. Retrieval + generation (built — Day 3-4)
- **Retrieval (`retrieve.py`):** load the persisted index → embed the question with the **same** model used at ingest → cosine-similarity search → return **top-k=5** chunks, each with a similarity score + source metadata. (Score 1.0 = identical meaning; observed ~0.69 for a strong hit, ~0.30 for an off-topic question.)
- **Generation (`generate.py`):** format the retrieved chunks into a numbered context block, then call Claude (`claude-opus-4-8`) with a **grounding system prompt**: answer *only* from the context, cite passages as `[n]`, and if the answer isn't present, **decline and recommend a human** rather than guess.
- **Why the raw Anthropic SDK for generation (not the framework's query engine):** the grounding prompt is the most important, most tunable part — writing it explicitly keeps it visible and under my control, instead of hidden inside `as_query_engine()`.
- **Citations:** the `file_path`/`file_name` metadata rides from Document → Node → retrieved result → into the answer, so every claim points back to its source doc.
- **Observed behavior:** answerable questions → accurate cited answers (RLS scored 0.69). Unanswerable account/billing questions → low scores (~0.30) → declined + escalated, **no hallucination**. The low score *is* the signal that retrieval found nothing relevant.
- **Key insight:** retrieval quality drives everything. Low-score factual questions (pagination 0.33) produced weak/hedged answers — the model is only as good as the chunks it's handed. Separating "did retrieval find the right chunk?" from "did generation answer well?" is the core of evaluation (Week 3).

---

## Questions an interviewer might ask (practice answering)
- Why chunk at all? Why 512 tokens?
- What's an embedding, and why cosine similarity?
- How do you stop the system hallucinating?
- How would you know if retrieval is bad vs. generation is bad? (→ eval, Week 3)
- What would you change to cut cost / latency in production?
- **If the docs are public and already in the model's training data, does RAG even help?** (see below — strong answer)

---

## Deep dive: does RAG help when the model already saw the data?

**Verdict: good retrieval *increases* correctness and trust even on trained-on data; bad retrieval can *decrease* it.**

**Why it helps even on "seen" data:**
1. **Parametric memory is lossy.** The model compressed its training data into weights — it remembers the *gist* but hallucinates *specifics* (exact flags, signatures, defaults, version behavior). Retrieval supplies the exact text, so it stops guessing details.
2. **Grounding makes it verifiable.** Without context you can't tell a correct answer from a confident hallucination. Retrieved chunks anchor the answer to a real, **citable** source — impossible from pure parametric knowledge, and the whole point in a support/enterprise setting.
3. **Freshness.** Training froze at a cutoff; docs change weekly. RAG always reflects the current source of truth.
4. **Disambiguation.** Models conflate similar things (Supabase vs raw Postgres vs Firebase, v1 vs v2). Context pins the answer to *this* product/version.

**The caveat (the senior nuance):** RAG's correctness is **bounded by retrieval quality**.
- Wrong chunks retrieved → the model is grounded in irrelevant/contradictory text → answer can be *worse* than its own knowledge, and confidently cited.
- Outdated/wrong docs → RAG faithfully reproduces the error.
- This is exactly why eval (Week 3) measures retrieval quality *separately* from generation quality.

**The deeper point (FDE framing):** public docs are the **weakest** case for RAG — chosen because the data is easy to get. RAG's real payoff is **private data the model has never seen**: a customer's internal tickets, runbooks, wikis, codebase, policies, account state. That's the actual FDE deployment — *"run this over the customer's private corpus, which no public model has ever touched."* Supabase docs are the learning proxy; private data is where the value is.

**One-liner:** *RAG raises correctness even on trained-on data because parametric memory is lossy and unverifiable — it fixes specifics, adds citations, stays fresh. But it's only as good as retrieval, and its real power is private data the model never saw.*
