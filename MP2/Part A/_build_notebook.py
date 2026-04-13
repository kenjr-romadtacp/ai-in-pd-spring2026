"""
Build script for MP2 Part A: The Information Problem — Building a RAG Pipeline
Generates MP2_PartA_The_Information_Problem.ipynb using nbformat.

Run from the repo root or from MP2/Part A/:
    python "MP2/Part A/_build_notebook.py"
"""

import sys
import os

# Ensure we can import sibling data modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from _data_paper import ATTENTION_PAPER_TEXT

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def md(source: str) -> nbformat.NotebookNode:
    """Create a markdown cell, auto-dedenting."""
    import textwrap
    return new_markdown_cell(textwrap.dedent(source).strip())


def code(source: str) -> nbformat.NotebookNode:
    """Create a code cell, auto-dedenting."""
    import textwrap
    return new_code_cell(textwrap.dedent(source).strip())


cells: list[nbformat.NotebookNode] = []

# ═══════════════════════════════════════════════════════════════════════════
# HEADER / INTRODUCTION
# ═══════════════════════════════════════════════════════════════════════════

cells.append(md("""\
    # The Information Problem — Building a RAG Pipeline
    ## ME 493B — AI in Product Development | Mini-Project 2, Part A

    **Instructor:** Scott Thielman, PhD — University of Washington Bothell
    **Due:** Monday, April 27, 2026 at 11:59 PM
    **Time estimate:** 60–90 minutes
    **Points:** 50 (Part A). Part B is worth 50 points separately.

    ---

    ### The problem you're solving

    In Sessions 5 and 6, you experienced the information problem firsthand. Your AI
    assistant knew about aeroelastic coupling *in general* but not your client's specific
    flutter margin data. It could discuss tolerance analysis *abstractly* but couldn't
    tell you which tolerances your predecessor specified for the CardioSense enclosure.

    **RAG (Retrieval-Augmented Generation)** solves this. Instead of hoping the model
    "knows" your data, you *inject* the relevant documents into the prompt at query time.
    In this notebook, you build a RAG pipeline from scratch.

    ### How this notebook works

    Unlike MP1, **you write the code.** Each section describes what to build — the
    concepts, the steps, the expected outputs. Use GitHub Copilot, Claude, ChatGPT, or
    any AI coding tool to help. The learning is in understanding *what* you're building
    and evaluating *whether* it works.

    **Cell conventions:**
    - Pre-written cells: Setup and data loading only (Section 0)
    - Empty code cells: You implement, guided by the instructions above each cell
    - **[X pts]** tags: Point value and expected output for grading

    ### Grading summary (50 pts)

    | Section | Points | What the grader checks |
    |---------|--------|----------------------|
    | 1. Tokens & Context Windows | 8 | Token counts printed, budget calculation correct |
    | 2. Embeddings for Retrieval | 8 | Ranked results with scores, answer extraction attempted |
    | 3. Chunking Tradeoffs | 8 | Comparison table across 3 chunk sizes, best size identified |
    | 4. RAG Pipeline | 10 | ChromaDB collection created, 5 queries run, accuracy reported |
    | 5. Capstone (Attention paper) | 8 | 4 queries answered with retrieved evidence |
    | 6. Reflections | 8 | Three thoughtful reflections (2–3 sentences each) |
    | **Total** | **50** | |

    ### Building blocks from MP1

    This notebook builds directly on three of the five building blocks you learned in MP1:

    | Building Block | MP1 | MP2 Part A |
    |---|---|---|
    | **Representation** | Hand-crafted feature vectors, then learned embeddings | Embedding entire *documents* for retrieval |
    | **Similarity** | Cosine similarity between individual vectors | Cosine similarity to rank documents against a query |
    | **Search & Retrieval** | Mini search engine over 12 sentences | Full RAG pipeline over 20 documents + a research paper |
"""))

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 0: SETUP
# ═══════════════════════════════════════════════════════════════════════════

