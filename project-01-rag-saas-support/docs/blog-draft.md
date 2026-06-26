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
I built a two-part eval harness that scores retrieval and generation *separately* — because "bad answer" has two very different causes (the right doc was never found vs. it was found and the model fumbled). What that surfaced was the real story:

- **A safety bug.** "Delete my entire production database" got back actual `DROP TABLE` commands, because retrieval found a deletion doc and the model dutifully answered. A support bot must refuse that. Eval caught it; I added a guardrail.
- **My graders had bugs before my system did.** One eval script scored every answer as a refusal (a keyword false-positive); another deflated faithfulness to 38% by showing the judge only part of the context. *Eval tooling needs validating too* — distrust the number, read the reasoning.
- **A corpus-coverage gap, not a retrieval gap.** Questions that scored badly turned out to ask about docs I never ingested (Realtime, Edge Functions). The fix isn't better search — it's matching the knowledge base to the questions.
- **Chunk size is a tempting-but-wrong lever.** Bigger chunks improved hit-rate@1 — but not recall@5, which is what actually feeds the generator. So it bought a vanity metric for more cost. The real bottleneck was elsewhere (hybrid retrieval).

The theme: a number you can't explain is worse than no number. Most of the work was learning *which* number to trust.

## What's next
Automated evaluation — measuring retrieval hit-rate separately from answer quality — and tuning retrieval on the weak spots.

## Takeaways
1. RAG quality is mostly a *data and retrieval* problem, not a model problem.
2. The ability to say "I don't know" is a feature, not a failure.
3. Measure retrieval and generation separately, or you can't tell which one is broken.

---
_Repo: <link>. Built as part of a 6-month applied-AI engineering portfolio._
