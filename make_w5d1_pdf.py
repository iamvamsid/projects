"""Week 5 Day 1 booklet: From Answering to Acting (agent design)."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted,
    Spacer, PageBreak, Table, TableStyle,
)

OUT = "/Users/vamsidhar/Google/ai-journey/notes/building-agents-week-5-day-1.pdf"

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
                        fontSize=8.2, leading=11, textColor=colors.HexColor("#222"))
chapno = ParagraphStyle("chapno", parent=body, fontName="Helvetica-Bold",
                        fontSize=11, textColor=ACCENT2, spaceAfter=2)
tocst = ParagraphStyle("toc", parent=body, fontSize=11, leading=18, spaceAfter=2)
titlest = ParagraphStyle("title", parent=styles["Title"], fontName="Helvetica-Bold",
                         fontSize=27, leading=32, textColor=ACCENT, alignment=TA_CENTER)
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
def proj(t): story.extend(boxflow(t, PROJBG, "OUR DESIGN", ACCENT2))
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
story.append(Paragraph("From Answering to Acting", titlest))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Designing an AI Agent", subst))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("What an agent is, the agent loop, tools, guardrails,<br/>"
                       "and the blueprint for our support agent.", subst))
story.append(Spacer(1, 3.5 * cm))
story.append(Paragraph("Project 2 &bull; Week 5 &bull; Day 1", subst))
story.append(Paragraph("Companion to project-02-agent-saas-support", subst))

# ===== TOC =====
story.append(PageBreak())
story.append(Paragraph("Contents", h1))
for item in [
    "1.  From Answering to Acting: What an Agent Is",
    "2.  The Agent Loop",
    "3.  Tools: How a Model Reaches Beyond Text",
    "4.  Designing an Agent: the Four Decisions",
    "5.  Our Support Agent (the Blueprint)",
    "6.  Three Ways to Build the Loop",
    "7.  Glossary",
]:
    story.append(Paragraph(esc(item), tocst))

# ===== 1 =====
chapter(1, "From Answering to Acting: What an Agent Is")
para("In Project 1 we built a system that <b>answers</b>: given a question, it retrieves the "
     "relevant documents and writes a reply. Its shape was a fixed straight line &mdash; "
     "retrieve, then generate, every single time. We were always in control of the sequence.")
para("An <b>agent</b> is different. It can <b>act</b>: fetch live information, call functions, "
     "take steps &mdash; and crucially, <i>the model decides what to do at each step</i>. You "
     "no longer hand it a fixed script; you give it a goal and some tools, and it works out "
     "the sequence itself.")
plain("Project 1 answered from documents. An agent goes and DOES things &mdash; and it, not "
      "you, chooses the steps. That shift of control is what makes it an agent.")
para("This is powerful and also why agents need careful design. A system that decides its own "
     "steps can wander, loop forever, or take an action you did not intend &mdash; unless you "
     "give it a clear job, a limited set of tools, and firm guardrails. That design is exactly "
     "what Day 1 is about.")

# ===== 2 =====
chapter(2, "The Agent Loop")
para("The heart of every agent is a <b>loop</b>. Instead of one request and one reply, the "
     "model and your code go back and forth until the task is done:")
code("user message\n"
     "  -> model decides: answer directly, OR call a tool\n"
     "       -> (tool call) YOUR code runs the tool, returns the result\n"
     "            -> model continues with the result\n"
     "                 -> final answer, or another tool call ...")
para("A worked example makes it concrete:")
code('user: "What is the status of order 12345, and can I still cancel it?"\n'
     '  -> model: "I do not know order data. Call lookup_order(order_id=12345)."\n'
     '  -> your code runs it -> returns {status: "shipped", cancellable: false}\n'
     '  -> model reads that -> "Order 12345 has shipped, so it can no longer be\n'
     '                          cancelled. Here is how to start a return instead..."')
warn("The model never runs the tool itself. It only REQUESTS the call; your code executes it "
     "and hands back the result. That separation is what lets you stay in control &mdash; you "
     "decide what a tool actually does, and you can refuse or confirm risky ones.")
plain("An agent is a conversation that pauses to look things up. The model asks for "
      "information, your code fetches it, the model carries on &mdash; round and round until "
      "it can finish.")

# ===== 3 =====
chapter(3, "Tools: How a Model Reaches Beyond Text")
para("On its own a model can only produce text. A <b>tool</b> (the same idea as "
     "&quot;function calling&quot;) is a function you expose to the model so it can reach "
     "beyond text &mdash; look up an account, search docs, check inventory.")
para("You describe each tool with a <b>name</b>, a <b>description</b> (the model reads this to "
     "decide WHEN to use it), and an <b>input schema</b> (the exact arguments it expects). "
     "Good descriptions matter: a vague one makes the model call the tool at the wrong time.")
code('name: get_account_status\n'
     'description: Look up a customer\'s account status (plan, billing state,\n'
     '             active incidents) by account id. Use when the question depends\n'
     '             on the customer\'s specific account, not on general docs.\n'
     'input: { account_id: string (required) }')
plain("A tool is just a function with a label the model can read. The description is you "
      "telling the model, in words, exactly when to reach for it.")

# ===== 4 =====
chapter(4, "Designing an Agent: the Four Decisions")
para("Before any code, a good agent design answers four questions. Skipping this is why "
     "agents wander.")
simple_table([["Decision", "The question it answers"],
              ["The job", "What workflow is this agent for?"],
              ["The tools", "What can it actually DO? (start with one)"],
              ["The guardrails", "What must it never do without checking?"],
              ['"Done"', "How does it know the task is finished?"]],
             [4.0 * cm, 11.5 * cm])
para("<b>Start with one tool.</b> It is tempting to give an agent many capabilities at once, "
     "but a single-tool agent whose loop you fully understand is worth far more than a "
     "multi-tool agent that tangles. Add tools only once the basic loop is rock solid.")
warn("Guardrails are a Day-1 decision, not an afterthought. An agent that can take actions can "
     "cause real harm &mdash; so decide upfront what it may only READ, what requires human "
     "confirmation, and when it must escalate.")

# ===== 5 =====
chapter(5, "Our Support Agent (the Blueprint)")
para("Here is the design we settled on for Project 2, in the same B2B SaaS support domain as "
     "Project 1.")
sec("The job")
para("A support agent that handles a customer ticket end to end: understand the question, "
     "look up whatever live information it needs, then either resolve the question or escalate "
     "to a human.")
sec("The first tool (Week 5 = one tool)")
para("<b>get_account_status(account_id)</b> &mdash; a mock that returns canned data: plan "
     "tier, billing status, and whether there is an active incident. We chose this first "
     "because looking up <i>live state the model cannot know</i> is the clearest demonstration "
     "of the agent idea. In Week 6 we add Project 1's document search as a second tool, tying "
     "the two projects together.")
sec("The guardrails")
para("The agent may <b>read</b> account status but must never take destructive or billing "
     "<b>actions</b> (refunds, plan changes, deletions). Those require a human. It escalates "
     "when unsure or when a real account change is requested &mdash; reusing the safety "
     "instinct from Project 1, where the system once wrongly offered destructive commands.")
sec('"Done"')
para("The agent is finished when it has either answered the customer using the looked-up "
     "information, or escalated with a clear reason. No silent dead-ends.")
proj("Three happy-path scenarios we will test in Week 5: (1) a question that needs the tool, "
     "(2) a general question that needs NO tool (it should not call it), and (3) an action "
     "request that should be declined and escalated.")

# ===== 6 =====
chapter(6, "Three Ways to Build the Loop")
para("We decided to build the SAME agent three times, increasing abstraction each time, so we "
     "understand what each layer hides. We start with the most hands-on.")
simple_table([["Approach", "Who runs the loop", "What you learn"],
              ["Manual (raw SDK)", "you, by hand", "everything &mdash; you see every step"],
              ["SDK tool runner", "the SDK", "less; the loop is hidden"],
              ["Framework", "the framework", "least; the library's abstractions"]],
             [4.2 * cm, 4.3 * cm, 7.0 * cm])
para("Week 5 builds the <b>manual loop</b>: send the tools, check whether the model asked for "
     "a tool, run it, send the result back, and repeat until the model is done. Building it "
     "the hard way first means that when the runner and the framework later handle the loop "
     "&quot;magically,&quot; you will know exactly what they are doing.")
plain("Learn it the hard way once, and every shortcut afterwards makes sense. Do it by hand, "
      "then let the tools do it for you.")

# ===== 7 =====
chapter(7, "Glossary")
for term, d in [
    ("Agent", "a system where the MODEL decides the steps, using tools to act, not just answer."),
    ("Agent loop", "the back-and-forth: model asks for a tool, your code runs it, model continues."),
    ("Tool / function calling", "a function you expose so the model can act beyond text."),
    ("Tool schema", "the name, description, and input shape that define a tool."),
    ("tool_use / tool_result", "the model's request to call a tool, and the result you send back."),
    ("Guardrail", "a rule limiting what the agent may do (e.g. read-only, escalate risky actions)."),
    ("Escalation", "handing off to a human when the agent is unsure or the action is risky."),
    ("Happy path", "the straightforward success case, before handling failures (that is Week 6)."),
    ("Manual loop", "writing the agent loop yourself with the raw SDK, for full understanding."),
]:
    story.append(Paragraph(f"<b>{esc(term)}</b> &mdash; {d}",
                           ParagraphStyle("g", parent=body, spaceAfter=4)))

story.append(Spacer(1, 14))
story.append(Paragraph("End of Day 1. Next: scaffold the repo and write the first tool "
                       "(Day 2), then wire the manual agent loop (Day 3).",
                       ParagraphStyle("end", parent=body, fontName="Helvetica-Oblique",
                                      textColor=ACCENT2)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "From Answering to Acting - Week 5 Day 1")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                      topMargin=2.2 * cm, bottomMargin=2.2 * cm)
doc.addPageTemplates([PageTemplate(id="all",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")],
    onPage=footer)])
doc.build(story)
print("WROTE", OUT)