cells.append(md("""\
    ---
    ## Section 0: Setup

    Run the cells below to install dependencies, import libraries, and load the
    document corpus. **These are the only pre-written code cells in the notebook** —
    everything else is yours to build.

    The document corpus for this notebook lives in the `corpus/` folder alongside
    this notebook — 20 text files from Ridgeline Engineering Partners, a fictional
    mechanical engineering consultancy. A `manifest.json` file maps each filename to
    its document ID, title, and type. The setup cell reads all of these automatically.

    This is how real RAG systems work: your documents live as files on disk (or in a
    database), and your pipeline loads and processes them programmatically.
"""))

# --- Setup cell 1: Installs and imports ---
cells.append(code("""\
    # ============================================================
    # SETUP — Run this cell first (pre-written, do not modify)
    # ============================================================

    # Install additional packages (not in base requirements.txt)
    import subprocess, sys
    for pkg in ["tiktoken", "chromadb", "openai"]:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", pkg],
            stdout=subprocess.DEVNULL
        )

    # Core imports
    import numpy as np
    import pandas as pd
    import tiktoken
    import chromadb
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import textwrap, os, time

    # Load the embedding model (same one you used in MP1 Section 5)
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Setup complete.")
    print(f"  numpy {np.__version__}")
    print(f"  pandas {pd.__version__}")
    print(f"  tiktoken {tiktoken.__version__}")
    print(f"  chromadb {chromadb.__version__}")
    print(f"  Embedding model: all-MiniLM-L6-v2 (384-dim)")
"""))

# --- Setup cell 2: Document corpus (loaded from corpus/ folder) ---
cells.append(code("""\
    # Load document corpus from the corpus/ folder
    # Each .txt file is one document; manifest.json maps filenames to metadata
    import json, pathlib

    corpus_dir = pathlib.Path("corpus")
    if not corpus_dir.exists():
        # Handle running from repo root vs. from notebook directory
        corpus_dir = pathlib.Path("MP2/Part A/corpus")

    with open(corpus_dir / "manifest.json", encoding="utf-8") as f:
        manifest = json.load(f)

    documents = []
    for entry in manifest:
        filepath = corpus_dir / entry["filename"]
        text = filepath.read_text(encoding="utf-8")
        documents.append({
            "id": entry["id"],
            "title": entry["title"],
            "type": entry["type"],
            "text": text,
        })

    print(f"Loaded {len(documents)} documents | Total characters: {sum(len(d['text']) for d in documents)}")
    print(f"Source: {corpus_dir.resolve()}")
    print()
    for doc in documents[:5]:
        print(f"  {doc['id']}: {doc['title']} ({len(doc['text'])} chars)")
    print(f"  ... and {len(documents) - 5} more")
"""))

# --- Setup cell 3: Attention paper text ---
escaped_paper = ATTENTION_PAPER_TEXT.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
paper_lines = [
    '# "Attention Is All You Need" — abridged educational summary',
    '# Vaswani et al., NeurIPS 2017. Full paper: https://arxiv.org/abs/1706.03762',
    f'attention_paper = """{escaped_paper}"""',
    "",
    'print(f"Paper loaded: {len(attention_paper)} characters")',
]
cells.append(code("\n".join(paper_lines)))


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: TOKENS AND CONTEXT WINDOWS
# ═══════════════════════════════════════════════════════════════════════════

