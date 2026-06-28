"""Week 7 booklet: Memory & Observability — Making an Agent Operable."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted,
    Spacer, PageBreak, Table, TableStyle,
)

OUT = "/Users/vamsidhar/Google/ai-journey/notes/memory-and-observability-week-7.pdf"

ACCENT = colors.HexColor("#a8541a")
ACCENT2 = colors.HexColor("#c46a2a")
CODEBG = colors.HexColor("#f7f3ef")
PROJBG = colors.HexColor("#f6efe8")
PLAINBG = colors.HexColor("#e9f5ee")
WARNBG = colors.HexColor("#fdeee4")

styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=8)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=20, leading=24, textColor=ACCENT, spaceAfter=12)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=13.5, leading=18, textColor=ACCENT2, spaceBefore=12, spaceAfter=6)
codest = ParagraphStyle("code", parent=styles["Code"], fontName="Courier",
                        fontSize=8.0, leading=10.5, textColor=colors.HexColor("#222"))
chapno = ParagraphStyle("chapno", parent=body, fontName="Helvetica-Bold",
                        fontSize=11, textColor=ACCENT2, spaceAfter=2)
tocst = ParagraphStyle("toc", parent=body, fontSize=11, leading=18, spaceAfter=2)
titlest = ParagraphStyle("title", parent=styles["Title"], fontName="Helvetica-Bold",
                         fontSize=25, leading=30, textColor=ACCENT, alignment=TA_CENTER)
subst = ParagraphStyle("sub", parent=body, fontSize=14, leading=20,
                       alignment=TA_CENTER, textColor=colors.HexColor("#555"))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


story = []


def CODE(text):
    rows = [[Preformatted(text.strip("\n"), codest)]]
    t = Table(rows, colWidths=[16.0 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CODEBG),
                           ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0d3c6")),
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
    story.append(Paragraph(f"SECTION {num}", chapno))
    story.append(Paragraph(esc(title), h1))


def sec(t): story.append(Paragraph(esc(t), h2))
def para(t): story.append(Paragraph(t, body))
def code(t): story.append(CODE(t)); story.append(Spacer(1, 6))
def proj(t): story.extend(boxflow(t, PROJBG, "OUR RUN", ACCENT2))
def plain(t): story.extend(boxflow(t, PLAINBG, "IN PLAIN WORDS", colors.HexColor("#3a9c6a")))
def warn(t): story.extend(boxflow(t, WARNBG, "WATCH OUT", colors.HexColor("#d98841")))


def simple_table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ACCENT2),
                           ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                           ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                           ("FONTSIZE", (0, 0), (-1, -1), 8.5), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 5),
                           ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    story.append(t); story.append(Spacer(1, 8))


# ===== COVER =====
story.append(Spacer(1, 4.5 * cm))
story.append(Paragraph("Memory &amp; Observability", titlest))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Making an Agent Operable", subst))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("Week 6 made the agent robust &mdash; it doesn't break. Week 7<br/>"
                       "makes it operable: it remembers across turns, and every run<br/>"
                       "leaves a complete record of what it did, what it cost, and why.", subst))
story.append(Spacer(1, 3.3 * cm))
story.append(Paragraph("Project 2 &bull; Week 7", subst))
story.append(Paragraph("Companion to project-02-agent-saas-support", subst))

# ===== TOC =====
story.append(PageBreak())
story.append(Paragraph("Contents", h1))
for item in [
    "1.  Robust vs. Operable",
    "2.  Memory: From One-Shot to Conversation",
    "3.  The Trap: Bounding Memory Without Breaking It",
    "4.  Observability: Why a Trace Exists",
    "5.  Building the Trace by Hand",
    "6.  The Three Vitals: Tokens, Cost, Latency",
    "7.  The Trace Viewer",
    "8.  Hand-Rolled vs. a Framework",
    "9.  Glossary",
]:
    story.append(Paragraph(esc(item), tocst))

# ===== 1 =====
chapter(1, "Robust vs. Operable")
para("Week 6 made the agent <b>robust</b>: it picks the right tool, chains tools when a "
     "question needs several, and fails gracefully instead of crashing or hallucinating. "
     "That's a big deal &mdash; but it's not enough to put in front of a customer at scale. "
     "The moment an agent runs in production, a different set of questions takes over, and "
     "none of them are about correctness:")
para("&bull; The customer asked three things in a row &mdash; why is the agent re-asking "
     "for their account every time?<br/>"
     "&bull; Which step was slow? Why did it call <i>that</i> tool? How much did that run "
     "cost? Where did it go wrong?")
para("Week 7 answers both. <b>Memory</b> lets the agent hold a conversation. "
     "<b>Observability</b> lets you see exactly what it did, what it cost, and why. Together "
     "they take the agent from &lsquo;works in a demo&rsquo; to &lsquo;operable in production&rsquo;.")
plain("Robust = it doesn't break. Operable = when something does go wrong, you can see "
      "what happened and fix it. The first question in any real deployment is &lsquo;how do "
      "we debug this in prod?&rsquo; &mdash; that's what this week builds.")

# ===== 2 =====
chapter(2, "Memory: From One-Shot to Conversation")
para("Until now, every question started fresh. The agent's <b>run()</b> built a brand-new "
     "list of messages, answered once, and threw the history away. Fine for one-shot Q&amp;A, "
     "useless for a real support chat &mdash; where &lsquo;does <i>it</i> include SSO?&rsquo; "
     "depends on &lsquo;what plan am I on?&rsquo; from the turn before.")
para("The fix is small but important: a <b>Conversation</b> object that <i>owns</i> the "
     "messages list and keeps it across turns. Each <b>.send()</b> is one turn appended to "
     "the same history. That persistent list <i>is</i> the memory &mdash; because we re-send "
     "the whole conversation every time, the model always has the context.")
code("class Conversation:\n"
     "    def __init__(self):\n"
     "        self.messages = []          # survives across .send() calls = MEMORY\n"
     "    def send(self, user_input):\n"
     "        self.messages.append({'role':'user', 'content': user_input})\n"
     "        # ... run the tool loop on self.messages ...\n"
     "        self.messages.append({'role':'assistant', 'content': answer})  # remember the reply too")
para("Two details make it work. First, we append the agent's <b>own answer</b> back into "
     "history &mdash; otherwise the next turn wouldn't know what was already said. Second, "
     "the loop guard resets <b>per turn</b>: re-calling get_account_status in a later turn is "
     "perfectly legitimate, not a stuck loop.")
proj("A 3-turn demo proved it. T1: &lsquo;What plan is acct_123 on?&rsquo; &rarr; Pro. "
     "T2: &lsquo;Does <i>it</i> include SSO?&rsquo; &mdash; the agent knew &lsquo;it&rsquo; = "
     "the Pro plan and looked up its features WITHOUT re-asking for the account. "
     "T3: &lsquo;And an SLA?&rsquo; &mdash; answered straight from memory with ZERO tool calls, "
     "because the plan's features were already in the conversation.")

# ===== 3 =====
chapter(3, "The Trap: Bounding Memory Without Breaking It")
para("Memory has a cost. Every turn re-sends the <i>entire</i> history, so tokens, money, "
     "and latency climb without limit. A 50-turn chat could cost more on turn 50 than the "
     "first ten turns combined. Unbounded memory is a production incident waiting to happen, "
     "so we cap it: keep only the most recent few turns and let old context fall off the back.")
para("But you <b>cannot</b> just &lsquo;drop the oldest messages&rsquo;. When the agent uses "
     "a tool, the history holds a <b>pair</b> joined by an id: the request (<b>tool_use</b>) "
     "and its answer (<b>tool_result</b>). The API rejects any conversation containing a "
     "tool_result whose tool_use is missing &mdash; an <b>orphaned tool_result</b>. Cut in "
     "the wrong place and the very next call crashes.")
code("# A naive trim can orphan a result:\n"
     "[user: 'what plan?']\n"
     "[assistant: tool_use t1]      <- request\n"
     "[user: tool_result t1]        <- answer (id t1)\n"
     "  -- if we drop the first two lines, the lone tool_result t1 is an ORPHAN -->\n"
     "  -- its request no longer exists -> API rejects the whole conversation")
para("The fix: only ever cut at a <b>customer-turn boundary</b> &mdash; a real message the "
     "person typed (role=user with plain text), never a tool_result turn. A customer turn "
     "always starts a fresh exchange, so a tool_use/tool_result pair is always kept or "
     "dropped together, never split.")
plain("Bounding memory isn't &lsquo;keep the last N messages&rsquo; &mdash; that would "
      "orphan tool results. It's &lsquo;keep the last N complete <i>exchanges</i>&rsquo;. "
      "Cutting on the right boundary is the entire trick.")
proj("Tested two ways. A deterministic check (no API): a 16-message history trimmed to 8, "
     "kept the last 2 customer turns, and a pairing-validator confirmed NO orphan. A live "
     "test: a cancel request mid-conversation still triggered the guardrail (refuse + "
     "escalate), and memory stayed intact afterwards. Adding state didn't weaken Week 6.")

# ===== 4 =====
chapter(4, "Observability: Why a Trace Exists")
para("The agent prints a few step-lines to the terminal and they scroll away. In production "
     "that's nothing. When a run misbehaves at 2am, you need a <b>permanent, replayable "
     "record</b> of what happened &mdash; that record is a <b>trace</b>.")
para("A trace is one run captured completely: every step, every tool call (with its input, "
     "result, and whether it errored), the token counts, and the timing &mdash; written to a "
     "file you can open later. It answers the operational questions correctness can't:")
simple_table([["Question", "Answered by"],
              ["What did the agent actually do, in order?", "the steps array"],
              ["Which tool failed, and why?", "tool_calls with is_error + result"],
              ["How many tokens did each step cost?", "input/output tokens per step"],
              ["Which step was slow?", "model_latency_ms per step"]],
             [9.0 * cm, 7.0 * cm])
plain("A run that scrolled past in the terminal is gone. A trace is the same run frozen on "
      "disk &mdash; you can read it, cost it, and debug it long after it finished.")

# ===== 5 =====
chapter(5, "Building the Trace by Hand")
para("We defined the <i>shape</i> of a trace as plain data classes &mdash; a Trace holds "
     "Steps, each Step holds ToolCalls &mdash; and instrumented the loop to fill it in as it "
     "runs. Tracing is opt-in (<b>collect_trace=True</b>), so default behaviour and the "
     "8-scenario suite are untouched.")
code("Trace { user_input, model, started_at, outcome, total_latency_ms,\n"
     "        steps: [ Step { n, stop_reason, input_tokens, output_tokens, latency,\n"
     "                        tool_calls: [ ToolCall{name, input, result, is_error, latency} ] } ],\n"
     "        final_text }")
para("The token counts come straight from the API's <b>usage</b> field &mdash; we don't "
     "estimate by counting characters; we read what we were actually billed for. Timing is a "
     "stopwatch around each model call and each tool call. One run &rarr; one JSON file under "
     "<b>traces/</b> (gitignored &mdash; these are run artifacts, not source).")
warn("Two halves of robust capture mirror Week 6's error handling: the model call and the "
     "tool call are timed and recorded separately. That separation is what later tells you "
     "whether a slow run was the model thinking or a tool waiting on a real service.")

# ===== 6 =====
chapter(6, "The Three Vitals: Tokens, Cost, Latency")
para("Raw token counts aren't actionable on their own. The point of a trace is turning them "
     "into the three numbers an operator actually watches: <b>tokens</b>, <b>cost</b>, and "
     "<b>latency</b>. Cost needs a price table; the model the run used sets the rate.")
simple_table([["Model", "Input $/1M", "Output $/1M"],
              ["claude-opus-4-8", "$5.00", "$25.00"],
              ["claude-sonnet-4-6", "$3.00", "$15.00"],
              ["claude-haiku-4-5", "$1.00", "$5.00"]],
             [7.0 * cm, 4.5 * cm, 4.5 * cm])
code("cost = input_tokens / 1e6 * input_rate  +  output_tokens / 1e6 * output_rate")
proj("A 3-step chained answer (&lsquo;does acct_123 include priority support?&rsquo;): "
     "~3,389 input / 288 output tokens, $0.024, 5.8s. Per step the input GREW: "
     "1006 -> 1130 -> 1253 &mdash; the same question costing more each step, because the "
     "whole transcript is re-sent every loop. That is exactly the cost curve the memory "
     "bound (Section 3) exists to cap.")
para("Two lessons fall straight out of the numbers. <b>Cost climbs with the conversation</b>, "
     "not with the question &mdash; long chats get quietly expensive. And <b>input dominates</b>: "
     "3,389 in vs 288 out. The lever for cost isn't shorter answers; it's shorter context "
     "(or caching). You couldn't see either of these without the trace.")

# ===== 7 =====
chapter(7, "The Trace Viewer")
para("A trace on disk is JSON &mdash; complete, but not readable. The viewer "
     "(<b>python -m src.trace_view</b>) turns one run into a readable timeline plus the "
     "one-line vitals: each step's stop-reason / tokens / cost / latency, each tool call "
     "marked with a tick or an &lsquo;ERROR&rsquo;, the final answer, and the summary.")
code("python -m src.trace_view            # the newest run, full timeline\n"
     "python -m src.trace_view <file>     # a specific run\n"
     "python -m src.trace_view --last 5   # recent runs, one line each")
proj("On an error run (acct_999, unknown), the viewer showed the tool call marked "
     "&lsquo;ERROR account_not_found&rsquo; on step 1, the model recovering into a "
     "verify-or-escalate answer on step 2, and the costed summary at the bottom. The "
     "--last listing gives a scannable operational log across many runs.")
plain("This is the payoff of the whole week, and the FDE-credible line: &lsquo;Here's ANY "
      "run my agent did &mdash; every step, what each tool returned, where it failed, what it "
      "cost, how long it took.&rsquo; That's the first thing a real deployment asks for.")

# ===== 8 =====
chapter(8, "Hand-Rolled vs. a Framework")
para("Frameworks (LlamaIndex + Arize Phoenix, Langfuse, LangSmith) give you all of this "
     "tracing in about two lines, with a clickable UI and cost computed for you. So why build "
     "it by hand? The same reason we built the agent loop three ways: to <b>understand</b> it.")
simple_table([["", "Hand-rolled (ours)", "Framework + Phoenix/Langfuse"],
              ["Code", "~50 lines you own", "~2 lines"],
              ["UI", "a JSON file + viewer", "a clickable waterfall"],
              ["Cost calc", "you write it", "built in"],
              ["You understand the data", "completely", "only if you've seen the raw form"],
              ["Lock-in", "none", "tied to the tool"]],
             [4.0 * cm, 5.5 * cm, 6.0 * cm])
para("The trade is <b>convenience and features</b> (UI, cost calc, auto-instrumentation, "
     "aggregation &mdash; all free in a framework) for <b>understanding, control, and zero "
     "lock-in</b> (you know and own every byte). Build it by hand to learn; reach for the "
     "framework in production. And because you built it by hand, the framework's trace is "
     "legible to you instead of magic.")
warn("The honest limit of hand-rolling: it only traces the code you instrumented. Switch to "
     "the framework agent or add retrieval and your trace sees none of it &mdash; "
     "auto-instrumentation hooks the framework's internals and captures everything.")

# ===== 9 =====
chapter(9, "Glossary")
for term, d in [
    ("Memory (conversation)", "keeping the messages list across turns so follow-ups have context."),
    ("Conversation / session", "an object that owns the running history; .send() is one turn."),
    ("Memory bound", "a cap (max_turns) on history so tokens/cost/latency can't grow forever."),
    ("Orphaned tool_result", "a tool answer whose tool_use was removed; the API rejects it."),
    ("Customer-turn boundary", "a real user message; the only safe place to trim history."),
    ("Trace", "a complete, replayable record of one run (steps, tools, tokens, cost, latency)."),
    ("usage field", "the API's report of input/output tokens actually billed for a call."),
    ("Cost (per MTok)", "price per million tokens; model-specific (opus-4-8 = $5 in / $25 out)."),
    ("Latency", "wall-clock time; split into model time vs tool time per step."),
    ("Observability", "being able to see, after the fact, what a system did and why."),
]:
    story.append(Paragraph(f"<b>{esc(term)}</b> &mdash; {d}",
                           ParagraphStyle("g", parent=body, spaceAfter=4)))

story.append(Spacer(1, 14))
story.append(Paragraph("End of Week 7. The agent now remembers across turns (bounded so it "
                       "can't run away) and emits a production-grade trace for every run, "
                       "viewable as a timeline with tokens, cost, and latency. Next (Week 8): "
                       "ship Project 2's three artifacts &mdash; blog, one-pager, demo video.",
                       ParagraphStyle("end", parent=body, fontName="Helvetica-Oblique",
                                      textColor=ACCENT2)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "Memory & Observability - Week 7")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                      topMargin=2.2 * cm, bottomMargin=2.2 * cm)
doc.addPageTemplates([PageTemplate(id="all",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")],
    onPage=footer)])
doc.build(story)
print("WROTE", OUT)
