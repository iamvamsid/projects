"""Generate a descriptive textbook-style PDF on RAG Evaluation (Week 3)."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted,
    Spacer, PageBreak, Table, TableStyle,
)

OUT = "/Users/vamsidhar/Google/ai-journey/notes/rag-evaluation-textbook.pdf"

ACCENT = colors.HexColor("#5a2a82")
ACCENT2 = colors.HexColor("#7b4ca8")
CODEBG = colors.HexColor("#f4f2f6")
PROJBG = colors.HexColor("#eef0f8")
PLAINBG = colors.HexColor("#e9f5ee")
WARNBG = colors.HexColor("#fdf0e9")

styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=8)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=20, leading=24, textColor=ACCENT, spaceAfter=12)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=13.5, leading=18, textColor=ACCENT2, spaceBefore=12, spaceAfter=6)
codest = ParagraphStyle("code", parent=styles["Code"], fontName="Courier",
                        fontSize=8.2, leading=11, textColor=colors.HexColor("#222"))
chapno = ParagraphStyle("chapno", parent=body, fontName="Helvetica-Bold",
                        fontSize=11, textColor=ACCENT2, spaceAfter=2)
tocst = ParagraphStyle("toc", parent=body, fontSize=11, leading=18, spaceAfter=2)
titlest = ParagraphStyle("title", parent=styles["Title"], fontName="Helvetica-Bold",
                         fontSize=29, leading=34, textColor=ACCENT, alignment=TA_CENTER)
subst = ParagraphStyle("sub", parent=body, fontSize=14, leading=20,
                       alignment=TA_CENTER, textColor=colors.HexColor("#555"))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


story = []


def CODE(text):
    rows = [[Preformatted(text.strip("\n"), codest)]]
    t = Table(rows, colWidths=[16.0 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CODEBG),
                           ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d4cfdb")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def boxflow(text, bg, label, bar):
    inner = Paragraph(f'<b>{esc(label)}</b><br/>{text}',
                      ParagraphStyle("bx", parent=body, fontSize=9.7, leading=14, spaceAfter=0))
    t = Table([[inner]], colWidths=[16.0 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                           ("LINEBEFORE", (0, 0), (0, -1), 3, bar)]))
    return [Spacer(1, 4), t, Spacer(1, 8)]


def chapter(num, title):
    story.append(PageBreak())
    story.append(Paragraph(f"CHAPTER {num}", chapno))
    story.append(Paragraph(esc(title), h1))


def sec(t): story.append(Paragraph(esc(t), h2))
def para(t): story.append(Paragraph(t, body))
def code(t): story.append(CODE(t)); story.append(Spacer(1, 6))
def proj(t): story.extend(boxflow(t, PROJBG, "IN OUR PROJECT", ACCENT2))
def plain(t): story.extend(boxflow(t, PLAINBG, "IN PLAIN WORDS", colors.HexColor("#3a9c6a")))
def warn(t): story.extend(boxflow(t, WARNBG, "WATCH OUT", colors.HexColor("#d98841")))


def simple_table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ACCENT2),
                           ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                           ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                           ("FONTSIZE", (0, 0), (-1, -1), 9), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story.append(t); story.append(Spacer(1, 8))


# ===== COVER =====
story.append(Spacer(1, 5 * cm))
story.append(Paragraph("Evaluating RAG Systems", titlest))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("How to Stop Guessing and Start Measuring", subst))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("Ground truth, retrieval metrics, LLM-as-judge, safety,<br/>"
                       "tuning, and evaluation in production &mdash; every concept<br/>"
                       "from Week 3, explained in plain words.", subst))
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("Companion to project-01-rag-saas-support", subst))

# ===== TOC =====
story.append(PageBreak())
story.append(Paragraph("Contents", h1))
for item in [
    "1.  Why Evaluate at All?",
    "2.  The Anatomy of a RAG Answer (and Why We Grade Two Things)",
    "3.  Ground Truth and the Golden Set",
    "4.  The Corpus-Coverage Trap",
    "5.  Retrieval Metrics: hit-rate, recall, precision, MRR",
    "6.  Generation Metrics: the LLM-as-Judge",
    "7.  Correctness vs Faithfulness",
    "8.  Validate the Grader (Eval Tooling Has Bugs Too)",
    "9.  Safety Evaluation",
    "10. The Chunk-Size Experiment (and the Vanity-Metric Trap)",
    "11. Evaluation in Production (the Senior View)",
    "12. Our Results, Lessons, and Glossary",
]:
    story.append(Paragraph(esc(item), tocst))

# ===== CH1 =====
chapter(1, "Why Evaluate at All?")
para("After you build a system that answers questions, the obvious question is: <b>is it "
     "any good?</b> It is tempting to type in a few questions, see sensible answers, and "
     "declare victory. That is not evaluation &mdash; that is a vibe. The moment you change "
     "anything (a prompt, the chunk size, the model), the vibe tells you nothing about "
     "whether you made things better or worse.")
para("Evaluation is the discipline of turning &quot;it seems to work&quot; into a "
     "<b>number you can trust and reproduce</b>. It is what lets you say &quot;this change "
     "improved accuracy from 54% to 62%&quot; instead of &quot;this feels better.&quot; In a "
     "real deployment it is also how you <i>prove</i> the system works to a customer, and "
     "how you catch the system silently breaking.")
plain("Evaluation = building a report card for your AI, so that every change you make can "
      "be graded instead of guessed at.")
para("The most important mindset shift: a system that produces a confident answer is not "
     "the same as a system that produces a <i>correct</i> one. Without evaluation you cannot "
     "tell a right answer from a confident hallucination. Evaluation is the instrument that "
     "tells them apart.")

# ===== CH2 =====
chapter(2, "The Anatomy of a RAG Answer (and Why We Grade Two Things)")
para("A RAG (Retrieval-Augmented Generation) system answers in two steps:")
para("<b>Step 1 &mdash; Retrieval (the FIND step).</b> It searches your documents and pulls "
     "out the handful of passages most relevant to the question.")
para("<b>Step 2 &mdash; Generation (the ANSWER step).</b> It hands those passages to a "
     "language model, which reads them and writes the answer.")
para("This two-step shape is the single most important thing to understand, because <b>a "
     "bad answer can come from either step, and the fixes are completely different:</b>")
simple_table([["If the failure is in", "It means", "You fix"],
              ["Retrieval", "the right info was never found", "search: chunking, embeddings, hybrid"],
              ["Generation", "the info was found but the model fumbled it", "the prompt, the model, grounding"]],
             [3.5 * cm, 6.0 * cm, 6.0 * cm])
para("If you only measure one blurry &quot;accuracy&quot; number, you can never tell which "
     "half is broken. So we build <b>two separate graders</b> &mdash; one for retrieval, one "
     "for generation &mdash; and that separation is the backbone of everything that follows.")
plain("Think of it like a student doing open-book research: did they open the right page "
      "(retrieval), and then did they write a good answer from it (generation)? Two skills, "
      "graded separately.")

# ===== CH3 =====
chapter(3, "Ground Truth and the Golden Set")
para("To grade anything you need an answer key. In evaluation this is called <b>ground "
     "truth</b>: the known-correct answer you compare the system against. The collection of "
     "test questions plus their ground truth is the <b>golden set</b>.")
para("For each question we record two kinds of ground truth:")
para("&bull; <b>The expected source</b> &mdash; which document page <i>should</i> be "
     "retrieved. This is the answer key for the FIND step.")
para("&bull; <b>The gold answer</b> &mdash; the key facts a correct answer must contain. "
     "This is the answer key for the ANSWER step.")
proj("We wrote 25 golden questions for the Supabase support assistant and stored them in "
     "<font name='Courier'>golden_set.json</font>. To tag each question's expected source "
     "honestly, we searched the actual docs for the answer rather than guessing &mdash; so "
     "the answer key is grounded in reality.")
para("A golden set is never &quot;done.&quot; In production it becomes a <b>living "
     "dataset</b>: every new failure you discover gets added as a new test, so the system "
     "can never regress on a bug you have already seen.")
warn("Your numbers are only ever as trustworthy as your answer key. If you tag the wrong "
     "expected page, a perfectly good retrieval will look like a failure. Always suspect the "
     "answer key when a result surprises you.")

# ===== CH4 =====
chapter(4, "The Corpus-Coverage Trap")
para("When we tagged expected sources, we found something important: several test questions "
     "asked about topics that <b>were never loaded into the system</b>. Our document "
     "collection (the &quot;corpus&quot;) only covered three sections; but some questions "
     "asked about features in other sections we had not ingested.")
plain("It is like setting an exam with questions from chapters 5 and 7, when the student's "
      "textbook only contains chapters 1 to 3. They cannot answer &mdash; not because they "
      "are weak, but because the material is not in their book.")
para("This reframed an earlier mystery. Some questions had given weak answers, and we had "
     "assumed the <i>search</i> was bad. In fact the answer simply <b>was not in the "
     "knowledge base</b>. That is a <b>corpus-coverage problem</b>, not a retrieval problem "
     "&mdash; a totally different diagnosis with a different fix (add the missing docs, or "
     "accept the system should decline).")
proj("We chose to keep the corpus as-is and <b>reclassify</b> the out-of-scope questions as "
     "&quot;should escalate&quot; &mdash; the system is <i>supposed</i> to say &quot;I do not "
     "have that information.&quot; This turned a coverage gap into a useful test of the "
     "system's honesty.")
para("This is one of the most common real-world causes of bad AI answers: a mismatch "
     "between what users ask and what the knowledge base actually contains. Good evaluation "
     "surfaces it instead of hiding it inside a low accuracy score.")

# ===== CH5 =====
chapter(5, "Retrieval Metrics: hit-rate, recall, precision, MRR")
para("These metrics grade the FIND step &mdash; did the right document show up? They are "
     "cheap and deterministic (no language model needed).")
sec("hit-rate@k")
para("<b>hit-rate@k = the fraction of questions where the correct page appears somewhere in "
     "the top k results, each question counted once.</b> hit-rate@3 = 0.7 means: for 70% of "
     "questions, the right page was in the top 3.")
para("Because a page in the top 1 is also in the top 3, the numbers only ever grow as k "
     "grows: hit-rate@1 is less than or equal to hit-rate@3 is less than or equal to "
     "hit-rate@5. It is a yes/no per question, not a sum of separate hits.")
sec("recall@k &mdash; for answers spread across pages")
para("hit-rate has a blind spot: it only checks whether <i>at least one</i> right page "
     "showed up. But some questions need <b>several</b> pages to answer fully. For those, "
     "<b>recall@k = the fraction of the needed pages that were found</b>. If a question needs "
     "2 pages and you found 1, recall = 0.5 &mdash; honest about the half-miss that hit-rate "
     "would have scored as a full success.")
proj("One of our questions needed both a Storage page and a security page. hit-rate called "
     "it a success (it found one); recall@5 scored it 0.50 (it found only one of two). recall "
     "exposed that the answer would be missing half its context.")
sec("precision@k and MRR")
para("<b>precision@k</b> asks the opposite of recall: of the pages you retrieved, what "
     "fraction were actually relevant? It measures noise. recall asks &quot;did I get "
     "everything I needed?&quot;; precision asks &quot;did I get <i>only</i> what I "
     "needed?&quot; They trade off.")
para("<b>MRR (Mean Reciprocal Rank)</b> rewards getting the right page <i>near the top</i>. "
     "If the correct page is always rank 1, MRR = 1.0; if it is usually rank 2, MRR is about "
     "0.5. It captures ranking quality, which plain hit-rate ignores.")
warn("Hit-rate / recall are RETRIEVAL metrics. They tell you the right info reached the "
     "model &mdash; they do NOT tell you the final answer was correct. They are the ceiling "
     "on correctness, not correctness itself. A good answer still needs the generation step "
     "to do its job.")

# ===== CH6 =====
chapter(6, "Generation Metrics: the LLM-as-Judge")
para("Grading the ANSWER step is harder, because there are many valid ways to phrase a "
     "correct answer &mdash; exact text-matching would fail good answers. And you cannot "
     "hand-grade hundreds of answers every time you make a change.")
para("The standard solution is <b>LLM-as-judge</b>: you use a second language model as an "
     "automatic grader. One model writes the answer; a different model marks it, the way an "
     "experienced teacher marks an essay against a rubric.")
sec("What the judge is given")
para("For each answer, the judge receives a grading packet: the question, the gold answer "
     "(the key facts), the retrieved passages the system was given, and the system's actual "
     "answer. Then it returns a simple verdict.")
code('# the judge is asked to return a small JSON verdict, e.g.\n'
     '{ "correctness": "correct" | "partial" | "wrong",\n'
     '  "faithfulness": "grounded" | "unsupported",\n'
     '  "reason": "one short sentence" }')
proj("We had the system answer with Claude Opus, and used a cheaper, faster model (Claude "
     "Sonnet) as the judge. Using a separate, cheaper grader is a normal, defensible pattern "
     "&mdash; the grader does not have to be the same model as the system under test.")
para("Finally we turn the verdicts into numbers (correct = 1, partial = 0.5, wrong = 0) and "
     "average them into scores like &quot;correctness 81%.&quot;")

# ===== CH7 =====
chapter(7, "Correctness vs Faithfulness")
para("For answerable questions we grade two <i>different</i> things, and the difference "
     "matters enormously.")
para("<b>Correctness</b> asks: did the answer get the facts right (match the gold answer)?")
para("<b>Faithfulness</b> (also called groundedness) asks: is every claim in the answer "
     "actually supported by the retrieved passages &mdash; or did the model add things from "
     "its own memory?")
para("An answer can pass one and fail the other, which is why we never merge them:")
simple_table([["Case", "Meaning", "Why it is dangerous"],
              ["Correct but unsupported", "right answer, but from the model's memory not the docs",
               "next time the docs change, it won't notice &mdash; may confidently go wrong"],
              ["Faithful but wrong", "stuck to the docs but still answered poorly",
               "the docs may not have contained the real answer"]],
             [4.3 * cm, 6.0 * cm, 5.2 * cm])
plain("Correctness = did you get the right answer. Faithfulness = did you get it from the "
      "source you were given, or did you make it up. A support bot that is correct by luck "
      "today can be confidently wrong tomorrow &mdash; so we insist on both.")

# ===== CH8 =====
chapter(8, "Validate the Grader (Eval Tooling Has Bugs Too)")
para("Here is the lesson the week kept teaching: <b>the grader is itself a program (and, for "
     "the judge, itself an AI), so it can be wrong &mdash; and a broken grader is worse than "
     "no grader, because it gives you false confidence.</b>")
para("We hit this three times:")
para("&bull; An analysis script once scored <i>every</i> answer as a refusal, because it "
     "searched the whole result block (which contained our own annotation text) instead of "
     "just the answer. A keyword false-positive.")
para("&bull; The faithfulness score came out at 38% &mdash; suspiciously low for a system we "
     "designed to be grounded. The cause was a bug in the grader: we showed the judge only "
     "part of the retrieved context, so it marked supported claims &quot;unsupported.&quot; "
     "After fixing it, faithfulness rose to no violations found.")
para("&bull; A single &quot;escalation accuracy&quot; number averaged together two unrelated "
     "groups of questions, producing a misleading 50%.")
warn("The discipline: distrust the number, read the judge's REASONS, and hand-check a few "
     "verdicts before trusting the aggregate. In production you go further &mdash; you "
     "periodically compare the judge against human labels and track their agreement, because "
     "judges drift and have biases.")
plain("If you only remember one sentence from this chapter: a number you have not validated "
      "is not evidence &mdash; it is decoration.")

# ===== CH9 =====
chapter(9, "Safety Evaluation")
para("Evaluation is not only about accuracy &mdash; it is also how you catch <b>dangerous</b> "
     "behaviour before a user does. Some test questions are deliberately ones the system "
     "should <i>refuse</i>: account/billing requests, and destructive or harmful actions.")
proj("Our most valuable single finding: asked &quot;delete my entire production "
     "database,&quot; the system retrieved a deletion document and helpfully replied with "
     "actual DROP TABLE commands. A support bot must never do that. We added a <b>safety "
     "guardrail</b> to the system prompt: decline destructive, account-specific, or "
     "action-taking requests regardless of what was retrieved. After the fix it refuses and "
     "escalates to a human.")
para("The general principle: a safety rule must <b>override the retrieved context</b>. It is "
     "not enough to answer from the docs &mdash; sometimes the right behaviour is to refuse "
     "even though a relevant-looking document exists. These refusal cases belong permanently "
     "in your golden set so a future change can never silently re-open the hole.")

# ===== CH10 =====
chapter(10, "The Chunk-Size Experiment (and the Vanity-Metric Trap)")
para("A natural assumption is &quot;bigger chunks give more correct answers.&quot; It is not "
     "true in general &mdash; chunk size is a <b>tradeoff</b>, and it affects the two steps in "
     "opposite directions.")
para("<b>Small chunks</b> make the FIND step sharper: a small chunk is one tight idea, so its "
     "meaning-vector is specific and matches precisely. But too-small chunks starve the "
     "ANSWER step of context. <b>Big chunks</b> carry more context but blur the FIND step "
     "(one vector averages many ideas), add noise, suffer &quot;lost in the middle,&quot; and "
     "cost more tokens.")
proj("We measured chunk sizes 256, 512, and 1024 on the same golden set. 256 was clearly "
     "worse. 1024 improved hit-rate@1 (54% to 62%) &mdash; the tempting &quot;win.&quot; But "
     "recall@5 and hit@5 were IDENTICAL to 512. Since the generator consumes the top 5, 1024 "
     "handed the model the <i>same documents</i> &mdash; it only reshuffled ranking, while "
     "costing more tokens. We did NOT adopt it.")
warn("A vanity metric is a number that moves without improving the outcome you care about. "
     "hit-rate@1 went up, but the metric that actually feeds the generator (recall@5) did "
     "not. The real bottleneck was the ~23% of questions whose document never reached the top "
     "5 at all &mdash; and chunk size did not fix that.")
sec("The senior fix: parent-document retrieval")
para("The elegant way to escape the small-vs-big tradeoff is <b>parent-document (small-to-"
     "big) retrieval</b>: search using small chunks for precision, but feed the model the "
     "larger parent section they came from for context. You get sharp matching <i>and</i> "
     "full context. The honest conclusion of our experiment was that the next real lever is "
     "smarter retrieval (this, or hybrid keyword+vector search), not chunk size.")

# ===== CH11 =====
chapter(11, "Evaluation in Production (the Senior View)")
para("Everything so far is <b>offline evaluation</b> &mdash; a fixed test set you control. "
     "Production adds <b>online evaluation</b> &mdash; live traffic you do not control. The "
     "whole challenge is the gap between them. A senior engineer designs a <i>system</i> for "
     "this, not a single check.")
sec("The hard problems, and how they are resolved")
para("&bull; <b>No ground truth at scale.</b> You cannot hand-label thousands of live "
     "queries. Resolution: a small curated regression set for gating, plus sampling, plus "
     "reference-free metrics.")
para("&bull; <b>No reference answer online.</b> Correctness needs a gold answer; live queries "
     "have none. Resolution: <b>reference-free</b> signals &mdash; faithfulness (answer vs "
     "retrieved context, always available), citation coverage, and user signals (thumbs, "
     "rephrasing, escalation).")
para("&bull; <b>The judge drifts and is biased.</b> Resolution: pin the judge model version, "
     "calibrate it against human labels periodically, track judge-human agreement.")
para("&bull; <b>Cost and latency.</b> You cannot judge 100% of traffic. Resolution: sample a "
     "few percent, judge asynchronously off the user's latency path, use cheap triage models, "
     "use batch APIs.")
para("&bull; <b>Distribution shift.</b> Real users ask things your test set never imagined. "
     "Resolution: mine production logs and fold new patterns and every new bug back into the "
     "regression set.")
para("&bull; <b>Offline metrics do not equal business outcomes.</b> Resolution: tie metrics "
     "to real KPIs (deflection rate, escalation rate, satisfaction) and confirm changes with "
     "A/B tests in production.")
para("&bull; <b>Silent degradation</b> (a provider model update, index drift). Resolution: "
     "continuous monitoring dashboards with drift alerts, plus full trace logging.")
para("&bull; <b>Privacy.</b> Live queries contain personal data. Resolution: redact before "
     "logging or judging, enforce retention limits, keep evaluation inside the approved data "
     "boundary.")
sec("The layered architecture")
code("1. CI eval gate        regression set + safety cases; blocks bad deploys   (pre-ship)\n"
     "2. Canary / shadow     new version on a traffic slice; compare            (at ship)\n"
     "3. Online sampling     judge ~2% of live traffic, reference-free          (continuous)\n"
     "4. Production monitor   dashboards + drift alerts on KPIs                  (continuous)\n"
     "5. Human-in-the-loop    label a sample; calibrate the judge; mine bugs     (periodic)\n"
     "6. A/B testing          prove changes move business KPIs                   (per change)")
para("The loop is the point: production failures become labelled examples become regression "
     "tests. The evaluation system <i>learns from production.</i> And there is never one "
     "number &mdash; you pick a primary metric with <b>guardrails</b> (for example, optimise "
     "deflection but never regress the safety gate).")

# ===== CH12 =====
chapter(12, "Our Results, Lessons, and Glossary")
sec("The numbers we ended with")
simple_table([["Metric", "Result"],
              ["Retrieval hit-rate@1 / @3 / @5", "54% / 69% / 77%"],
              ["Retrieval recall@5", "73%"],
              ["Retrieval MRR", "0.63"],
              ["Generation correctness", "~81%"],
              ["Generation faithfulness", "no violations found (n=13)"],
              ["Critical escalation (account / destructive)", "4 / 4"]],
             [9.5 * cm, 6.0 * cm])
sec("The lessons that outlast the numbers")
para("&bull; Measure retrieval and generation <b>separately</b> &mdash; they fail "
     "differently.")
para("&bull; A retrieval metric is the <b>ceiling</b> on correctness, not correctness "
     "itself.")
para("&bull; Use <b>recall</b>, not just hit-rate, when answers span multiple pages.")
para("&bull; <b>Validate the grader</b> &mdash; ours was wrong before our system was, three "
     "times.")
para("&bull; Watch for <b>vanity metrics</b> &mdash; a number can move without improving the "
     "outcome.")
para("&bull; Safety rules must <b>override</b> retrieval; refusal cases live in the golden "
     "set forever.")
para("&bull; In production, evaluation is a <b>layered system with a feedback loop</b>, tied "
     "to business outcomes.")
sec("Glossary")
for term, d in [
    ("Ground truth", "the known-correct answer you grade against."),
    ("Golden set", "your collection of test questions plus their ground truth."),
    ("Retrieval", "the FIND step &mdash; searching the docs for relevant passages."),
    ("Generation", "the ANSWER step &mdash; the model writing an answer from those passages."),
    ("hit-rate@k", "fraction of questions where the right page is in the top k (counted once)."),
    ("recall@k", "fraction of the needed pages that were found in the top k."),
    ("precision@k", "fraction of retrieved pages that were actually relevant."),
    ("MRR", "mean reciprocal rank &mdash; how high the right page ranked on average."),
    ("LLM-as-judge", "using a second model to grade the system's answers."),
    ("Correctness", "did the answer get the facts right?"),
    ("Faithfulness", "is every claim supported by the retrieved context (no making things up)?"),
    ("Reference-free metric", "a quality signal that needs no gold answer (e.g. faithfulness)."),
    ("Vanity metric", "a number that improves without improving the real outcome."),
    ("Regression set", "a fixed test set run on every change to catch breakages."),
]:
    story.append(Paragraph(f"<b>{esc(term)}</b> &mdash; {d}",
                           ParagraphStyle("g", parent=body, spaceAfter=4)))

story.append(Spacer(1, 14))
story.append(Paragraph("End of book. The real skill you built this week was not any single "
                       "metric &mdash; it was the judgment to distrust a number until you "
                       "understand how it was produced.",
                       ParagraphStyle("end", parent=body, fontName="Helvetica-Oblique",
                                      textColor=ACCENT2)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "Evaluating RAG Systems")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                      topMargin=2.2 * cm, bottomMargin=2.2 * cm)
doc.addPageTemplates([PageTemplate(id="all",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")],
    onPage=footer)])
doc.build(story)
print("WROTE", OUT)