cells.append(md("""\
    ---
    ## Section 1: Tokens and Context Windows [8 pts]

    Before you can manage context, you need to understand the **budget**. Every language
    model has a finite context window measured in tokens — not words, not characters,
    but *tokens*. Your job as an engineer using AI is to ensure the right information
    fits within that budget.

    ### What are tokens?

    A token is the fundamental unit a language model reads and generates. Most modern
    models use **subword tokenization** — common words like "the" or "engineering" map
    to a single token, while rare or technical words get split into pieces. For example,
    "aeroelastic" might become ["aero", "elastic"], using two tokens. The tokenizer
    `cl100k_base` is used by GPT-4-class models (and is representative of how
    Claude-class models tokenize as well).

    Different models use different tokenizers, so the same text produces different token
    counts depending on which model you're targeting. The context window is a **hard
    budget** — not a suggestion. If your prompt exceeds it, the API returns an error.

    ### What to build

    1. Create a `tiktoken` encoder using the `cl100k_base` encoding
    2. Tokenize one of the Ridgeline documents — print the raw text, the token list
       (first 20 tokens), and the total token count
    3. Tokenize **all 20 documents**. Build and print a summary table (DataFrame):
       document ID, title, character count, token count
    4. Calculate: if the context window is 8,192 tokens and you reserve 1,000 for the
       question + answer, how many documents can you fit in the remaining 7,192 tokens?
       Iterate through documents sorted by token count (smallest first) and pack as many
       as fit. Print the count and remaining tokens.

    ### Key concepts

    - Tokens are not words — subword tokenization splits rare words and joins common ones
    - The ratio of characters-to-tokens is typically 3–5 for English text
    - Context window is a hard constraint, not a suggestion
    - **This is why we need retrieval** — you can't paste all 20 documents into a prompt

    ### Reference links

    - [Tiktokenizer](https://tiktokenizer.vercel.app/) — paste text and see tokens interactively
    - [Anthropic Context Windows](https://docs.anthropic.com/en/docs/about-claude/models) — see how context windows vary by model

    ### What to submit [8 pts]

    Print these exact outputs (the grader checks for them):

    ```
    Document DOC-001: {N} characters → {M} tokens (ratio: {N/M:.1f} chars/token)
    ```

    A summary table of all 20 documents with columns: ID, Title, Characters, Tokens

    ```
    At 8,192 token context window with 1,000 reserved: {X} documents fit fully, {Y} tokens remaining
    ```

    > **Forward connection:** You can't paste all 20 documents into a prompt. That's why
    > we need retrieval — finding the RIGHT documents for each question.
"""))

cells.append(code("""\
    # Your code here — see instructions above
    # Step 1: Create a tiktoken encoder (cl100k_base)
    # Step 2: Tokenize DOC-001, print text, first 20 tokens, and count
    # Expected output: "Document DOC-001: {N} characters → {M} tokens (ratio: {N/M:.1f} chars/token)"
"""))

cells.append(code("""\
    # Your code here — tokenize all 20 documents
    # Build a pandas DataFrame with columns: ID, Title, Characters, Tokens
    # Print the full table
"""))

cells.append(code("""\
    # Your code here — context window budget calculation
    # Context window: 8,192 tokens. Reserve 1,000 for question + answer.
    # How many documents fit in the remaining 7,192 tokens? (pack smallest-first)
    # Expected output: "At 8,192 token context window with 1,000 reserved: {X} documents fit fully, {Y} tokens remaining"
"""))


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: EMBEDDINGS FOR DOCUMENT RETRIEVAL
# ═══════════════════════════════════════════════════════════════════════════

cells.append(md("""\
    ---
    ## Section 2: Embeddings for Document Retrieval [8 pts]

    You used embeddings in MP1 to measure similarity between individual sentences. Now
    apply the same idea at document scale: embed each document, embed a query, and find
    the most relevant documents by cosine similarity.

    The model is the same `all-MiniLM-L6-v2` you used in MP1 Section 5 — it maps any
    text to a 384-dimensional vector. Cosine similarity (MP1 Section 2) measures how
    closely two vectors point in the same direction, regardless of magnitude.

    ### What to build

    1. Embed all 20 document texts using `embedding_model.encode()` — you'll get a
       (20, 384) matrix
    2. Embed the query: `"What is the standard billing rate for senior engineers?"`
    3. Compute cosine similarity between the query embedding and all 20 document embeddings
       (use `sklearn.metrics.pairwise.cosine_similarity`)
    4. Print a ranked list: top 5 documents by similarity, with their scores
    5. Read the top-ranked document text — does it contain the answer? Print what you find.
    6. Run a second, harder query: `"What rating factor was found for the interior girders on the bridge project?"`
       Repeat steps 3–5 for this query.

    ### Key concepts

    - This is the same cosine similarity from MP1 Section 2, now applied to real documents
    - Embedding quality depends on the model — `all-MiniLM-L6-v2` was trained on semantic
      similarity tasks (sentence pairs), so it captures meaning, not just keywords
    - Whole-document embeddings work for short documents but lose detail for long ones —
      a 500-word document about five different topics gets one "averaged" embedding that
      may not match any specific fact well. This motivates chunking (Section 3).

    ### Reference links

    - [Sentence-Transformers documentation](https://www.sbert.net/)
    - [MTEB Benchmark Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) — compare embedding models

    ### What to submit [8 pts]

    For **each** of the two queries, print:

    ```
    Query: '{query text}'
    Top match: DOC-{XXX} '{title}' (similarity: {score:.4f})
    ```

    Ranked list of top 5 documents with similarity scores.

    For the top match, print either:
    ```
    Answer found in document: {the specific answer}
    ```
    or:
    ```
    Answer NOT found in top document — [your explanation of why]
    ```
"""))

