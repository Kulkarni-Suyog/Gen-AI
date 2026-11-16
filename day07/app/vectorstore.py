"""Persistent Chroma collection of GSTSaral chunks + semantic search."""

from __future__ import annotations

import os
from pathlib import Path

import chromadb

from app.chunking import chunk_records
from app.embed import embed_query, embed_texts

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = os.getenv("CHROMA_PATH", str(ROOT / "chroma_db"))
COLLECTION = "gstsaral"

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=DB_PATH)
    return _client


def build_index(chunks: list[dict] | None = None, name: str = COLLECTION) -> int:
    """(Re)build the collection. Returns number of chunks indexed."""
    chunks = chunk_records() if chunks is None else chunks
    client = _get_client()
    try:
        client.delete_collection(name)
    except Exception:  # noqa: BLE001 - collection may not exist yet
        pass
    col = client.create_collection(name, metadata={"hnsw:space": "cosine"})
    col.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=embed_texts([c["text"] for c in chunks]),
        metadatas=[c["metadata"] for c in chunks],
    )
    return len(chunks)


def semantic_search(query: str, k: int = 4, name: str = COLLECTION) -> list[dict]:
    client = _get_client()
    try:
        col = client.get_collection(name)
    except Exception:  # noqa: BLE001
        build_index(name=name)
        col = client.get_collection(name)
    res = col.query(query_embeddings=[embed_query(query)], n_results=k)
    out = []
    for cid, doc, meta, dist in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]):
        out.append({"id": cid, "text": doc, "metadata": meta, "score": round(1.0 - float(dist), 4)})
    return out
