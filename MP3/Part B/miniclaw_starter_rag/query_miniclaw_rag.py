"""Query the MiniClaw starter RAG.

This is the function you wrap as an MCP tool in ``mcp_server_starter/server.py``.

Usage:
    from query_miniclaw_rag import query_miniclaw_rag
    out = query_miniclaw_rag("What's the print-shop tolerance on press fits?", n_results=3)
"""

from __future__ import annotations

import pathlib
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

_HERE = pathlib.Path(__file__).resolve().parent
_DB_DIR = _HERE / "chroma_db"

COLLECTION_NAME = "miniclaw_starter"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(EMBED_MODEL_NAME)


@lru_cache(maxsize=1)
def _get_collection():
    if not _DB_DIR.exists():
        raise FileNotFoundError(
            "MiniClaw starter ChromaDB not found. Run "
            "`python MP3/Part\\ B/miniclaw_starter_rag/build_index.py` first."
        )
    client = chromadb.PersistentClient(path=str(_DB_DIR))
    return client.get_collection(COLLECTION_NAME)


def query_miniclaw_rag(question: str, n_results: int = 3) -> dict:
    """Search the MiniClaw / ACME project knowledge base.

    Searches ACME Robotics' internal knowledge base for the MiniClaw project.
    The corpus covers manufacturing capabilities (Prusa MK4S print shop,
    achievable tolerances, FilaTech PolyPro PLA test data), previous product
    history (WidgetBot 2.0 gear test report, GripperBot specs, BigClaw teardown
    notes), engineering design standards (gear design guidelines, design review
    checklist, tolerance procedure for printed assemblies), vendor information
    (FilaTech bulk pricing), and project status (RobotExpo logistics, Q1
    engineering report). Use this whenever the user asks about the MiniClaw
    project, ACME's capabilities, or company-specific data.

    Args:
        question: Natural-language question about the MiniClaw project,
            ACME's standards, BigClaw reference data, vendor info, or print
            shop capabilities.
        n_results: Number of chunks to retrieve (default 3, max 10).

    Returns:
        dict with:
            "chunks":  list of {"text", "doc_id", "title", "score"}
            "summary": brief 1-line summary of what was retrieved
    """
    n_results = max(1, min(int(n_results), 10))
    coll = _get_collection()
    model = _get_model()
    q_emb = model.encode([question], normalize_embeddings=True).tolist()
    res = coll.query(query_embeddings=q_emb, n_results=n_results)

    chunks = []
    for text, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        score = max(0.0, 1.0 - dist / 2.0)
        chunks.append({
            "text": text,
            "doc_id": meta["doc_id"],
            "title": meta["title"],
            "score": round(score, 4),
        })

    summary = (
        f"{len(chunks)} chunks retrieved. Top match: "
        f"{chunks[0]['doc_id']} — {chunks[0]['title']} (score {chunks[0]['score']})."
        if chunks else "No chunks retrieved."
    )
    return {"chunks": chunks, "summary": summary}


if __name__ == "__main__":
    out = query_miniclaw_rag("What PLA printing parameters does ACME use for gears?", 3)
    print(out["summary"])
    for c in out["chunks"]:
        print(f"  [{c['doc_id']}] {c['title']} (score {c['score']})")
        print("   ", c["text"][:160].replace("\n", " "), "...")