cells.append(code("""\
    # Your code here — embed all 20 documents
    # Step 1: Embed document texts → (20, 384) matrix
    # Step 2: Embed query: "What is the standard billing rate for senior engineers?"
    # Step 3: Compute cosine similarity, rank, print top 5
    # Expected output: ranked list with similarity scores, answer extraction
"""))

cells.append(code("""\
    # Your code here — second query (harder)
    # Query: "What rating factor was found for the interior girders on the bridge project?"
    # Embed, compute similarity, rank top 5, extract answer
    # Does whole-document embedding find the right document? Why or why not?
"""))


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: CHUNKING AND ITS CONSEQUENCES
# ═══════════════════════════════════════════════════════════════════════════

cells.append(md("""\
    ---
    ## Section 3: Chunking and Its Consequences [8 pts]

    Whole-document embeddings lose specificity for long documents. A document covering
    five topics gets one "averaged" vector that poorly represents any individual fact.
    **Chunking** breaks documents into smaller pieces so each embedding is more focused.

    But chunk size is an engineering tradeoff — exactly like mesh density in FEA
    (Session 6, slide 13):

    | Chunk too small | Chunk too large |
    |---|---|
    | Lose context between related sentences | Dilute specific facts with surrounding noise |
    | A chunk saying "0.73" without "rating factor" or "interior girders" is useless | Similarity score drops because the embedding averages over irrelevant text |

    **Overlap** helps: facts that span a chunk boundary are captured in both the
    overlapping chunks.

    ### What to build

    1. Write a chunking function: `chunk_text(text, chunk_size, overlap)` that splits
       text into chunks of `chunk_size` characters with `overlap` characters of overlap.
       Each chunk should also carry metadata about its source document.
    2. Chunk all 20 documents at three sizes: **200**, **500**, and **1000** characters
       (use overlap = 20% of chunk_size: 40, 100, 200 respectively)
    3. For each chunk size, print: total chunks created, average chunk length in
       characters, smallest chunk, largest chunk
    4. Re-embed ALL chunks at each size and re-run the two queries from Section 2
    5. Compare: which chunk size retrieves the most relevant chunk? Build a comparison
       table showing chunk_size | num_chunks | query_1_top_score | query_2_top_score

    ### Key concepts

    - Chunking is an engineering tradeoff — not a parameter you optimize once and forget
    - Smaller chunks = more precise retrieval but risk losing context
    - Larger chunks = more context per result but diluted similarity scores
    - Overlap prevents losing facts that fall on chunk boundaries
    - The "right" chunk size depends on your documents and your questions

    ### Reference links

    - [LangChain Text Splitters](https://docs.langchain.com/oss/javascript/integrations/splitters/index) — chunking strategies (JS examples, concepts are universal)
    - [Greg Kamradt's Chunking Visualization](https://github.com/FullStackRetrieval-com/RetrievalTutorials) — visual intuition

    ### What to submit [8 pts]

    Comparison table:

    ```
    chunk_size | num_chunks | query_1_top_score | query_2_top_score
    200        | ...        | ...               | ...
    500        | ...        | ...               | ...
    1000       | ...        | ...               | ...
    ```

    ```
    Best chunk size for query 1: {size} chars (score: {score:.4f})
    Best chunk size for query 2: {size} chars (score: {score:.4f})
    ```

    Print the actual text of the top-retrieved chunk for each query at the best chunk
    size — visually confirm it contains the answer.
"""))

