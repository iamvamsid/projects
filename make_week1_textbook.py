"""Generate a descriptive textbook-style PDF on LLM API Foundations (Week 1)."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted,
    Spacer, PageBreak, Table, TableStyle,
)

OUT = "/Users/vamsidhar/Google/ai-journey/notes/llm-api-foundations-textbook.pdf"

ACCENT = colors.HexColor("#243b73")
ACCENT2 = colors.HexColor("#3a5599")
CODEBG = colors.HexColor("#f2f3f7")
PROJBG = colors.HexColor("#eceff6")
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
                         fontSize=28, leading=33, textColor=ACCENT, alignment=TA_CENTER)
subst = ParagraphStyle("sub", parent=body, fontSize=14, leading=20,
                       alignment=TA_CENTER, textColor=colors.HexColor("#555"))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


story = []


def CODE(text):
    rows = [[Preformatted(text.strip("\n"), codest)]]
    t = Table(rows, colWidths=[16.0 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CODEBG),
                           ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d2d6e2")),
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
def proj(t): story.extend(boxflow(t, PROJBG, "IN OUR JOURNEY", ACCENT2))
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
story.append(Paragraph("Working with LLM APIs", titlest))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("The Foundations Every AI Engineer Needs", subst))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("Messages, streaming, system prompts, caching, tool use,<br/>"
                       "structured outputs, and adaptive thinking &mdash; every<br/>"
                       "concept from Week 1, explained in plain words.", subst))
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("Foundations for the AI Journey", subst))

# ===== TOC =====
story.append(PageBreak())
story.append(Paragraph("Contents", h1))
for item in [
    "1.  Talking to a Model: the Messages API",
    "2.  Tokens, and Why They Are the Unit of Everything",
    "3.  Streaming",
    "4.  System Prompts",
    "5.  Prompt Caching",
    "6.  Tool Use (a.k.a. Function Calling)",
    "7.  Structured Outputs",
    "8.  Adaptive Thinking and Effort",
    "9.  Choosing the Right Model",
    "10. Strategy: Picking a Domain (the FDE Lens)",
    "11. Eval-First: Golden Questions Before Code",
    "12. Glossary",
]:
    story.append(Paragraph(esc(item), tocst))

# ===== CH1 =====
chapter(1, "Talking to a Model: the Messages API")
para("Everything you build on top of a large language model starts with one kind of call: you "
     "send a list of <b>messages</b>, you get a reply. With the Anthropic SDK it looks like "
     "this:")
code('import anthropic\n'
     'client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment\n\n'
     'resp = client.messages.create(\n'
     '    model="claude-opus-4-8",\n'
     '    max_tokens=1024,\n'
     '    messages=[{"role": "user", "content": "Explain RAG in one paragraph."}],\n'
     ')\n'
     'print(resp.content[0].text)')
para("The pieces: <b>model</b> chooses which brain answers; <b>max_tokens</b> caps how long the "
     "reply can be; <b>messages</b> is the conversation so far, each item tagged with a "
     "<b>role</b> (user or assistant). The API is <i>stateless</i> &mdash; it remembers nothing "
     "between calls, so to hold a conversation you send the whole history back every time.")
plain("One call = here is the conversation so far, please add the next turn. The model has no "
      "memory of its own; you carry the history.")
proj("In Week 1 we wrote tiny hello-world scripts against both Anthropic (Claude) and OpenAI "
     "(GPT) to build muscle memory for this single call shape &mdash; it underpins everything "
     "else.")

# ===== CH2 =====
chapter(2, "Tokens, and Why They Are the Unit of Everything")
para("Models do not read characters or words &mdash; they read <b>tokens</b>, chunks of text "
     "roughly four characters long (about three-quarters of a word). &quot;Row level "
     "security&quot; is a handful of tokens.")
para("Tokens matter because they are the unit of <b>cost</b> and <b>limits</b>. You pay per "
     "million input tokens and per million output tokens; the <b>context window</b> is the "
     "maximum tokens a model can consider at once. Everything you send &mdash; system prompt, "
     "history, retrieved documents &mdash; spends from that budget.")
warn("A rough rule of thumb is ~4 characters per token, but it is only an estimate. For real "
     "counts use the provider's token-counting endpoint, not a guess &mdash; and never use one "
     "provider's tokenizer to estimate another's.")

# ===== CH3 =====
chapter(3, "Streaming")
para("By default a call waits until the entire reply is finished, then returns it. With "
     "<b>streaming</b>, the model sends the reply token-by-token as it is generated, so the "
     "user sees words appear immediately instead of staring at a spinner.")
code('with client.messages.stream(\n'
     '    model="claude-opus-4-8", max_tokens=1024,\n'
     '    messages=[{"role": "user", "content": "Write a short story."}],\n'
     ') as stream:\n'
     '    for text in stream.text_stream:\n'
     '        print(text, end="", flush=True)')
para("Streaming does not make the model faster overall, but it dramatically improves the "
     "<i>perceived</i> speed, and it avoids connection time-outs on long replies. For anything "
     "user-facing or long, stream.")

# ===== CH4 =====
chapter(4, "System Prompts")
para("The <b>system prompt</b> is a separate instruction that sets the model's role, "
     "behaviour, and rules for the whole conversation &mdash; distinct from the user's actual "
     "question.")
code('client.messages.create(\n'
     '    model="claude-opus-4-8", max_tokens=1024,\n'
     '    system="You are a support assistant. Answer only from the provided context.",\n'
     '    messages=[{"role": "user", "content": "..."}],\n'
     ')')
sec("Does a system prompt cost extra? (a question we actually asked)")
para("A system prompt improves quality and consistency &mdash; persona, constraints, output "
     "format. But its tokens are billed exactly like any other input tokens, so it does not "
     "<i>reduce</i> cost; it slightly adds to it. Moving an instruction from the user message "
     "into the system prompt is cost-neutral.")
plain("System prompt = the standing rules for the whole chat. Same token price as anything "
      "else &mdash; it buys quality, not savings.")

# ===== CH5 =====
chapter(5, "Prompt Caching")
para("If you send the same large block of text on many calls &mdash; a big system prompt, or a "
     "fixed knowledge context &mdash; <b>prompt caching</b> lets the provider remember it so "
     "you are not charged full price to re-process it every time.")
para("You mark a stable block as cacheable; repeated calls then read it from cache at roughly "
     "one-tenth the input price, and faster. The catch: it is a <b>prefix match</b> &mdash; any "
     "change to the cached part (even a timestamp) invalidates it, and the block has to be large "
     "enough to be worth caching.")
proj("This is directly relevant to RAG: the system prompt plus retrieved context can be "
     "thousands of tokens reused on every query &mdash; the textbook caching win, and a strong "
     "cost-control talking point (&quot;I cut per-query cost by caching the static context&quot;).")
warn("Caching saves money only when the cached block is stable and reused. Put volatile things "
     "(the user's question, timestamps) AFTER the cached part, never inside it.")

# ===== CH6 =====
chapter(6, "Tool Use (a.k.a. Function Calling)")
para("On its own a model can only produce text. <b>Tool use</b> (OpenAI calls it function "
     "calling &mdash; same idea, different name) lets the model ask your program to run a "
     "function and hand back the result. This is how an AI looks something up, checks an order, "
     "or takes an action.")
para("You describe the tools (name, description, input shape). When the model decides it needs "
     "one, it does not run it &mdash; it returns a structured request saying &quot;please call "
     "get_weather with location=Paris.&quot; <i>Your</i> code runs it and sends the result "
     "back; the model continues with that information.")
code('tools = [{\n'
     '    "name": "get_order_status",\n'
     '    "description": "Look up the status of a customer order by id.",\n'
     '    "input_schema": {\n'
     '        "type": "object",\n'
     '        "properties": {"order_id": {"type": "string"}},\n'
     '        "required": ["order_id"],\n'
     '    },\n'
     '}]')
plain("The model never runs anything itself. It says what it wants done; your code does it and "
      "reports back. That request-result loop is the whole foundation of AI agents.")
proj("This is the backbone of Project 2 (the agent): the support assistant will use tools to "
     "look things up and act, not just answer from text.")

# ===== CH7 =====
chapter(7, "Structured Outputs")
para("Normally a model replies in free-form prose. Often you need a <b>guaranteed shape</b> "
     "&mdash; valid JSON with specific fields &mdash; so your program can read it reliably. "
     "<b>Structured outputs</b> constrain the reply to a schema you define.")
code('resp = client.messages.create(\n'
     '    model="claude-opus-4-8", max_tokens=1024,\n'
     '    output_config={"format": {"type": "json_schema", "schema": {\n'
     '        "type": "object",\n'
     '        "properties": {"sentiment": {"type": "string"},\n'
     '                       "score": {"type": "number"}},\n'
     '        "required": ["sentiment", "score"],\n'
     '        "additionalProperties": False}}},\n'
     '    messages=[{"role": "user", "content": "Classify: I love this product."}],\n'
     ')')
para("This matters enormously for evaluation and pipelines: when you ask a model to grade an "
     "answer or extract data, you want a clean JSON verdict you can parse, not a paragraph. We "
     "lean on this heavily when building the eval judge.")

# ===== CH8 =====
chapter(8, "Adaptive Thinking and Effort")
para("Modern models can <b>think before answering</b> &mdash; produce a private chain of "
     "reasoning, then write the final reply. Two controls govern this, and they are easy to "
     "confuse.")
sec("Adaptive thinking &mdash; how much to reason")
para("<b>Adaptive thinking</b> lets the model decide, per request, whether and how much to "
     "think. A trivial question gets little; a multi-step problem gets more. You no longer pick "
     "a fixed budget &mdash; the model adapts.")
code('client.messages.create(\n'
     '    model="claude-opus-4-8", max_tokens=2000,\n'
     '    thinking={"type": "adaptive"},\n'
     '    output_config={"effort": "high"},   # low | medium | high | xhigh | max\n'
     '    messages=[{"role": "user", "content": "..."}],\n'
     ')')
sec("Effort &mdash; the master dial")
para("<b>Effort</b> sets how hard the model works overall &mdash; both how deep its thinking "
     "may go AND how much it does (tool calls, thoroughness, verbosity). Adaptive thinking "
     "varies within the band that effort sets.")
simple_table([["", "Who decides", "What it controls"],
              ["Effort", "you (fixed per call)", "the ceiling: how hard it works, thinking + acting"],
              ["Adaptive thinking", "the model (per request)", "where inside that band a given question lands"]],
             [3.6 * cm, 4.6 * cm, 7.3 * cm])
plain("Effort is the manager setting the budget; adaptive thinking is the worker spending "
      "wisely within it. Effort sets the band; adaptive picks the point inside it &mdash; and "
      "effort also governs tool-use and verbosity, which thinking does not.")
proj("A real cost lever for our support bot: use low effort for simple FAQ lookups and high "
     "effort for hard multi-document questions &mdash; route effort by difficulty.")

# ===== CH9 =====
chapter(9, "Choosing the Right Model")
para("Providers offer a ladder of models trading intelligence against speed and cost. The "
     "engineering skill is matching the model to the job, not always reaching for the biggest.")
simple_table([["Tier", "Good for"],
              ["Largest / most capable", "hard reasoning, agents, correctness-critical work"],
              ["Mid (balanced)", "high-volume production, summarization, most tasks"],
              ["Smallest / fastest", "simple, latency-sensitive, cheap classification"]],
             [5.5 * cm, 10.0 * cm])
para("A common production pattern is to mix them: a cheap model for simple or high-volume "
     "steps, a powerful one where correctness matters. We later use a cheaper model as our "
     "evaluation judge while a top model answers &mdash; same idea.")
warn("Use exact model identifiers from the provider's current list; never guess or append "
     "made-up date suffixes, or the call will fail. Defaults and capabilities change, so check "
     "the current docs rather than relying on memory.")

# ===== CH10 =====
chapter(10, "Strategy: Picking a Domain (the FDE Lens)")
para("Week 1 was not only technical &mdash; the highest-leverage decision was choosing what "
     "<b>domain</b> to build in. The technology is similar across domains; the <i>story</i> is "
     "not.")
para("The guiding lens was the <b>Forward Deployed Engineer (FDE)</b> framing: prefer an "
     "enterprise/business-flavoured domain where a real buyer (a CTO, a VP) can see themselves "
     "as the customer. The same RAG code is a far stronger portfolio piece as &quot;ticket "
     "deflection for a B2B SaaS&quot; than as &quot;ask questions about Wikipedia.&quot;")
proj("We chose Customer Support / Internal Knowledge, flavour B2B SaaS support &mdash; the most "
     "common real Applied-AI / FDE deployment, and the easiest to demo to a non-technical "
     "executive. We deliberately declined a flashier consumer idea (an AI tutor) because it "
     "weakens the enterprise narrative.")
plain("Pick a domain a business would pay for, that you can demo to an executive in one "
      "sentence. The buyer story matters as much as the code.")

# ===== CH11 =====
chapter(11, "Eval-First: Golden Questions Before Code")
para("The most counter-intuitive habit from Week 1: before writing a single line of retrieval "
     "code, we wrote down the questions the system must answer correctly &mdash; the "
     "<b>golden questions</b>.")
para("This sounds backwards, but it is the discipline that makes everything later measurable. "
     "If you do not decide up front what &quot;good&quot; looks like, you will grade the system "
     "on vibes. Writing the test before the system forces clarity about the goal &mdash; and "
     "becomes the foundation for real evaluation in Week 3.")
plain("Write the exam before you teach the class. You cannot fix what you cannot measure, and "
      "you cannot measure without deciding the right answers in advance.")

# ===== CH12 =====
chapter(12, "Glossary")
for term, d in [
    ("Token", "the model's unit of text (~4 characters); the unit of cost and limits."),
    ("Context window", "the maximum tokens a model can consider at once."),
    ("Messages API", "the core call: send a list of role-tagged messages, get a reply."),
    ("Role", "who a message is from: user or assistant (and the separate system prompt)."),
    ("Stateless", "the API remembers nothing between calls; you resend the history."),
    ("Streaming", "receiving the reply token-by-token as it is generated."),
    ("System prompt", "standing instructions/persona for the whole conversation."),
    ("Prompt caching", "reusing a stable text block cheaply across many calls."),
    ("Tool use / function calling", "the model requests your code run a function and return a result."),
    ("Structured output", "constraining the reply to a defined JSON schema."),
    ("Adaptive thinking", "the model decides per request how much to reason."),
    ("Effort", "the dial for how hard the model works overall (thinking + acting)."),
    ("FDE", "Forward Deployed Engineer &mdash; embeds with customers to deploy AI into their world."),
    ("Golden questions", "the test set written before the system, defining what good looks like."),
]:
    story.append(Paragraph(f"<b>{esc(term)}</b> &mdash; {d}",
                           ParagraphStyle("g", parent=body, spaceAfter=4)))

story.append(Spacer(1, 14))
story.append(Paragraph("End of book. With these foundations in hand, the next volume builds the "
                       "system &mdash; see Building a RAG System.",
                       ParagraphStyle("end", parent=body, fontName="Helvetica-Oblique",
                                      textColor=ACCENT2)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "Working with LLM APIs")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                      topMargin=2.2 * cm, bottomMargin=2.2 * cm)
doc.addPageTemplates([PageTemplate(id="all",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")],
    onPage=footer)])
doc.build(story)
print("WROTE", OUT)
