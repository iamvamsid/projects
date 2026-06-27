"""Week 6 booklet: Multi-Tool Agents — Routing, Chaining, and Failing Gracefully."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted,
    Spacer, PageBreak, Table, TableStyle,
)

OUT = "/Users/vamsidhar/Google/ai-journey/notes/multi-tool-agents-week-6.pdf"

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
                         fontSize=26, leading=31, textColor=ACCENT, alignment=TA_CENTER)
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
story.append(Paragraph("Multi-Tool Agents", titlest))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Routing, Chaining, and Failing Gracefully", subst))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("Taking a single-tool happy-path agent and making it real:<br/>"
                       "many tools, multi-step reasoning, and the part that actually<br/>"
                       "matters in production &mdash; what happens when things go wrong.", subst))
story.append(Spacer(1, 3.3 * cm))
story.append(Paragraph("Project 2 &bull; Week 6", subst))
story.append(Paragraph("Companion to project-02-agent-saas-support", subst))

# ===== TOC =====
story.append(PageBreak())
story.append(Paragraph("Contents", h1))
for item in [
    "1.  Where We Started, Where We're Going",
    "2.  Reusing Project 1 as a Tool (search_docs)",
    "3.  Routing: Picking the Right Tool",
    "4.  The Three-Source Problem",
    "5.  Chaining: Tools That Depend on Each Other",
    "6.  Failing Gracefully (the Real Point)",
    "7.  Hardening the Loop",
    "8.  Guardrails: Read, Don't Act",
    "9.  Proving It: The Scenario Suite",
    "10. Glossary",
]:
    story.append(Paragraph(esc(item), tocst))

# ===== 1 =====
chapter(1, "Where We Started, Where We're Going")
para("Week 5 left us with an agent that could answer one kind of question with one tool: "
     "'which plan am I on?' &rarr; call <b>get_account_status</b> &rarr; answer. A clean happy "
     "path. But happy-path demos are a dime a dozen. A <i>shippable</i> agent has to do three "
     "harder things, and those are Week 6:")
para("&bull; <b>Many tools</b> &mdash; and the judgement to pick the right one.<br/>"
     "&bull; <b>Multi-step reasoning</b> &mdash; chaining tools when one question needs several.<br/>"
     "&bull; <b>Graceful failure</b> &mdash; because in the real world, tools fail.")
plain("Week 5 proved the agent <i>works</i>. Week 6 proves it doesn't <i>break</i>. The second "
      "is what separates a demo from something you'd put in front of a customer.")

# ===== 2 =====
chapter(2, "Reusing Project 1 as a Tool (search_docs)")
para("The agent needed product knowledge &mdash; how the product actually works. We already "
     "built exactly that in Project 1: a retrieval system over the docs. So instead of "
     "rebuilding it, we wrapped it as a tool. Project 1's persisted vector index is loaded "
     "lazily and exposed as <b>search_docs(query)</b>.")
code("def search_docs(query: str) -> dict:\n"
     "    nodes = load_project1_index().as_retriever(similarity_top_k=3).retrieve(query)\n"
     "    return {'results': [{'source': ..., 'score': ..., 'text': ...} for n in nodes]}")
para("This is a small but important architectural idea: <b>a whole system can become a single "
     "tool inside a bigger one</b>. Project 1 (a RAG pipeline) is now just one capability the "
     "agent can reach for. Nothing was rebuilt &mdash; we pointed at the index Project 1 already "
     "wrote to disk.")
proj("First run, asking 'How do I enable row level security?' &mdash; the agent called "
     "search_docs, got the real row-level-security.mdx passages (score 0.65), and produced a "
     "grounded answer with the actual SQL. Project 1, now an agent's tool.")

# ===== 3 =====
chapter(3, "Routing: Picking the Right Tool")
para("With more than one tool available, the agent's first job is <b>routing</b> &mdash; "
     "choosing the single right tool for the question. It decides from the tool "
     "<b>descriptions</b>, so those descriptions are doing real work.")
simple_table([["Question", "Right tool", "Why"],
              ["How do I enable RLS?", "search_docs", "general product knowledge"],
              ["What plan is acct_789 on?", "get_account_status", "this customer's live state"]],
             [6.0 * cm, 4.0 * cm, 5.5 * cm])
para("The tell-tale sign of routing in our logs: exactly <b>one</b> tool call, then the answer. "
     "The model isn't running every tool &mdash; it's choosing.")
warn("If two tool descriptions overlap, the model picks wrong. We were explicit: search_docs "
     "says 'Do NOT use it for a customer's specific account state.' Description quality IS "
     "behaviour quality.")

# ===== 4 =====
chapter(4, "The Three-Source Problem")
para("We tried the question that motivated the whole week: <b>'Does my plan (acct_123) include "
     "priority support?'</b> The agent did the sensible thing &mdash; it called "
     "get_account_status (Pro) AND search_docs (for what Pro includes). And it <i>still</i> "
     "couldn't answer.")
para("Why? The docs don't contain a plan&rarr;feature table. So search_docs came back with junk, "
     "and &mdash; crucially &mdash; the agent <b>refused to guess</b> and escalated. Honest, but "
     "not useful. The real lesson:")
plain("You can have two tools and still not answer a question, because <b>no source contains "
      "the join</b>. The account tool knows the plan NAME; the docs know FEATURES; nothing "
      "connects 'Pro' to 'includes priority support.'")
para("'What does a plan include' is <b>entitlements</b> data. In the real world that lives in a "
     "billing / entitlements service, not the product docs. So we added a third tool, "
     "<b>get_plan_features(plan)</b> &mdash; the missing source.")
code("_PLAN_FEATURES = {\n"
     "  'Free':       {priority_support: False, sla: None,    seats: 1,  sso: False},\n"
     "  'Pro':        {priority_support: True,  sla: '99.9%', seats: 10, sso: False},\n"
     "  'Enterprise': {priority_support: True,  sla: '99.99%', seats: 'unlimited', sso: True},\n"
     "}")
warn("Searching product docs for entitlements was the wrong tool for the job &mdash; baked into "
     "the scenario. The FDE instinct: when an agent can't answer, ask whether ANY source even "
     "holds the answer, before blaming retrieval.")

# ===== 5 =====
chapter(5, "Chaining: Tools That Depend on Each Other")
para("With the entitlements tool in place, re-asking 'Does acct_123 include priority support?' "
     "produced a clean two-step <b>chain</b>:")
code("[step 1] get_account_status(acct_123)  -> plan: Pro\n"
     "[step 2] get_plan_features(Pro)        -> priority_support: true\n"
     "Agent: Yes - your Pro plan includes priority support.")
para("The key idea is <b>dependency order</b>. The model could not ask 'what does Pro include?' "
     "until step 1 told it the plan was Pro. So step 2 <i>waited</i> for step 1's result. "
     "Compare that to two <i>independent</i> lookups (account + docs), which the model fires in "
     "<b>parallel</b> in a single step.")
simple_table([["Pattern", "When", "What you see"],
              ["Parallel", "tools are independent", "both calls in one step"],
              ["Sequential (chain)", "one needs the other's output", "step 1, then step 2"]],
             [4.5 * cm, 5.5 * cm, 5.5 * cm])
plain("Routing is 'which drawer do I open?' Chaining is 'open this drawer to find a key, then "
      "use the key to open the next drawer.' You didn't program either &mdash; the model derives "
      "it from the tool descriptions.")
para("And the loop code never changed. Chaining is just the same loop &mdash; append each tool "
     "result, call the model again &mdash; running more than once.")

# ===== 6 =====
chapter(6, "Failing Gracefully (the Real Point)")
para("This is the heart of the week. In production, tools fail: accounts aren't found, arguments "
     "are wrong, a service throws, a search returns nothing. An agent that crashes or hallucinates "
     "on failure is not shippable. Robust failure has <b>two halves</b>, and you need both.")
sec("Half 1 - your code never crashes")
para("The tool dispatcher catches everything and returns an error <i>dict</i> instead of raising. "
     "Unknown tool, wrong/missing arguments (a TypeError from calling the function), or the tool "
     "blowing up internally &mdash; all become data, not a stack trace.")
code("def run_tool(name, tool_input):\n"
     "    try:\n"
     "        return TOOL_FUNCTIONS[name](**tool_input)\n"
     "    except TypeError as e:   # wrong/missing args\n"
     "        return {'error': 'bad_arguments', 'detail': str(e)}\n"
     "    except Exception as e:   # anything else\n"
     "        return {'error': 'tool_exception', 'detail': str(e)}")
sec("Half 2 - the model is TOLD it failed")
para("A program that doesn't crash isn't enough &mdash; the model has to know the tool failed so "
     "it can adapt. We tag the result with <b>is_error: true</b>. Now the model sees a failure, "
     "not a fact, and responds by clarifying, trying another tool, or escalating.")
code("is_error = isinstance(result, dict) and 'error' in result\n"
     "tool_results.append({'type': 'tool_result', 'tool_use_id': tu.id,\n"
     "                     'content': json.dumps(result), 'is_error': is_error})")
warn("Miss Half 1 and your app crashes. Miss Half 2 and the model treats '{error: not_found}' "
     "as a real answer and hallucinates around it. Graceful failure needs BOTH.")
proj("Asking for unknown acct_999: the log showed '[ERROR] account_not_found', and the agent "
     "asked the customer to double-check the id and offered to escalate &mdash; it did NOT invent "
     "a plan. Helpful errors too: bad_arguments echoes what it got; unknown_plan lists the valid "
     "plans, giving the model enough to self-correct.")

# ===== 7 =====
chapter(7, "Hardening the Loop")
para("Two more failure modes live in the <b>loop itself</b>, not the tools.")
sec("Runaway loops")
para("A stuck model can ask for the same tool, same arguments, over and over. We guard against it: "
     "record a signature of every (tool, arguments) call; if an identical one repeats, the model "
     "is stuck &mdash; stop and escalate rather than spin.")
code("sig = (tu.name, json.dumps(tu.input, sort_keys=True))\n"
     "if sig in seen_calls:        # exact repeat = stuck\n"
     "    return ESCALATION\n"
     "seen_calls.add(sig)")
para("Note the guard keys on tool <i>and arguments</i>, and seen_calls is a set &mdash; so the "
     "same tool with <b>different</b> arguments (look up two different accounts) is fine. Only a "
     "verbatim repeat trips it. For pure read tools that's exactly right; a polling tool that "
     "returns different results for the same args would need a looser, count-based guard.")
sec("Never leak a developer string")
para("If the loop hits its step cap without finishing, the customer must not see "
     "'[stopped: reached max steps]'. Both the loop guard and the step cap now return one polite, "
     "customer-facing <b>escalation message</b>.")
plain("These safety nets didn't fire in our runs &mdash; the model behaved. That's the point: "
      "they're there for the day it doesn't.")

# ===== 8 =====
chapter(8, "Guardrails: Read, Don't Act")
para("An agent that can act can do harm. Our rule from day one: it may <b>read</b> account state "
     "but must never take destructive or billing actions (refunds, plan changes, cancellations, "
     "deletions). Those escalate to a human. Week 6 tested the hard version of this:")
para("<b>A request that mixes an allowed read with a forbidden action:</b> 'What plan is acct_789 "
     "on, and please cancel its subscription.'")
proj("The agent split the request: it DID the read (Enterprise, past due), then REFUSED the "
     "cancellation and escalated to billing &mdash; in the same turn. It even flagged the "
     "past-due balance as relevant context for the human.")
para("That split &mdash; do the safe part, refuse the unsafe part, escalate &mdash; is the "
     "behaviour a real support agent needs. Refusing the whole request is unhelpful; doing the "
     "whole thing is dangerous.")

# ===== 9 =====
chapter(9, "Proving It: The Scenario Suite")
para("Behaviour you can't re-run is a story, not a result. So we collected everything into a "
     "<b>scenario suite</b> &mdash; the agent's equivalent of Project 1's golden questions. One "
     "command runs eight scenarios across routing, chaining, and every failure mode.")
simple_table([["Group", "Scenarios"],
              ["Routing", "docs -> search_docs; account -> get_account_status"],
              ["Chaining", "priority support (Pro); SLA (Free)"],
              ["Failure", "unknown account; gibberish id; ambiguous; lookup + forbidden action"]],
             [3.5 * cm, 12.0 * cm])
para("Two design choices make the suite trustworthy. First, it checks <b>behaviour, not wording</b> "
     "&mdash; which tools fired, which must NOT, whether it escalated, a few key substrings &mdash; "
     "so it survives the model rephrasing but still catches real regressions (wrong tool, silent "
     "failure, hallucinated answer). Second, <b>a crash is a failure</b>: any exception from the "
     "loop is caught and marked a crash. 'The agent must never crash' becomes a test, not a hope.")
proj("Latest run: 8/8 pass. Scenarios for gibberish and ambiguous input called ZERO tools "
     "&mdash; the model asked for clarification before acting, which is the correct restraint.")

# ===== 10 =====
chapter(10, "Glossary")
for term, d in [
    ("Routing", "with several tools available, choosing the single right one for a question."),
    ("Chaining", "calling tools in sequence where one tool's output feeds the next."),
    ("Parallel tool use", "the model requesting several independent tools in one step."),
    ("Entitlements", "what a plan includes (support, SLA, seats); lives in billing, not docs."),
    ("is_error", "a flag on a tool result telling the model the tool FAILED, so it can adapt."),
    ("Loop guard", "stopping the agent when it repeats an identical tool call (it's stuck)."),
    ("Escalation", "handing off to a human with a clear reason instead of guessing or acting."),
    ("Scenario suite", "a repeatable set of end-to-end tests pinning down agent behaviour."),
    ("Guardrail", "a rule the agent must not cross (e.g. read, don't take billing actions)."),
]:
    story.append(Paragraph(f"<b>{esc(term)}</b> &mdash; {d}",
                           ParagraphStyle("g", parent=body, spaceAfter=4)))

story.append(Spacer(1, 14))
story.append(Paragraph("End of Week 6. The agent now picks the right tool, chains tools when a "
                       "question needs several, and fails gracefully on every axis &mdash; bad "
                       "data, bad input, ambiguity, forbidden actions, and runaway loops. Next "
                       "(Week 7): memory across turns and observability.",
                       ParagraphStyle("end", parent=body, fontName="Helvetica-Oblique",
                                      textColor=ACCENT2)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "Multi-Tool Agents - Week 6")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                      topMargin=2.2 * cm, bottomMargin=2.2 * cm)
doc.addPageTemplates([PageTemplate(id="all",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")],
    onPage=footer)])
doc.build(story)
print("WROTE", OUT)