cells.append(code("""\
    # Your code here — implement the chunking function
    # def chunk_text(text, chunk_size, overlap):
    #     \"\"\"Split text into chunks of chunk_size characters with overlap.\"\"\"
    #     ...
    #     return list_of_chunks
"""))

cells.append(code("""\
    # Your code here — chunk all 20 documents at 3 sizes (200, 500, 1000)
    # For each size, print: total chunks, avg length, min length, max length
"""))

cells.append(code("""\
    # Your code here — embed all chunks and re-run both queries
    # Query 1: "What is the standard billing rate for senior engineers?"
    # Query 2: "What rating factor was found for the interior girders on the bridge project?"
    # Build comparison table: chunk_size | num_chunks | query_1_top_score | query_2_top_score
    # Print best chunk size for each query
    # Print the text of the top-retrieved chunk at the best size for each query
"""))


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: BUILDING THE RAG PIPELINE
# ═══════════════════════════════════════════════════════════════════════════

cells.append(md("""\
    ---
    ## Section 4: Building the RAG Pipeline [10 pts]

    Now assemble the full pipeline: chunk documents → embed chunks → store in a vector
    database → query → retrieve relevant chunks → generate a grounded answer. This is
    the machinery behind every AI system that uses your data.

    ### The RAG stack

    | Component | Tool | Why |
    |-----------|------|-----|
    | Embedding | `all-MiniLM-L6-v2` | Local, fast, no API key needed |
    | Vector store | ChromaDB | Handles storage + similarity search — you don't compute cosine manually against every chunk |
    | Generation | GitHub Models API (`openai` SDK) | Free for GitHub accounts, OpenAI-compatible |

    **ChromaDB** is the vector store from the RAG pipeline diagram in Session 6 (slide 12):
    documents → chunk & embed → **vector store** → query → retrieve → generate.
    It handles embedding storage and nearest-neighbor search efficiently.

    **GitHub Models API** provides free access to models like GPT-4o via the `openai`
    Python SDK — same SDK, just a different base URL. You'll use your existing GitHub
    Personal Access Token (PAT).

    ### Setting up your GitHub PAT

    You need a **fine-grained** GitHub Personal Access Token with Models permission:

    1. Go to [github.com/settings/tokens?type=beta](https://github.com/settings/tokens?type=beta)
    2. Click **"Generate new token"** (this page defaults to fine-grained tokens —
       do **not** use classic tokens)
    3. Give it a name (e.g., "ME493B Models") and set expiration
    4. Under **Permissions → Account permissions → Models**, select **"Read"**
    5. Click "Generate token" and **copy the token immediately** — you won't see
       it again

    ### Storing your token in a `.env` file

    Your token goes in a `.env` file in the root of your repository. This file is
    already listed in `.gitignore`, so it won't be committed or shared.

    **If you don't have a `.env` file yet:** ask Copilot! Open Copilot Chat and type:
    *"Create a .env file in my repo root with a GITHUB_TOKEN variable."* It will
    generate the file for you — just paste in your actual token value.

    The `.env` file should look like this:
    ```
    GITHUB_TOKEN=github_pat_your_token_here
    ```

    The setup cell below loads the token from `.env` automatically.

    **Rate limits:** GitHub Models free tier is rate-limited (~10 requests/min for
    GPT-4o, ~50/day). This is enough for the exercises. If you hit limits, wait a minute
    or switch to another model (e.g., `openai/gpt-4o-mini`).

    ### What to build

    1. Choose a chunk size based on your Section 3 results — justify your choice in a
       comment
    2. Chunk all documents at that size
    3. Create a ChromaDB collection and add all chunks with embeddings and metadata
       (source document ID, title, chunk index)
    4. Write `query_rag(question, n_results=3)`: embed the question, query ChromaDB,
       return top-N chunks with metadata
    5. Write `generate_answer(question, retrieved_chunks)`: format chunks into a prompt,
       call GitHub Models API, return the answer. The prompt must instruct the model to:
       - Answer ONLY based on the provided context
       - Cite which chunk(s) it used
       - Say "I don't have enough information" if the context doesn't contain the answer
    6. Test the full pipeline with **5 queries** (3 provided + 2 you create):
       - "How many engineers work in the Seattle office?"
       - "What material was used for the CardioSense enclosure?"
       - "How many hours of continuing education are required annually?"
       - *(your query 1)*
       - *(your query 2)*

    ### Key concepts

    - A vector database (ChromaDB) replaces manual cosine similarity — it indexes
      embeddings and returns nearest neighbors efficiently
    - **Metadata** (source document, chunk index) is critical — you need to know WHERE
      the answer came from, not just what it says
    - The **generation prompt** matters: without "answer only from context," the model
      will hallucinate from training data instead of your documents
    - This is what Claude's web search, Copilot's codebase search, and enterprise RAG
      platforms do at scale

    ### Reference links

    - [ChromaDB Getting Started](https://docs.trychroma.com/docs/overview/getting-started)
    - [GitHub Models Quickstart](https://docs.github.com/en/github-models/quickstart)

    ### What to submit [10 pts]

    ```
    ChromaDB collection created: {N} chunks indexed
    ```

    For each of 5 queries, print:
    ```
    Question: {question}
    Retrieved chunks:
      1. [{source_doc_id}] {first 100 chars of chunk}...
      2. [{source_doc_id}] {first 100 chars of chunk}...
      3. [{source_doc_id}] {first 100 chars of chunk}...
    Generated answer: {answer from GitHub Models}
    Answer correct: [yes/no]. Ground truth: {expected answer}
    ```

    ```
    RAG pipeline accuracy: {X}/5 queries answered correctly
    ```
"""))

