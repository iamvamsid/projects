"""Week 5 Day 3 booklet: The Agent Loop, Three Ways."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted,
    Spacer, PageBreak, Table, TableStyle,
)

OUT = "/Users/vamsidhar/Google/ai-journey/notes/agent-loop-week-5-day-3.pdf"

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
story.append(Spacer(1, 5 * cm))
story.append(Paragraph("The Agent Loop, Three Ways", titlest))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("From a Hand-Written Loop to a Framework", subst))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("The same support agent built three times &mdash; raw SDK,<br/>"
                       "SDK tool runner, and a framework &mdash; so you understand<br/>"
                       "exactly what each abstraction hides.", subst))
story.append(Spacer(1, 3.5 * cm))
story.append(Paragraph("Project 2 &bull; Week 5 &bull; Day 3", subst))
story.append(Paragraph("Companion to project-02-agent-saas-support", subst))

# ===== TOC =====
story.append(PageBreak())
story.append(Paragraph("Contents", h1))
for item in [
    "1.  Recap: What the Agent Loop Is",
    "2.  Version 1 - The Manual Loop (Raw SDK)",
    "3.  Version 2 - The SDK Tool Runner",
    "4.  Version 3 - The Framework",
    "5.  Side by Side: What Each One Hides",
    "6.  When to Use Which",
    "7.  Glossary",
]:
    story.append(Paragraph(esc(item), tocst))

# ===== 1 =====
chapter(1, "Recap: What the Agent Loop Is")
para("An agent is not one request and one reply. It is a <b>loop</b>: the model may ask to "
     "use a tool, your code runs the tool and hands back the result, and the model continues "
     "&mdash; round and round until it can give a final answer.")
code("user message\n"
     "  -> model decides: answer directly, OR call a tool\n"
     "       -> (tool call) code runs the tool, returns the result\n"
     "            -> model continues with the result\n"
     "                 -> final answer, or another tool call ...")
para("Today we built the <i>same</i> support agent three times. The agent's behaviour is "
     "identical every time; the only thing that changes is <b>who runs that loop</b>. Building "
     "it the hard way first means every shortcut afterwards is understood, not magic.")
plain("The agent is the loop. Three versions, one loop &mdash; we just keep handing the "
      "loop-running job to someone else each time.")

# ===== 2 =====
chapter(2, "Version 1 - The Manual Loop (Raw SDK)")
para("Here WE write the loop. We send the model the tools; if it returns a "
     "<b>tool_use</b> request, we run the tool ourselves and send back a <b>tool_result</b>; "
     "then we call the model again. We repeat until the model stops asking for tools.")
code("messages = [{'role': 'user', 'content': user_input}]\n"
     "while True:\n"
     "    response = client.messages.create(model, system, tools=TOOLS, messages=messages)\n"
     "    if response.stop_reason == 'end_turn':\n"
     "        return final_text(response)          # the model is done\n"
     "    # else: it asked for a tool\n"
     "    messages.append({'role': 'assistant', 'content': response.content})\n"
     "    results = [run_tool(tu.name, tu.input) for tu in tool_uses(response)]\n"
     "    messages.append({'role': 'user', 'content': tool_results})  # send back, loop")
para("Two details that matter: each <b>tool_result</b> must carry the same id as the "
     "<b>tool_use</b> it answers, and you must append the model's tool-call turn to the history "
     "before you send the results. Get either wrong and the conversation breaks.")
warn("The model never executes the tool. It only REQUESTS it; your code runs it. That gap is "
     "your control point &mdash; it is where you validate inputs, gate risky actions, or refuse.")
proj("Our run printed exactly this: '[step 1] model calls get_account_status(acct_123) -> "
     "{plan: Pro...}' and then the answer. You can literally watch the loop turn once.")

# ===== 3 =====
chapter(3, "Version 2 - The SDK Tool Runner")
para("Now the SDK runs the loop. We decorate our function as a tool and hand it to "
     "<b>tool_runner()</b>; the SDK calls the model, runs the tool when asked, feeds the result "
     "back, and repeats &mdash; all internally. The while-loop disappears from our code.")
code("@beta_tool\n"
     "def get_account_status(account_id: str) -> str:\n"
     "    '''Look up a customer's account status by id. Use when ...'''  # <- becomes the schema\n"
     "    return json.dumps(lookup(account_id))\n"
     "\n"
     "runner = client.beta.messages.tool_runner(\n"
     "    model=MODEL, system=SYSTEM, tools=[get_account_status], messages=[...])\n"
     "for message in runner:        # the SDK is running the loop for us\n"
     "    ...")
para("Notice a second thing vanished too: we no longer hand-write the tool's JSON schema. The "
     "SDK generates it from the function's signature and <b>docstring</b> &mdash; so the "
     "docstring becomes the description the model reads. Write it carefully.")
plain("Same agent, but 'for message in runner' is now hiding the exact while-loop from "
      "Version 1. Because we wrote that loop ourselves first, this is not mysterious.")

# ===== 4 =====
chapter(4, "Version 3 - The Framework")
para("The framework (here, LlamaIndex's FunctionAgent) hides the most. We give it a tool, an "
     "LLM, and a system prompt; it wraps all three and runs the whole loop. Our code shrinks to "
     "almost nothing.")
code("llm = Anthropic(model=MODEL, max_tokens=1024)\n"
     "tool = FunctionTool.from_defaults(fn=get_account_status, description=...)\n"
     "agent = FunctionAgent(tools=[tool], llm=llm, system_prompt=SYSTEM)\n"
     "response = await agent.run(user_input)    # the framework runs everything")
para("This is the least code and the least visibility. The framework also wraps the LLM itself "
     "(its own Anthropic adapter) and the tool object, so even the model call is one layer "
     "removed from you.")
warn("Frameworks change their APIs often &mdash; the exact class names and whether a call is "
     "async shift between versions. Convenient, but you are now learning the library, not the "
     "mechanics. Knowing the manual version protects you when the framework surprises you.")

# ===== 5 =====
chapter(5, "Side by Side: What Each One Hides")
simple_table([["Aspect", "Manual (raw SDK)", "Tool runner", "Framework"],
              ["Who runs the loop", "you", "the SDK", "the framework"],
              ["Tool schema", "hand-written", "from docstring", "from function"],
              ["The LLM call", "yours", "yours", "wrapped by framework"],
              ["Lines of code", "~40", "~15", "~10"],
              ["Visibility", "full", "some", "least"]],
             [3.6 * cm, 3.6 * cm, 3.6 * cm, 4.7 * cm])
para("The behaviour was the same in all three (it called the tool, answered, and escalated the "
     "billing action). The progression is purely <b>how much you can see</b> versus <b>how "
     "little you have to write</b>.")

# ===== 6 =====
chapter(6, "When to Use Which")
para("There is no single right answer &mdash; it depends on what you need.")
para("&bull; <b>Manual loop</b> &mdash; when you need full control: custom logging, "
     "human-in-the-loop approval before a tool runs, conditional execution, or unusual flows. "
     "Also the best way to <i>learn</i>.")
para("&bull; <b>Tool runner</b> &mdash; the practical middle ground for most Anthropic-native "
     "apps: the loop handled for you, but you stay close to the SDK and can still inspect each "
     "step.")
para("&bull; <b>Framework</b> &mdash; when you want speed and you are already living in that "
     "framework's world (many tools, retrieval, multi-agent orchestration). Accept that it "
     "hides the mechanics.")
plain("Build it by hand to learn; reach for the runner for most real work; pick a framework "
      "when its extra machinery genuinely earns its keep.")

# ===== 7 =====
chapter(7, "Glossary")
for term, d in [
    ("Agent loop", "the model-asks-for-tool / you-run-it / model-continues cycle, repeated."),
    ("stop_reason", "why the model stopped: 'tool_use' (it wants a tool) or 'end_turn' (done)."),
    ("tool_use", "the model's structured request to call a named tool with arguments."),
    ("tool_result", "the result you send back, tagged with the matching tool_use id."),
    ("Tool schema", "the name + description + input shape that tells the model how to call a tool."),
    ("tool_runner", "an SDK helper that runs the agent loop for you."),
    ("FunctionAgent", "a LlamaIndex agent that wraps the LLM, tools, and loop."),
    ("Abstraction", "hiding detail to save effort; the trade is less visibility and control."),
]:
    story.append(Paragraph(f"<b>{esc(term)}</b> &mdash; {d}",
                           ParagraphStyle("g", parent=body, spaceAfter=4)))

story.append(Spacer(1, 14))
story.append(Paragraph("End of Day 3. You can now explain an agent at every level of "
                       "abstraction &mdash; a level above 'I used a framework.' Next: a second "
                       "tool, and handling failures (Week 6).",
                       ParagraphStyle("end", parent=body, fontName="Helvetica-Oblique",
                                      textColor=ACCENT2)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "The Agent Loop, Three Ways - Week 5 Day 3")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                      topMargin=2.2 * cm, bottomMargin=2.2 * cm)
doc.addPageTemplates([PageTemplate(id="all",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")],
    onPage=footer)])
doc.build(story)
print("WROTE", OUT)
