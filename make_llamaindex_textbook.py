"""Generate a textbook-style PDF on llama_index.core using reportlab."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted,
    Spacer, PageBreak, Table, TableStyle, NextPageTemplate,
)

OUT = "/Users/vamsidhar/Google/ai-journey/notes/llama-index-core-textbook.pdf"

# ---------------------------------------------------------------- styles
ACCENT = colors.HexColor("#1f5673")
ACCENT2 = colors.HexColor("#3a7ca5")
CODEBG = colors.HexColor("#f4f4f2")
CALLBG = colors.HexColor("#eaf2f8")
WARNBG = colors.HexColor("#fdf3e7")

styles = getSampleStyleSheet()

body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=10.5, leading=15, alignment=TA_JUSTIFY,
                      spaceAfter=8)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=20, leading=24, textColor=ACCENT, spaceBefore=6,
                    spaceAfter=12)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=13.5, leading=18, textColor=ACCENT2, spaceBefore=12,
                    spaceAfter=6)
codest = ParagraphStyle("code", parent=styles["Code"], fontName="Courier",
                        fontSize=8, leading=10.5, textColor=colors.HexColor("#222222"))
chap_no = ParagraphStyle("chapno", parent=body, fontName="Helvetica-Bold",
                         fontSize=11, textColor=ACCENT2, spaceAfter=2)
toc_item = ParagraphStyle("toc", parent=body, fontSize=11, leading=18, spaceAfter=2)
title_st = ParagraphStyle("title", parent=styles["Title"], fontName="Helvetica-Bold",
                          fontSize=30, leading=36, textColor=ACCENT, alignment=TA_CENTER)
sub_st = ParagraphStyle("sub", parent=body, fontSize=14, leading=20,
                        alignment=TA_CENTER, textColor=colors.HexColor("#555555"))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def P(text):
    return Paragraph(text, body)


def CODE(text):
    rows = [[Preformatted(text.strip("\n"), codest)]]
    t = Table(rows, colWidths=[16.0 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d0d0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def BOX(text, bg=CALLBG, label="IN OUR PROJECT"):
    inner = Paragraph(
        f'<b>{esc(label)}</b><br/>{text}',
        ParagraphStyle("box", parent=body, fontSize=9.5, leading=13.5))
    t = Table([[inner]], colWidths=[16.0 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT2),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 8)]


story = []


def chapter(num, title):
    story.append(PageBreak())
    story.append(Paragraph(f"CHAPTER {num}", chap_no))
    story.append(Paragraph(esc(title), h1))


def sec(title):
    story.append(Paragraph(esc(title), h2))


def para(text):
    story.append(P(text))


def code(text):
    story.append(CODE(text))
    story.append(Spacer(1, 6))


def callout(text, warn=False):
    story.extend(BOX(text, bg=WARNBG if warn else CALLBG,
                     label="GOTCHA" if warn else "IN OUR PROJECT"))


# ================================================================ COVER
story.append(Spacer(1, 5 * cm))
story.append(Paragraph("LlamaIndex Core", title_st))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("A Practical Textbook for RAG Engineers", sub_st))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("The data model, readers, chunking, embeddings, indexes,<br/>"
                       "storage, retrievers and query engines — with worked examples<br/>"
                       "grounded in a real support-RAG project.", sub_st))
story.append(Spacer(1, 4 * cm))
story.append(Paragraph("Companion to project-01-rag-saas-support", sub_st))

# ================================================================ TOC
story.append(PageBreak())
story.append(Paragraph("Contents", h1))
toc = [
    "1.  What LlamaIndex Core Is (and Isn't)",
    "2.  The Data Model: Documents and Nodes",
    "3.  Loading Data: Readers",
    "4.  Chunking: Node Parsers",
    "5.  Embeddings",
    "6.  Indexes",
    "7.  Storage and Persistence",
    "8.  Retrievers",
    "9.  Query Engines and Response Synthesis",
    "10. Settings: Global Configuration",
    "11. End to End: Building the Pipeline",
    "12. Gotchas, Tuning and Glossary",
]
for item in toc:
    story.append(Paragraph(esc(item), toc_item))

# ============================================================ CH1
chapter(1, "What LlamaIndex Core Is (and Isn't)")
para("LlamaIndex is a framework for connecting large language models (LLMs) to your "
     "own data. The <b>core</b> package — installed as <font name='Courier'>"
     "llama-index-core</font> — contains the framework's machinery: the data "
     "structures, the ingestion pipeline, the indexing and retrieval logic, and the "
     "query engines. It is deliberately <i>model-agnostic</i>: it knows how to "
     "orchestrate a Retrieval-Augmented Generation (RAG) pipeline, but it does not "
     "know how to talk to any specific LLM or embedding provider on its own.")
para("That last point explains the package layout. There is a small core, and then "
     "separate <i>adapter</i> packages for each external service — one for each LLM "
     "provider, one for each embedding provider, one for each vector store. You "
     "install the core plus only the adapters you need.")
code("pip install llama-index-core\n"
     "pip install llama-index-llms-anthropic        # use Claude as the LLM\n"
     "pip install llama-index-embeddings-openai     # use OpenAI embeddings")
callout("Our project uses exactly this split: llama-index-core for the pipeline, "
        "llama-index-llms-anthropic to generate answers with Claude, and "
        "llama-index-embeddings-openai to embed chunks. Three packages, not one "
        "monolith.")
sec("The RAG pipeline in one line")
para("Everything in this book serves a single flow:")
code("raw docs -> clean -> chunk into nodes -> embed -> index\n"
     "          -> retrieve nearest chunks for a query\n"
     "          -> ground an LLM answer in them -> cited answer")
sec("What Core does NOT do")
para("Core does not provide an LLM, an embedding model, or a production vector "
     "database. By default it can use a simple in-memory vector store and will call "
     "out to whichever adapter you configure. It is the conductor, not the orchestra.")

# ============================================================ CH2
chapter(2, "The Data Model: Documents and Nodes")
para("Two classes underpin everything: <b>Document</b> and <b>Node</b> (specifically "
     "<font name='Courier'>TextNode</font>). Understanding the difference is the "
     "single most useful thing in this chapter.")
sec("Document — one whole source")
para("A <b>Document</b> represents one whole piece of source content — typically one "
     "file. It carries the full text plus metadata about where it came from.")
code("from llama_index.core import Document\n\n"
     "doc = Document(\n"
     "    text='Row Level Security is enabled with ALTER TABLE ...',\n"
     "    metadata={'file_name': 'row-level-security.mdx'},\n"
     ")\n"
     "print(doc.text[:50])      # the content\n"
     "print(doc.metadata)       # {'file_name': 'row-level-security.mdx'}\n"
     "print(doc.id_)            # a unique id")
callout("In ingest.py, loading the Supabase docs produced 209 Document objects — one "
        "per .mdx file. A Document is the raw, whole-file unit; it is too big to "
        "retrieve directly.")
sec("Node — one retrievable chunk")
para("A <b>Node</b> is a smaller slice of a Document — a chunk. Retrieval and "
     "embedding operate on Nodes, not Documents, because a whole document embedded "
     "into a single vector blurs its meaning. One Document becomes many Nodes.")
code("# Conceptually:\n"
     "Document (whole file, ~18,000 chars)\n"
     "   -> Node, Node, Node, Node, Node   (chunks of ~512 tokens each)")
sec("Metadata travels — this is how citations work")
para("Crucially, metadata flows from Document to its Nodes and onward into retrieval "
     "results. The <font name='Courier'>file_name</font> captured at load time is "
     "what lets a final answer say \"...according to row-level-security.mdx\". "
     "Citations are free precisely because metadata rides along.")
callout("Document.text is read-only in recent versions. To 'edit' a document (e.g. "
        "after cleaning) you build a NEW Document with the cleaned text rather than "
        "assigning to .text — assigning raises AttributeError: property 'text' has "
        "no setter.", warn=True)

# ============================================================ CH3
chapter(3, "Loading Data: Readers")
para("A <b>Reader</b> turns raw sources (files, web pages, databases) into a list of "
     "Document objects. The workhorse in core is "
     "<font name='Courier'>SimpleDirectoryReader</font>, which walks a folder.")
code("from llama_index.core import SimpleDirectoryReader\n\n"
     "docs = SimpleDirectoryReader(\n"
     "    input_dir='data/corpus',\n"
     "    required_exts=['.md', '.mdx'],   # filter by extension\n"
     "    recursive=True,                  # descend into subfolders\n"
     ").load_data()\n\n"
     "print(type(docs))   # <class 'list'>\n"
     "print(len(docs))    # number of files loaded\n"
     "print(docs[0].metadata['file_path'])")
sec("What load_data() returns")
para("It returns a <font name='Courier'>list[Document]</font> — by default one "
     "Document per file. Each Document's metadata is auto-populated with "
     "<font name='Courier'>file_path, file_name, file_size</font> and timestamps.")
sec("Cleaning at load time")
para("Readers give you raw text — including noise like front-matter and markup. "
     "Cleaning the corpus before indexing matters more than any model choice: "
     "garbage chunks produce confident, wrong, cited answers.")
code("import re\n"
     "from llama_index.core import Document\n\n"
     "def clean(text):\n"
     "    text = re.sub(r'^---\\n.*?\\n---\\n', '', text, flags=re.DOTALL)  # frontmatter\n"
     "    text = re.sub(r'\\{/\\*.*?\\*/\\}', '', text, flags=re.DOTALL)      # mdx comments\n"
     "    return text.strip()\n\n"
     "clean_docs = [\n"
     "    Document(text=clean(d.text), metadata=d.metadata, id_=d.id_)\n"
     "    for d in docs if not d.metadata['file_name'].startswith('_')\n"
     "]")
callout("This is exactly load_documents() in ingest.py: drop '_'-prefixed template "
        "files and strip YAML front-matter + MDX comments before indexing. Result: "
        "210 files -> 209 real documents.")

# ============================================================ CH4
chapter(4, "Chunking: Node Parsers")
para("A <b>Node Parser</b> (also called a splitter) turns Documents into Nodes. The "
     "most common is <font name='Courier'>SentenceSplitter</font>, which splits on "
     "sentence boundaries while targeting a chunk size.")
code("from llama_index.core.node_parser import SentenceSplitter\n\n"
     "splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)\n"
     "nodes = splitter.get_nodes_from_documents(docs)\n"
     "print(len(nodes))            # many more nodes than docs\n"
     "print(nodes[0].get_content())")
sec("chunk_size and chunk_overlap")
para("<b>chunk_size</b> is the target number of tokens per chunk. Smaller chunks give "
     "more precise retrieval (you fetch the exact paragraph) but more fragments; "
     "larger chunks carry more context per hit but match more fuzzily. "
     "<b>chunk_overlap</b> repeats a few tokens across the boundary so an idea "
     "spanning two chunks is not cut in half.")
callout("We chose chunk_size=512, chunk_overlap=50. That turned 209 documents into "
        "1,137 nodes — about five chunks per document on average. These numbers are a "
        "starting point, not a law; Chapter 12 covers tuning them with evaluation.")
sec("The tradeoff, visually")
para("Think of chunk size as a dial between precision and context:")
code("small chunks  ->  precise retrieval, less context per hit, more fragments\n"
     "large chunks  ->  more context per hit, fuzzier matching, fewer fragments")

# ============================================================ CH5
chapter(5, "Embeddings")
para("An <b>embedding</b> turns a piece of text into a vector — a list of numbers "
     "that captures its meaning. Texts with similar meaning land near each other in "
     "vector space. This is the mechanism that makes 'find relevant chunks' a "
     "math problem: embed the query the same way, then find the nearest chunk "
     "vectors by cosine similarity.")
code("from llama_index.embeddings.openai import OpenAIEmbedding\n\n"
     "embed = OpenAIEmbedding(model='text-embedding-3-small')  # 1536 dimensions\n"
     "vec = embed.get_text_embedding('How do I enable RLS?')\n"
     "print(len(vec))   # 1536 numbers")
sec("Two models, two jobs")
para("This is the most important idea in RAG. There are two different models doing "
     "two different things, and blurring them is the classic beginner mistake.")
data = [["Role", "Model (our project)", "Job"],
        ["Embedding model", "text-embedding-3-small", "text -> vectors, for FINDING chunks"],
        ["Generation model", "claude-opus-4-8", "read chunks -> WRITE the answer"]]
t = Table(data, colWidths=[3.2 * cm, 5.0 * cm, 7.8 * cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), ACCENT2),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 8))
para("<b>Embeddings find; the LLM answers.</b> If you remember one sentence from "
     "this book, make it that one.")
callout("The embedding model used to retrieve MUST be the same one used to index. "
        "Query vectors and chunk vectors are only comparable if produced by the same "
        "model. Mismatching them yields nonsense rankings with no error message.",
        warn=True)

# ============================================================ CH6
chapter(6, "Indexes")
para("An <b>Index</b> ties chunks and their embeddings together into a searchable "
     "structure. The default and most common is "
     "<font name='Courier'>VectorStoreIndex</font>, which stores each node's vector "
     "and supports nearest-neighbour search.")
code("from llama_index.core import VectorStoreIndex\n"
     "from llama_index.core.node_parser import SentenceSplitter\n\n"
     "index = VectorStoreIndex.from_documents(\n"
     "    docs,\n"
     "    transformations=[SentenceSplitter(chunk_size=512, chunk_overlap=50)],\n"
     "    show_progress=True,\n"
     ")")
sec("from_documents does a lot")
para("That single call runs the whole back half of ingestion: it applies the "
     "transformations (chunking), embeds every resulting node with the configured "
     "embedding model, and stores the vectors in the index. This convenience is the "
     "reason a framework saves time — and the reason you should understand each step "
     "it hides.")
callout("Building our index embedded all 1,137 chunks via text-embedding-3-small in "
        "roughly 17 seconds, for about one to two cents. The embedding cost is "
        "proportional to total tokens in the corpus.")

# ============================================================ CH7
chapter(7, "Storage and Persistence")
para("Embedding is the expensive step, so you do not want to repeat it on every run. "
     "<b>Persistence</b> writes the index to disk; loading it back skips re-embedding.")
code("# Persist after building\n"
     "index.storage_context.persist(persist_dir='storage')")
para("This writes several JSON files: the vector store (the embeddings), the doc "
     "store (chunk text and metadata), and the index store (structure).")
sec("Loading a persisted index")
para("To reload, rebuild a <font name='Courier'>StorageContext</font> from the "
     "directory and call <font name='Courier'>load_index_from_storage</font>. You "
     "must configure the same embedding model first, because any new query will be "
     "embedded with it.")
code("from llama_index.core import (\n"
     "    Settings, StorageContext, load_index_from_storage)\n"
     "from llama_index.embeddings.openai import OpenAIEmbedding\n\n"
     "Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')\n"
     "ctx = StorageContext.from_defaults(persist_dir='storage')\n"
     "index = load_index_from_storage(ctx)")
callout("retrieve.py loads the persisted index once and caches it in a module-level "
        "variable, so repeated queries in one process don't reload from disk. The "
        "storage/ folder is git-ignored — it's a regenerable build artifact.")

# ============================================================ CH8
chapter(8, "Retrievers")
para("A <b>Retriever</b> takes a query string and returns the most relevant nodes. "
     "Get one from an index with <font name='Courier'>as_retriever</font>.")
code("retriever = index.as_retriever(similarity_top_k=5)\n"
     "results = retriever.retrieve('How do I enable row level security?')\n\n"
     "for r in results:\n"
     "    print(r.score, r.node.metadata['file_name'])\n"
     "    print(r.node.get_content()[:120])")
sec("similarity_top_k and scores")
para("<b>similarity_top_k</b> is how many chunks to return. Each result is a "
     "<font name='Courier'>NodeWithScore</font>: the node plus a similarity score "
     "where 1.0 means identical meaning. The score is your signal for relevance.")
callout("On 'how do I enable RLS?' our top hit scored about 0.69; on an unrelated "
        "billing request the best score was about 0.30. That low score is the signal "
        "the system uses to decide it should escalate rather than answer — see "
        "Chapter 9.")

# ============================================================ CH9
chapter(9, "Query Engines and Response Synthesis")
para("A <b>Query Engine</b> combines retrieval and generation: it retrieves chunks, "
     "stuffs them into a prompt, and asks an LLM to answer. The one-call convenience "
     "form is <font name='Courier'>as_query_engine</font>.")
code("from llama_index.llms.anthropic import Anthropic\n\n"
     "engine = index.as_query_engine(\n"
     "    llm=Anthropic(model='claude-opus-4-8'),\n"
     "    similarity_top_k=5,\n"
     ")\n"
     "resp = engine.query('How do I enable RLS?')\n"
     "print(resp)                 # the answer text\n"
     "print(resp.source_nodes)    # the chunks it used (for citations)")
sec("Framework convenience vs. explicit control")
para("The query engine is fast to write but hides the prompt — and the prompt is "
     "where grounding and citations live. For maximum control you can split the "
     "concern: use the framework only to retrieve, then call the LLM yourself with a "
     "prompt you write explicitly.")
code("# What generate.py does: retrieve via framework, generate via raw SDK\n"
     "nodes = retriever.retrieve(query)\n"
     "context = format_with_numbered_sources(nodes)\n"
     "# then call Claude with a system prompt that says:\n"
     "#   'answer ONLY from the context, cite [n], escalate if not present'")
callout("We deliberately use the framework for retrieval but the raw Anthropic SDK "
        "for generation. The grounding prompt is the most important, most-tunable "
        "part of the system; writing it explicitly keeps it visible and under our "
        "control instead of buried inside as_query_engine().")

# ============================================================ CH10
chapter(10, "Settings: Global Configuration")
para("<font name='Courier'>Settings</font> is a global object that holds default "
     "components — the embedding model, the LLM, the node parser, the chunk size — so "
     "you don't pass them to every call. Set it once at startup.")
code("from llama_index.core import Settings\n"
     "from llama_index.embeddings.openai import OpenAIEmbedding\n"
     "from llama_index.core.node_parser import SentenceSplitter\n\n"
     "Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')\n"
     "Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)")
para("Components fall back to Settings when not passed explicitly. This is convenient "
     "but has a sharp edge: if you forget to set "
     "<font name='Courier'>Settings.embed_model</font> before loading an index, "
     "LlamaIndex may fall back to a default embedding provider and fail or mismatch.")
callout("Both ingest.py and retrieve.py set Settings.embed_model to the SAME model. "
        "That consistency is what keeps query vectors comparable to chunk vectors.",
        warn=False)

# ============================================================ CH11
chapter(11, "End to End: Building the Pipeline")
para("Here is the whole pipeline assembled from the pieces in this book — the "
     "skeleton of our project, condensed.")
sec("Ingest: build and persist the index")
code("from llama_index.core import (Settings, SimpleDirectoryReader,\n"
     "                              VectorStoreIndex)\n"
     "from llama_index.core.node_parser import SentenceSplitter\n"
     "from llama_index.embeddings.openai import OpenAIEmbedding\n\n"
     "Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')\n"
     "docs = SimpleDirectoryReader('data/corpus', required_exts=['.mdx'],\n"
     "                             recursive=True).load_data()\n"
     "# (clean docs here — Chapter 3)\n"
     "index = VectorStoreIndex.from_documents(\n"
     "    docs, transformations=[SentenceSplitter(512, 50)], show_progress=True)\n"
     "index.storage_context.persist('storage')")
sec("Query: load, retrieve, generate")
code("from llama_index.core import (Settings, StorageContext,\n"
     "                              load_index_from_storage)\n"
     "from llama_index.embeddings.openai import OpenAIEmbedding\n\n"
     "Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')\n"
     "ctx = StorageContext.from_defaults(persist_dir='storage')\n"
     "index = load_index_from_storage(ctx)\n"
     "nodes = index.as_retriever(similarity_top_k=5).retrieve(question)\n"
     "# build a grounded prompt from nodes, then call your LLM")
para("That is a complete RAG system. Everything else — better cleaning, smarter "
     "chunking, hybrid retrieval, evaluation — is refinement on this spine.")

# ============================================================ CH12
chapter(12, "Gotchas, Tuning and Glossary")
sec("Gotchas worth memorising")
para("<b>1. Document.text is read-only.</b> Build a new Document to change text.")
para("<b>2. The embedding model must match</b> between indexing and querying.")
para("<b>3. Set Settings.embed_model before loading an index</b>, or you may hit a "
     "default provider and an error.")
para("<b>4. Persist after building</b> so you don't pay to re-embed every run.")
para("<b>5. Clean the corpus first.</b> Templates and markup noise produce confident "
     "wrong answers. Retrieval quality is mostly a data problem.")
sec("Tuning levers")
para("When retrieval is weak (low scores on questions that should be answerable), "
     "reach for these in roughly this order: adjust <b>chunk_size</b> / "
     "<b>chunk_overlap</b>; raise <b>similarity_top_k</b>; improve corpus cleaning; "
     "try a <b>hybrid retriever</b> (keyword + vector) for term-heavy queries; or "
     "rephrase queries. Always measure before and after — never tune by vibes.")
sec("Glossary")
for term, deftext in [
    ("Document", "One whole source item (usually a file); the raw, pre-chunk unit."),
    ("Node / TextNode", "A chunk of a Document; the unit that gets embedded and retrieved."),
    ("Reader", "Turns raw sources into a list of Documents (e.g. SimpleDirectoryReader)."),
    ("Node Parser / Splitter", "Turns Documents into Nodes (e.g. SentenceSplitter)."),
    ("Embedding", "A vector capturing a text's meaning; similar meaning -> nearby vectors."),
    ("Index", "Searchable structure over node embeddings (e.g. VectorStoreIndex)."),
    ("StorageContext", "Handle to a persisted index on disk."),
    ("Retriever", "Returns the top-k most similar nodes for a query."),
    ("Query Engine", "Retrieval + generation in one object (as_query_engine)."),
    ("Settings", "Global defaults: embed model, LLM, node parser."),
    ("Cosine similarity", "Closeness measure between two vectors; 1.0 = identical meaning."),
]:
    story.append(Paragraph(f"<b>{esc(term)}</b> — {esc(deftext)}",
                           ParagraphStyle("g", parent=body, spaceAfter=4)))

story.append(Spacer(1, 16))
story.append(Paragraph("End of book. Now go re-read your own under-the-hood.md and "
                       "explain each of these in your own words — that is how it "
                       "sticks.", ParagraphStyle("end", parent=body,
                       fontName="Helvetica-Oblique", textColor=ACCENT2)))


# ---------------------------------------------------------------- build
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "LlamaIndex Core — A Practical Textbook")
    canvas.drawRightString(19 * cm, 1.2 * cm, f"{doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                      topMargin=2.2 * cm, bottomMargin=2.2 * cm)
frame = Frame(doc.leftMargin, doc.bottomMargin,
              doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])
doc.build(story)
print("WROTE", OUT)