cells.append(code("""\
    # --- GitHub PAT Setup ---
    # Loads your token from a .env file in your repo root.
    # If you don't have a .env file yet, ask Copilot to create one!
    # Your .env should contain:   GITHUB_TOKEN=github_pat_your_token_here

    import os

    # Look for .env in repo root (handles running from notebook dir or repo root)
    for _env_dir in [os.path.abspath(""), os.path.abspath(".."), os.path.abspath("../..") ]:
        _env_path = os.path.join(_env_dir, ".env")
        if os.path.exists(_env_path):
            with open(_env_path) as _f:
                for _line in _f:
                    _line = _line.strip()
                    if _line and not _line.startswith("#") and "=" in _line:
                        _key, _val = _line.split("=", 1)
                        os.environ[_key.strip()] = _val.strip()
            break

    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
    if not GITHUB_TOKEN:
        print("⚠️  GITHUB_TOKEN not found. The generation cells in Section 4 will fail.")
        print()
        print("To fix this:")
        print("  1. Create a .env file in your repo root (ask Copilot if you need help)")
        print("  2. Add this line:  GITHUB_TOKEN=github_pat_your_token_here")
        print("  3. Re-run this cell")
    else:
        print(f"✅ GitHub token loaded ({len(GITHUB_TOKEN)} chars)")

    # Helper: API call with retry logic for rate limits
    from openai import OpenAI

    github_client = OpenAI(
        base_url="https://models.github.ai/inference",
        api_key=GITHUB_TOKEN,
    )

    def call_github_model(messages, model="openai/gpt-4o", max_retries=3):
        \"\"\"Call GitHub Models API with retry logic for rate limits.\"\"\"
        for attempt in range(max_retries):
            try:
                response = github_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=500,
                )
                return response.choices[0].message.content
            except Exception as e:
                if "rate" in str(e).lower() and attempt < max_retries - 1:
                    wait = 15 * (attempt + 1)
                    print(f"  Rate limited. Waiting {wait}s... (attempt {attempt+1}/{max_retries})")
                    time.sleep(wait)
                else:
                    raise
        return None

    print("GitHub Models client ready.")
    print("Note: Free tier rate limits apply (~10 req/min, ~50 req/day for GPT-4o).")
    print("If rate-limited, wait or switch model: e.g., 'openai/gpt-4o-mini'")
"""))

