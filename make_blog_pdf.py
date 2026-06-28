"""Render the Project 2 blog markdown into a clean article-style PDF."""

import re
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted,
    Spacer, Table, TableStyle,
)

SRC = "/Users/vamsidhar/Google/ai-journey/projects/project-02-agent-saas-support/blog/building-a-support-agent.md"
OUT = "/Users/vamsidhar/Google/ai-journey/projects/project-02-agent-saas-support/blog/building-a-support-agent.pdf"

ACCENT = colors.HexColor("#a8541a")
ACCENT2 = colors.HexColor("#c46a2a")
CODEBG = colors.HexColor("#f7f3ef")
QUOTEBG = colors.HexColor("#f6efe8")

styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=10.5, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=8)
h1 = ParagraphStyle("h1", parent=styles["Title"], fontName="Helvetica-Bold",
                    fontSize=20, leading=25, textColor=ACCENT, alignment=TA_LEFT, spaceAfter=10)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=14, leading=18, textColor=ACCENT2, spaceBefore=12, spaceAfter=6)
bullet = ParagraphStyle("bul", parent=body, leftIndent=14, spaceAfter=3)
codest = ParagraphStyle("code", parent=styles["Code"], fontName="Courier",
                        fontSize=8.0, leading=10.5, textColor=colors.HexColor("#222"))
caption = ParagraphStyle("cap", parent=body, fontName="Helvetica-Oblique",
                         fontSize=9, textColor=colors.HexColor("#777"), alignment=TA_LEFT)

story = []


def inline(text):
    """Markdown inline -> reportlab markup. Escape first, then style."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r'<font face="Courier" size="9">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return text


def codebox(text):
    t = Table([[Preformatted(text.strip("\n"), codest)]], colWidths=[16.0 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CODEBG),
                           ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e0d3c6")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(t); story.append(Spacer(1, 6))


def quotebox(text):
    inner = Paragraph(inline(text), ParagraphStyle("q", parent=body, fontName="Helvetica-Oblique",
                                                   fontSize=10.5, leading=15, spaceAfter=0))
    t = Table([[inner]], colWidths=[16.0 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), QUOTEBG),
                           ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                           ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT2)]))
    story.append(Spacer(1, 4)); story.append(t); story.append(Spacer(1, 8))


def render():
    lines = open(SRC).read().splitlines()
    i = 0
    para_buf, quote_buf = [], []

    def flush_para():
        if para_buf:
            story.append(Paragraph(inline(" ".join(para_buf)), body))
            para_buf.clear()

    def flush_quote():
        if quote_buf:
            quotebox(" ".join(quote_buf))
            quote_buf.clear()

    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            flush_para(); flush_quote()
            i += 1; buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            codebox("\n".join(buf)); i += 1; continue
        if ln.startswith("# "):
            flush_para(); flush_quote(); story.append(Paragraph(inline(ln[2:]), h1)); i += 1; continue
        if ln.startswith("## "):
            flush_para(); flush_quote(); story.append(Paragraph(inline(ln[3:]), h2)); i += 1; continue
        if ln.startswith("!["):
            flush_para(); flush_quote()
            story.append(Paragraph("[ Figure: system architecture — see docs/architecture.svg ]", caption))
            story.append(Spacer(1, 6)); i += 1; continue
        if ln.startswith("> "):
            flush_para(); quote_buf.append(ln[2:]); i += 1; continue
        if ln.startswith("- "):
            flush_para(); flush_quote()
            story.append(Paragraph("&bull;&nbsp; " + inline(ln[2:]), bullet)); i += 1; continue
        if ln.strip() == "":
            flush_para(); flush_quote(); i += 1; continue
        quote_buf and flush_quote()
        para_buf.append(ln.strip()); i += 1

    flush_para(); flush_quote()


render()


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "Building a B2B SaaS Support Agent")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                      topMargin=2.2 * cm, bottomMargin=2.2 * cm)
doc.addPageTemplates([PageTemplate(id="all",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")],
    onPage=footer)])
doc.build(story)
print("WROTE", OUT)
