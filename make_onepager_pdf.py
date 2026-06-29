"""One-page customer-facing one-pager PDF (CTO audience) with embedded diagram."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Image, Table, TableStyle,
)

OUT = "/Users/vamsidhar/Google/ai-journey/projects/project-02-agent-saas-support/onepager/support-agent-one-pager.pdf"
DIAGRAM = "/Users/vamsidhar/Google/ai-journey/projects/project-02-agent-saas-support/docs/architecture-onepager.png"

ACCENT = colors.HexColor("#a8541a")
ACCENT2 = colors.HexColor("#c46a2a")
INK = colors.HexColor("#2c2c2a")
MUTED = colors.HexColor("#5f5e5a")

styles = getSampleStyleSheet()
title = ParagraphStyle("title", parent=styles["Title"], fontName="Helvetica-Bold",
                       fontSize=19, leading=23, textColor=ACCENT, alignment=TA_LEFT, spaceAfter=2)
tagline = ParagraphStyle("tag", parent=styles["Normal"], fontName="Helvetica-Oblique",
                         fontSize=11, leading=15, textColor=MUTED, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=10.8, leading=13, textColor=ACCENT2, spaceBefore=5, spaceAfter=2)
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=9.1, leading=12.4, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=4)
bullet = ParagraphStyle("bul", parent=body, leftIndent=12, spaceAfter=1.5)
foot = ParagraphStyle("foot", parent=body, fontName="Helvetica-Oblique", fontSize=8.3,
                      leading=11, textColor=MUTED, alignment=TA_LEFT)

story = []


def para(t): story.append(Paragraph(t, body))
def head(t): story.append(Paragraph(t, h2))
def bul(t): story.append(Paragraph("&bull;&nbsp; " + t, bullet))


story.append(Paragraph("AI Support Agent — resolve more tickets, safely", title))
story.append(Paragraph("An AI agent that answers customer support questions end to end — "
                       "and knows when to hand off to a human.", tagline))

# thin accent rule
rule = Table([[""]], colWidths=[16.4 * cm], rowHeights=[2])
rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT)]))
story.append(rule); story.append(Spacer(1, 6))

head("The problem")
para("Support volume keeps rising, but answers don't keep up. Front-line agents juggle three "
     "separate systems for a single question — the customer's <b>account</b>, the <b>product "
     "documentation</b>, and <b>what their plan actually includes</b> — and the answer often "
     "lives in the gap between them. The result: slow first responses, inconsistent answers, "
     "and skilled people spending their day on routine lookups.")

head("What it does")
para("A single agent handles the conversation end to end. For each question it decides which "
     "sources it needs, pulls them together, and either resolves the question or escalates with "
     "context — from one-off questions (&ldquo;how do I enable SSO?&rdquo;) to questions that "
     "need several systems at once (&ldquo;does <i>my</i> plan include priority support?&rdquo;).")

# diagram, centered, sized to width
img = Image(DIAGRAM, width=10.6 * cm, height=10.6 * cm * 744 / 1360)
img.hAlign = "CENTER"
story.append(Spacer(1, 1)); story.append(img); story.append(Spacer(1, 2))

head("Why you can trust it")
bul("<b>Read-only by design.</b> It can look up account and billing information, but cannot "
    "make changes — no cancellations, refunds, or plan edits. Those always go to a human.")
bul("<b>It refuses risky requests and escalates.</b> Asked to do something it shouldn't, it "
    "does the safe part, declines the rest, and routes it to the right team — in one reply.")
bul("<b>It never makes things up.</b> When the information isn't available, it says so and "
    "escalates, rather than guessing.")
bul("<b>It remembers the conversation</b> — customers don't repeat themselves — within bounds.")

head("What you can measure")
para("Every interaction is fully logged: which sources were used, what they returned, where it "
     "escalated, and the <b>tokens, cost, and response time</b> of each one. You can see exactly "
     "what the agent did on any ticket, and price it. Reliability is verified against a fixed "
     "suite of real scenarios — routing, multi-step questions, and every failure mode — all passing.")

head("The bottom line")
para("Faster, consistent first responses on routine questions; humans freed for the cases that "
     "need them; and a full, costed audit trail behind every answer. The agent extends a team's "
     "capacity without giving up control or visibility.")

story.append(Spacer(1, 6))
story.append(Paragraph("Demonstrated on a working prototype. The account and billing connections "
                       "use stand-in data; the agent is built so that swapping those for live "
                       "systems does not change how it behaves. Technical write-up and source "
                       "available on request.", foot))


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                      topMargin=1.5 * cm, bottomMargin=1.4 * cm)
doc.addPageTemplates([PageTemplate(id="all",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")])])
doc.build(story)
print("WROTE", OUT)