cells.append(code("""\
    # Your code here — Step 1-3: Chunk documents, create ChromaDB collection
    # Choose your chunk size from Section 3 results. Justify in a comment.
    # Create a ChromaDB collection, add all chunks with embeddings and metadata.
    # Expected output: "ChromaDB collection created: {N} chunks indexed"
"""))

cells.append(code("""\
    # Your code here — Step 4: Write query_rag function
    # def query_rag(question, n_results=3):
    #     \"\"\"Embed question, query ChromaDB, return top-N chunks with metadata.\"\"\"
    #     ...
"""))

cells.append(code("""\
    # Your code here — Step 5: Write generate_answer function
    # def generate_answer(question, retrieved_chunks):
    #     \"\"\"Format chunks into a prompt, call GitHub Models API, return answer.\"\"\"
    #     # The prompt should instruct the model to:
    #     #   - Answer ONLY from the provided context
    #     #   - Cite which chunk(s) it used
    #     #   - Say "I don't have enough information" if context is insufficient
    #     ...
"""))

cells.append(code("""\
    # Your code here — Step 6: Test the full RAG pipeline with 5 queries
    # 3 provided queries:
    #   "How many engineers work in the Seattle office?"
    #   "What material was used for the CardioSense enclosure?"
    #   "How many hours of continuing education are required annually?"
    # 2 queries you create (pick facts from the documents you know are there)
    #
    # For each query print: question, top-3 chunks (first 100 chars), source doc IDs,
    # generated answer, and your assessment (correct yes/no, ground truth)
    #
    # Final line: "RAG pipeline accuracy: {X}/5 queries answered correctly"
"""))


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: CAPSTONE — QUERYING "ATTENTION IS ALL YOU NEED"
# ═══════════════════════════════════════════════════════════════════════════

cells.append(md("""\
    ---
    ## Section 5: Capstone — Querying "Attention Is All You Need" [8 pts]

    Now apply your RAG pipeline to a real research paper. You'll embed the paper that
    invented the Transformer architecture — the foundation of every LLM you've used this
    quarter — and query it using the retrieval technique it describes.

    The paper text is loaded in `attention_paper` from the setup cell (~30,000 characters
    of key sections: Abstract, Introduction, Model Architecture, Attention, Results,
    Conclusion). This is an abridged educational summary — read the full paper at
    https://arxiv.org/abs/1706.03762

    ### What to build

    1. Chunk the paper using the chunk size you chose in Section 4
    2. Add the chunks to a **new** ChromaDB collection (or clear and rebuild the existing
       one) — keep the paper separate from the Ridgeline documents
    3. Query with these 4 specific questions:
       - "What problem does multi-head attention solve compared to single attention?"
       - "How does the model handle the order of words without recurrence?"
       - "What were the BLEU scores on the English-to-German translation task?"
       - "Why is self-attention faster than recurrence for sequence modeling?"
    4. For each query, print the top-2 retrieved chunks (first 150 chars each) and write
       a 1–2 sentence answer **based on what the chunks say** (not from memory)

    ### Key concepts

    - You're using retrieval-augmented generation to study the paper that invented the
      attention mechanism *behind* retrieval-augmented generation. Recursive and satisfying.
    - The paper's technical content is dense — your RAG pipeline should surface the
      specific relevant passages rather than requiring you to read all 15 pages
    - Could you answer these by pasting the entire paper into an LLM? Yes — it's short
      enough. But a 500-page engineering manual wouldn't fit. **RAG scales where
      paste-everything doesn't.**

    ### What to submit [8 pts]

    For each of the 4 queries, print:
    ```
    Question: {question}
    Chunk 1: {first 150 chars}...
    Chunk 2: {first 150 chars}...
    Answer: {your 1-2 sentence answer based on the retrieved chunks}
    ```

    Final reflection (print as text in the last cell):
    ```
    One thing RAG got right: {your observation}
    One limitation I noticed: {your observation}
    ```
"""))

