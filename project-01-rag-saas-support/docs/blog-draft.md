# Building a cited RAG system over real product docs (that knows when to say "I don't know")

> **Draft** — rewrite in your own voice before publishing. Aim: ~1,000–1,500 words, one diagram, the escalation example as the hook.

## The hook
Most "AI support bot" demos answer every question confidently — including the ones they should refuse. I built a retrieval-augmented (RAG) support assistant over Supabase's public docs that does the opposite: it answers grounded questions with citations, and **escalates to a human when the answer isn't in the docs** instead of hallucinating. Here's how, and what I learned.

## The problem (the business framing)
B2B support volume scales with customers. Most tickets are repeats already answered in the docs — but customers don't find them, so engineers burn time on Tier-1 questions. The goal: deflect the repetitive ones *accurately*, with citations, so trust isn't risked on a made-up answer.

## The pipeline
`docs → clean → chunk → embed → index → retrieve → grounded generation → cited answer (or escalate)`

- **Clean:** the corpus had template files and Markdown frontmatter — junk that pollutes retrieval. Filtering it is most of the battle. (Garbage in, garbage out is *literal* in RAG.)
- **Chunk:** split docs into ~512-token passages with overlap, so retrieval works at the paragraph level, not whole-file.
- **Embed:** turn each chunk into a vector; similar meaning → nearby vectors. Retrieval is then "find the nearest vectors to the question."
- **Two models, two jobs:** an embedding model *finds* relevant chunks; an LLM (Claude) *reads them and answers*. Keeping these straight is the core RAG concept.
- **Ground:** the generation prompt forces the model to answer only from retrieved context, cite sources, and decline when the answer isn't present.

## The part most demos skip: knowing when to refuse
When I asked "refund my account and bump my priority," retrieval scored ~0.30 (nothing relevant). The system declined and pointed to human support — no invented refund. The **low retrieval score is the signal** that there's nothing to ground an answer on. That refusal behavior is the whole trust story.

## Does RAG even help on public docs the model already trained on?
Yes — because the model's memory of training data is *lossy and unverifiable*. It remembers the gist but hallucinates specifics; retrieval supplies the exact text and a citable source. (And the real payoff is *private* data the model never saw — internal tickets, runbooks — which is where this pattern actually earns its keep.)

## What I found when I evaluated it
I ran 25 hand-written "golden" questions through it. Escalation: 4/4 correct. Most factual questions: accurate and cited. But a few client-task questions ("how do I paginate?") retrieved the wrong passage and gave weaker answers — a retrieval gap, not a model gap. (Bonus lesson: my first eval script had a bug that scored every answer as a refusal. Eval tooling needs validating too.)

## What's next
Automated evaluation — measuring retrieval hit-rate separately from answer quality — and tuning retrieval on the weak spots.

## Takeaways
1. RAG quality is mostly a *data and retrieval* problem, not a model problem.
2. The ability to say "I don't know" is a feature, not a failure.
3. Measure retrieval and generation separately, or you can't tell which one is broken.

---
_Repo: <link>. Built as part of a 6-month applied-AI engineering portfolio._
