# Day 2 Worklog — Ingestion Pipeline (for review)

**Date:** 2026-06-18
**Goal:** Build the RAG ingestion pipeline — clean → chunk → embed → persist a vector index over the Supabase docs corpus.
**Result:** ✅ Done. 209 cleaned docs → 1,137 embedded chunks → persisted index in `storage/`.

---

## 1. What was built

### `src/ingest.py` (rewritten)
The full ingestion pipeline. Key parts:
- **`load_documents()`** — loads `.md/.mdx` files via `SimpleDirectoryReader`, then:
  - drops `_`-prefixed files (templates/partials, e.g. `_flow-template.mdx`),
  - cleans each doc with `_clean()`,
  - rebuilds each as a fresh `Document` (because `Document.text` is read-only in this LlamaIndex version), preserving metadata + id.
- **`_clean(text)`** — strips YAML frontmatter (`--- ... ---`), MDX/JSX comments (`{/* ... */}`), MDX `import/export` lines, and collapses blank lines.
- **`build_index()`** — sets the embedding model + chunk splitter, builds a `VectorStoreIndex`, and persists it to `storage/`.
- **`stats()`** (`--stats` flag) — local-only: prints cleanup + chunk counts with **no API calls** (used to sanity-check before spending on embeddings).

### `notes/under-the-hood.md` (new)
Plain-English explanation of the pipeline (chunking, embeddings, retrieval, grounding) — interview-prep ammo. **Draft — needs rewriting in your own words.**

### `.gitignore` (updated)
Added `storage/` (the persisted index is a regenerable build artifact, ~36 MB — don't commit).

### `requirements.txt` (restored)
Re-added the 4 deps that had been lost (`pydantic`, `llama-index-core`, `llama-index-llms-anthropic`, `llama-index-embeddings-openai`).

---

## 2. Decisions made (and why)

| Decision | Value | Rationale |
|---|---|---|
| Embedding model | OpenAI `text-embedding-3-small` (1536-dim) | Cheap, fast, strong baseline |
| Chunk size | 512 tokens | Precise single-topic passages |
| Chunk overlap | 50 tokens | Keeps context across chunk seams |
| Drop `_`-prefixed files | — | They're Supabase's internal templates, not real docs |
| Strip frontmatter/MDX | — | Markup noise dilutes embedding meaning |
| Persist index to `storage/` | — | Avoid re-embedding every run |

---

## 3. Problems hit & fixed (the debugging trail)

1. **`ModuleNotFoundError: llama_index`** → root cause was a **truncated `requirements.txt`** (llama-index lines missing), NOT the Python version. Restored the file; installed into the shared `.ai-proj` venv.
   - *Correction:* earlier I suspected Python 3.14 was too new. It's actually fine — llama-index runs on 3.14 here.
2. **`AttributeError: property 'text' has no setter`** → `Document.text` is read-only in this LlamaIndex version. Fixed by constructing new `Document` objects with cleaned text instead of mutating in place.
3. **`OpenAIError: Missing credentials`** → the project had no `.env`; keys lived in the sandbox-root `projects/.env`. Fixed by copying keys into the project `.env` (confirmed gitignored — no leak).

---

## 4. Verification (what we actually observed)

```
Loaded 210 files -> kept 209, dropped 1 (templates/empty).
Chunking: 209 docs -> 1137 chunks (chunk_size=512, overlap=50)
Embedding with text-embedding-3-small ... 1137/1137 in ~17s
✅ Index persisted to storage/
   default__vector_store.json  36 MB  (the 1137 vectors)
   docstore.json                4 MB  (chunk text + metadata)
   index_store.json            96 KB  (index structure)
```
Example cleaned chunk (`architecture.mdx`) verified free of frontmatter/MDX noise.

---

## 5. Current state
- Ingestion: **complete and verified.**
- Index: **built and persisted** (not committed — gitignored, regenerable).
- Secrets: project `.env` present, **gitignored, no leak**.
- Not yet committed to git (suggested commit message ready).

## 6. Open items / next
- [ ] **Rewrite `under-the-hood.md` in your own words** (interview prep).
- [ ] **Commit + push** Day 2 work.
- [ ] **Day 3:** `retrieve.py` + `generate.py` — load the index, retrieve top-k, have Claude answer grounded + cited.
- [ ] Carry-over: verify the golden-question expected answers against live docs.