cells.append(code("""\
    # Your code here — chunk the Attention paper and add to ChromaDB
    # Use the same chunk size you chose in Section 4
    # Create a new ChromaDB collection for the paper
"""))

cells.append(code("""\
    # Your code here — query the paper with 4 questions
    # For each: print question, top-2 chunks (first 150 chars), your answer
    #
    # Questions:
    # 1. "What problem does multi-head attention solve compared to single attention?"
    # 2. "How does the model handle the order of words without recurrence?"
    # 3. "What were the BLEU scores on the English-to-German translation task?"
    # 4. "Why is self-attention faster than recurrence for sequence modeling?"
"""))

cells.append(code("""\
    # Your reflection on the capstone
    # Print:
    #   "One thing RAG got right: ..."
    #   "One limitation I noticed: ..."
"""))


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: REFLECTIONS
# ═══════════════════════════════════════════════════════════════════════════

cells.append(md("""\
    ---
    ## Section 6: Reflections [8 pts]

    Answer each prompt in 2–3 sentences. Generic responses earn minimal credit — reference
    specific results from your work above.
"""))

cells.append(md("""\
    ### Reflection 1: How does chunk size affect retrieval quality?

    Describe the tradeoff you observed in Section 3. What would you consider when choosing
    a chunk size for a new document set?

    **Your answer (2–3 sentences):**

    *[Replace this with your reflection]*
"""))

cells.append(md("""\
    ### Reflection 2: Where did RAG succeed and where did it fail?

    Across Sections 4 and 5, identify one query where RAG found exactly the right
    information and one where it struggled. Why?

    **Your answer (2–3 sentences):**

    *[Replace this with your reflection]*
"""))

cells.append(md("""\
    ### Reflection 3: How will you apply context management in Part B?

    You'll be building a context package for the MiniClaw project in Part B. Based on
    what you learned about chunking, retrieval, and the information problem, what's your
    strategy?

    **Your answer (2–3 sentences):**

    *[Replace this with your reflection]*
"""))


# ═══════════════════════════════════════════════════════════════════════════
# SUBMISSION BLOCK
# ═══════════════════════════════════════════════════════════════════════════

cells.append(md("""\
    ---
    ## Submission Checklist

    Before submitting, verify:

    - [ ] All cells run without errors (Kernel → Restart & Run All)
    - [ ] Section 1: Token counts and context budget printed
    - [ ] Section 2: Ranked document lists for both queries with scores
    - [ ] Section 3: Comparison table across 3 chunk sizes, top chunks printed
    - [ ] Section 4: ChromaDB collection created, 5 queries with generated answers and accuracy
    - [ ] Section 5: 4 paper queries answered with retrieved evidence + reflection
    - [ ] Section 6: Three reflections filled in (2–3 sentences each, specific to your results)

    **Due: Monday, April 27, 2026 at 11:59 PM**

    **Save and push your work:**
    In Codespaces, use the Source Control panel (Ctrl+Shift+G) to commit and push.
    Then paste your GitHub repo URL in Canvas.

    ---

    ### References

    - Vaswani, A. et al. "Attention Is All You Need." NeurIPS, 2017. https://arxiv.org/abs/1706.03762
    - ChromaDB documentation: https://docs.trychroma.com/docs/overview/introduction
    - GitHub Models: https://docs.github.com/en/github-models
    - Sentence-Transformers: https://www.sbert.net/
    - tiktoken: https://github.com/openai/tiktoken
"""))


# ═══════════════════════════════════════════════════════════════════════════
# ASSEMBLE AND WRITE NOTEBOOK
# ═══════════════════════════════════════════════════════════════════════════

nb = new_notebook()
nb.metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "name": "python",
        "version": "3.11.0"
    }
}
nb.cells = cells

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "MP2_PartA_The_Information_Problem.ipynb")
with open(out_path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print(f"Notebook written to: {out_path}")
print(f"Total cells: {len(cells)}")
print(f"  Markdown: {sum(1 for c in cells if c.cell_type == 'markdown')}")
print(f"  Code: {sum(1 for c in cells if c.cell_type == 'code')}")
