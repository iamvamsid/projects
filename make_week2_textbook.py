"""Generate a descriptive textbook-style PDF on Building a RAG System (Week 2)."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted,
    Spacer, PageBreak, Table, TableStyle,
)

OUT = "/Users/vamsidhar/Google/ai-journey/notes/building-rag-textbook.pdf"

ACCENT = colors.HexColor("#1f6f5c")
ACCENT2 = colors.HexColor("#2e8b74")
CODEBG = colors.HexColor("#f1f5f3")
PROJBG = colors.HexColor("#e9f3ef")
PLAINBG = colors.HexColor("#eef4ec")
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
                           ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cfded8")),
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
story.append(Paragraph("Building a RAG System", titlest))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("From a Folder of Docs to a Cited Answer", subst))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("Corpus and cleaning, chunking, embeddings, indexes,<br/>"
                       "retrieval, grounded generation, and knowing when to<br/>"
                       "refuse &mdash; every concept from Week 2, in plain words.", subst))
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("Companion to project-01-rag-saas-support", subst))

# ===== TOC =====
story.append(PageBreak())
story.append(Paragraph("Contents", h1))
for item in [
    "1.  What RAG Is, and Why It Exists",
    "2.  Getting and Cleaning the Corpus",
    "3.  Documents and Chunks",
    "4.  Embeddings: Turning Meaning into Numbers",
    "5.  The Index: Storing Knowledge You Can Search",
    "6.  Persistence: Don't Pay Twice",
    "7.  Retrieval: Finding the Right Passages",
    "8.  Grounded Generation with Citations",
    "9.  Knowing When to Say 'I Don't Know'",
    "10. Does RAG Help on Data the Model Already Saw?",
    "11. The Bugs We Hit (and What They Taught)",
    "12. The Mental Model and Glossary",
]:
    story.append(Paragraph(esc(item), tocst))

# ===== CH1 =====
chapter(1, "What RAG Is, and Why It Exists")
para("A language model on its own has two problems for a support assistant. First, it only "
     "knows what it saw during training &mdash; it has never read <i>your</i> product's "
     "current docs or private tickets. Second, when it does not know something, it tends to "
     "make up a confident-sounding answer rather than admit ignorance.")
para("<b>RAG &mdash; Retrieval-Augmented Generation</b> &mdash; fixes both by giving the model "
     "an open book. Instead of answering from memory, the system first <i>retrieves</i> the "
     "most relevant passages from your documents, then asks the model to answer <i>using only "
     "those passages</i>. The answer is grounded in real, current, citable text.")
plain("RAG = let the AI look things up in your documents before answering, instead of "
      "answering from memory. Open-book exam, not closed-book.")
proj("We built a support assistant over Supabase's documentation. A user asks a question; the "
     "system finds the relevant doc passages and answers from them, with citations &mdash; and "
     "escalates to a human when the docs do not contain the answer.")
para("The whole pipeline is one sentence: <b>load documents, clean them, chop them into "
     "chunks, turn each chunk into a searchable vector, store them; then for each question, "
     "retrieve the closest chunks and have the model answer from them with citations.</b> The "
     "rest of this book walks that sentence one piece at a time.")

# ===== CH2 =====
chapter(2, "Getting and Cleaning the Corpus")
para("The <b>corpus</b> is the collection of documents the system can draw on &mdash; its "
     "knowledge base. The first practical step is simply getting those documents onto disk.")
proj("We pulled three sections of the Supabase docs (auth, database, storage) &mdash; about "
     "210 Markdown files &mdash; using a sparse checkout so we did not download their entire "
     "company repository. Starting with a focused subset, not the whole site, is deliberate: a "
     "small corpus that works beats a giant one that half-works.")
sec("Cleaning matters more than any model choice")
para("Raw docs are full of noise that is not actual content: page front-matter (title/"
     "metadata blocks), special markup, template files used by the doc authors. If you embed "
     "that noise, you pollute your search &mdash; and a junk passage retrieved is a junk (but "
     "confident, and cited) answer.")
warn("The hard truth of RAG: retrieval quality is mostly a DATA problem, not a model problem. "
     "Garbage in, garbage out is literal here. A hallucinated answer can usually be traced "
     "back to a junk chunk that should never have been in the index.")
proj("Inspecting our very first loaded document revealed it was a TEMPLATE file (not real "
     "content), and every file carried front-matter and markup noise. So we added a cleaning "
     "pass: drop template files, strip front-matter and markup. 210 files became 209 real, "
     "clean documents.")

# ===== CH3 =====
chapter(3, "Documents and Chunks")
para("Two units of text matter. A <b>Document</b> is one whole source &mdash; usually one file. "
     "A <b>chunk</b> (or node) is a small slice of a document. The pipeline turns each Document "
     "into several chunks.")
sec("Why not just use whole documents?")
para("Because a document is too big to search precisely. If you turn an entire 18,000-character "
     "page into a single searchable unit, its meaning becomes a blur &mdash; you would retrieve "
     "&quot;the whole RLS page&quot; instead of &quot;the specific paragraph about enabling "
     "it.&quot; And you would stuff the model's context with mostly-irrelevant text. So we "
     "<b>chunk</b>: split each document into passages of a few hundred words.")
sec("Chunk size and overlap")
para("<b>Chunk size</b> is how big each piece is (we used about 512 tokens). <b>Overlap</b> is "
     "a small amount of text repeated between neighbouring chunks (we used 50 tokens), so an "
     "idea that straddles a boundary is not sliced in half.")
proj("Chunking our 209 clean documents produced 1,137 chunks &mdash; roughly five per "
     "document. Retrieval now works at the paragraph level, which is what makes answers precise.")
plain("A document is the whole chapter; chunks are the paragraphs. You search paragraphs, "
      "because that is the level at which a precise answer actually lives.")

# ===== CH4 =====
chapter(4, "Embeddings: Turning Meaning into Numbers")
para("How does a computer decide which chunk is &quot;most relevant&quot; to a question? It "
     "cannot read. So we convert meaning into maths using <b>embeddings</b>.")
para("An <b>embedding</b> turns a piece of text into a vector &mdash; a long list of numbers "
     "&mdash; that captures its meaning. The key property: texts with similar meaning produce "
     "vectors that sit close together in &quot;vector space.&quot; So &quot;find relevant "
     "chunks&quot; becomes &quot;find the chunk vectors closest to the question's vector,&quot; "
     "measured by <b>cosine similarity</b> (closeness of direction; 1.0 = identical meaning).")
proj("We embedded all 1,137 chunks with OpenAI's text-embedding-3-small model (each vector is "
     "1,536 numbers). It took about 17 seconds and a cent or two.")
sec("The most important idea in the whole pipeline")
para("There are <b>two different models doing two different jobs</b>, and confusing them is the "
     "classic beginner mistake.")
simple_table([["Role", "Model (ours)", "Job"],
              ["Embedding model", "text-embedding-3-small", "text into vectors, for FINDING chunks"],
              ["Generation model", "claude-opus-4-8", "read chunks, WRITE the answer"]],
             [3.5 * cm, 5.0 * cm, 7.5 * cm])
plain("Embeddings FIND; the language model ANSWERS. If you remember one sentence about how RAG "
      "works, make it that one.")

# ===== CH5 =====
chapter(5, "The Index: Storing Knowledge You Can Search")
para("Once every chunk has a vector, you need somewhere to keep them that supports fast "
     "&quot;find the nearest vectors&quot; searches. That structure is the <b>index</b> (a "
     "vector index / vector store).")
para("Building the index is the moment all the earlier pieces come together: it takes the "
     "cleaned documents, applies the chunking, runs every chunk through the embedding model, "
     "and stores the resulting vectors alongside each chunk's text and metadata.")
code("# the one call that runs the back half of ingestion\n"
     "index = VectorStoreIndex.from_documents(\n"
     "    docs,\n"
     "    transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=50)],\n"
     ")")
para("That single call is exactly why a framework saves time &mdash; and exactly why you "
     "should understand the steps it hides, so the convenience never becomes a mystery.")

# ===== CH6 =====
chapter(6, "Persistence: Don't Pay Twice")
para("Embedding is the slow, costly step. You do not want to repeat it every time the program "
     "runs. <b>Persistence</b> writes the finished index to disk; loading it back skips all the "
     "re-embedding.")
code("index.storage_context.persist('storage')     # save once\n"
     "# later, in another run:\n"
     "index = load_index_from_storage(\n"
     "    StorageContext.from_defaults(persist_dir='storage'))")
warn("When you reload the index to answer questions, you MUST configure the SAME embedding "
     "model you built it with. The question gets embedded too, and the question's vector is "
     "only comparable to the chunk vectors if the same model produced both. Mismatch them and "
     "you get nonsense rankings with no error message.")
proj("Our saved index is about 36 MB. It is git-ignored &mdash; it is a regenerable build "
     "artifact, not source code, so there is no reason to commit it.")

# ===== CH7 =====
chapter(7, "Retrieval: Finding the Right Passages")
para("With the index built, retrieval is straightforward: embed the user's question with the "
     "same embedding model, then ask the index for the <b>top-k</b> chunks whose vectors are "
     "closest to the question's vector. Each result comes back with a similarity score and the "
     "source file it came from.")
code('results = index.as_retriever(similarity_top_k=5).retrieve(\n'
     '    "How do I enable row level security?")\n'
     'for r in results:\n'
     '    print(r.score, r.node.metadata["file_name"])')
proj("On &quot;how do I enable RLS?&quot; our top chunk scored about 0.69 and came from "
     "row-level-security.mdx &mdash; the right page. On an unrelated billing question, the best "
     "score was about 0.30. That low score is a signal in itself: it tells the system nothing "
     "relevant was found.")
plain("Retrieval = embed the question the same way the chunks were embedded, then grab the "
      "handful of chunks pointing in the most similar direction.")

# ===== CH8 =====
chapter(8, "Grounded Generation with Citations")
para("Now the second model earns its keep. We take the retrieved chunks, format them into a "
     "numbered context block, and ask the language model to answer &mdash; with strict "
     "instructions.")
sec("The grounding prompt is the heart of the system")
para("The system prompt tells the model: answer <b>only</b> from the provided passages; cite "
     "the passages you use with their numbers; and if the answer is not in the passages, say so "
     "rather than guess. This is what stops the model from quietly answering from its own "
     "memory and inventing details.")
proj("We deliberately used the framework to RETRIEVE, but called the language model directly "
     "to GENERATE. Why: the grounding prompt is the most important, most-tunable part of the "
     "system, so we kept it explicit and visible in our own code rather than buried inside a "
     "one-line framework call.")
sec("Citations come for free")
para("Because each chunk carried its source file as metadata from the very start (loading), "
     "that source rides all the way through to the answer. So every claim can point back to the "
     "document it came from &mdash; the trust feature that makes the whole thing credible to a "
     "real customer.")

# ===== CH9 =====
chapter(9, "Knowing When to Say 'I Don't Know'")
para("The single feature that separates a trustworthy assistant from a dangerous one is the "
     "ability to <b>refuse</b>. A support bot that confidently answers a question it has no "
     "information about will eventually give a customer a wrong, damaging answer.")
para("Our grounding prompt instructs the model to escalate to a human when the retrieved "
     "passages do not contain the answer. The <b>low retrieval score</b> from Chapter 7 is the "
     "tell-tale: when nothing relevant was found, the right move is to decline.")
proj("Asked to &quot;refund my account and bump my priority,&quot; retrieval scored about 0.30 "
     "(nothing relevant), and the system declined and pointed to human support &mdash; instead "
     "of inventing a refund. A naive bot would have happily &quot;processed&quot; it.")
plain("A good assistant knows the edges of its own knowledge. &quot;I do not have that "
      "information, let me get a human&quot; is a feature, not a failure.")

# ===== CH10 =====
chapter(10, "Does RAG Help on Data the Model Already Saw?")
para("A sharp question: Supabase's docs are public, so the language model probably already saw "
     "them in training. Does feeding them back via RAG actually help? <b>Yes &mdash; and "
     "understanding why is worth a lot.</b>")
para("The model's memory of its training data is <b>lossy and unverifiable</b>. It compressed "
     "billions of documents into its weights, so it remembers the <i>gist</i> but hallucinates "
     "the <i>specifics</i> &mdash; exact flags, function names, defaults. Retrieval hands it the "
     "exact text, so it stops guessing details. It also makes answers <b>citable</b> "
     "(impossible from memory) and <b>current</b> (the model's training froze; your docs are "
     "today's).")
warn("The catch: RAG's quality is capped by retrieval quality. If retrieval pulls the wrong "
     "passages, you have grounded the model in the wrong thing &mdash; the answer can be worse "
     "than its own memory, and confidently cited.")
para("And the deeper point: public docs are the <b>weakest</b> case for RAG &mdash; chosen "
     "because the data is easy to get. RAG's real power is <b>private</b> data the model has "
     "never seen: internal tickets, runbooks, a company's own policies. That is the real "
     "deployment; public docs are just the practice ground.")

# ===== CH11 =====
chapter(11, "The Bugs We Hit (and What They Taught)")
para("Building this was not a clean straight line. The bugs are worth remembering, because the "
     "debugging IS the engineering.")
para("<b>1. &quot;Module not found.&quot;</b> The package install seemed to run, but the code "
     "could not find it. Cause: the dependency list had been truncated, and we were installing "
     "into a different environment than we ran from. Lesson: activate the right environment "
     "<i>before</i> installing, and confirm which one you are in.")
para("<b>2. &quot;Property has no setter.&quot;</b> We tried to overwrite a document's text "
     "after cleaning, but in this library version the text field is read-only. Lesson: build a "
     "new Document with the cleaned text instead of mutating the old one.")
para("<b>3. &quot;Missing credentials.&quot;</b> Embedding failed because the project had no "
     "local secrets file &mdash; the keys lived elsewhere. Lesson: know exactly where your "
     "program loads its keys from.")
plain("None of these were deep AI problems &mdash; they were ordinary engineering friction. "
      "Getting comfortable with that friction is most of what &quot;building with AI&quot; "
      "actually feels like.")
para("We also corrected a wrong assumption: we briefly blamed a too-new Python version, but the "
     "real cause was the truncated dependency list. Chasing the right cause, not the "
     "first-guess cause, is the skill.")

# ===== CH12 =====
chapter(12, "The Mental Model and Glossary")
sec("The whole system in one picture")
code("file on disk\n"
     "  -> Document (whole file)\n"
     "    -> clean (drop templates, strip noise)\n"
     "      -> chunks (small passages)\n"
     "        -> embeddings (a vector per chunk)\n"
     "          -> index (searchable store)        [BUILD ONCE]\n"
     "\n"
     "question\n"
     "  -> embed the question\n"
     "    -> retrieve nearest chunks (top-k + scores + sources)\n"
     "      -> ground the model in them\n"
     "        -> cited answer  (or: escalate if nothing relevant)")
sec("Glossary")
for term, d in [
    ("RAG", "Retrieval-Augmented Generation &mdash; look things up before answering."),
    ("Corpus", "the collection of documents the system can draw on."),
    ("Document", "one whole source item, usually a file."),
    ("Chunk / node", "a small slice of a document; the unit that gets embedded and retrieved."),
    ("Chunk size", "how big each chunk is (e.g. ~512 tokens)."),
    ("Overlap", "text repeated between neighbouring chunks so ideas are not cut in half."),
    ("Embedding", "a vector capturing a text's meaning; similar meaning, nearby vectors."),
    ("Cosine similarity", "how aligned two vectors are; 1.0 = identical meaning."),
    ("Index / vector store", "the searchable structure holding chunk vectors."),
    ("Persistence", "saving the index to disk so you don't re-embed every run."),
    ("Retrieval", "finding the top-k chunks closest to the question."),
    ("top-k", "how many chunks retrieval returns."),
    ("Grounding", "instructing the model to answer only from the retrieved passages."),
    ("Citation", "pointing each claim back to its source document."),
    ("Escalation", "declining and handing off to a human when the answer is not in the docs."),
]:
    story.append(Paragraph(f"<b>{esc(term)}</b> &mdash; {d}",
                           ParagraphStyle("g", parent=body, spaceAfter=4)))

story.append(Spacer(1, 14))
story.append(Paragraph("End of book. Next week's story is how we MEASURED this system &mdash; "
                       "see the companion volume, Evaluating RAG Systems.",
                       ParagraphStyle("end", parent=body, fontName="Helvetica-Oblique",
                                      textColor=ACCENT2)))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "Building a RAG System")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                      topMargin=2.2 * cm, bottomMargin=2.2 * cm)
doc.addPageTemplates([PageTemplate(id="all",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")],
    onPage=footer)])
doc.build(story)
print("WROTE", OUT)
