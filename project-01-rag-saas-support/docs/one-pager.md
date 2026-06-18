# Deflect repetitive support tickets — without wrong answers

_A one-page brief for a VP of Engineering / Head of Support at a B2B software company._

---

## The business problem

Your support volume grows with every new customer. Most incoming tickets are repeat questions already answered somewhere in your documentation or in past resolved tickets — but customers don't find those answers, so your engineers spend hours on Tier-1 questions instead of building product. Hiring more support staff scales cost linearly with revenue. The constraint isn't knowledge; it's *retrieval* — getting the right answer to the customer at the right moment.

## What this does

An AI assistant answers customer support questions directly from your own documentation and resolved tickets, and **shows the source for every answer**. Customers get an instant, correct, cited answer; your team only sees the questions that genuinely need a human.

## Why now

Modern language models are finally accurate enough to answer grounded technical questions — *if* they're constrained to your real content and made to cite their sources. The difference between a useful deployment and a liability is engineering discipline: retrieval quality, grounding, and measurable accuracy. That discipline is what this system is built around.

## How it works (high level)

- Ingests your documentation and resolved support tickets into a searchable knowledge base.
- For each customer question, retrieves the most relevant passages.
- Generates an answer **grounded only in those passages**, with citations back to the source.
- Escalates to a human — rather than guessing — when confidence is low.

No customer trust is risked on a hallucinated answer: every response is traceable to a source, and the system is measured continuously for accuracy.

## What success looks like

| Metric | What it means to you |
|---|---|
| **Ticket deflection rate** | Share of questions resolved without a human (target: 30–50% on repetitive questions). |
| **Answer accuracy / faithfulness** | A hard guardrail — answers are grounded and cited, not invented. |
| **Time-to-answer** | Customers get instant responses instead of waiting in a queue. |
| **Engineer hours reclaimed** | Senior time returned to building product. |

## What we'd need from you

- Access to your documentation and a sample of resolved support tickets.
- A subject-matter expert for ~2 hours to validate a first batch of answers.
- Light IT cooperation to connect the knowledge sources.

---

_Prepared as part of an applied-AI engineering portfolio. Hypothetical customer: a 200–800-person B2B developer-tools SaaS (Series B/C)._
