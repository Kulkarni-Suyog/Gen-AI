"""Persistent Chroma vector database for GSTSaral chunks."""
import json
from pathlib import Path
from typing import Any, Dict, List

import chromadb
from app.chunking import chunk_records
from app.embed import embed_texts

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "records.json"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "gstsaral_semantic_chunks"


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})


def rebuild_index() -> int:
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    chunks = chunk_records(records)
    collection = get_collection()
    # Rebuild cleanly so old chunks cannot remain in the collection.
    collection.delete(where={"record_id": {"$ne": ""}})
    if chunks:
        embeddings = embed_texts([chunk["text"] for chunk in chunks])
        collection.add(
            ids=[chunk["id"] for chunk in chunks],
            documents=[chunk["text"] for chunk in chunks],
            embeddings=embeddings,
            metadatas=[chunk["metadata"] for chunk in chunks],
        )
    return len(chunks)


def search_semantic(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    query_embedding = embed_texts([query])[0]
    collection = get_collection()
    if collection.count() == 0:
        rebuild_index()
        collection = get_collection()
    result = collection.query(query_embeddings=[query_embedding], n_results=min(top_k, collection.count()))
    hits = []
    for i, document in enumerate(result.get("documents", [[]])[0]):
        hits.append({
            "text": document,
            "metadata": result.get("metadatas", [[]])[0][i],
            "distance": result.get("distances", [[]])[0][i],
            "id": result.get("ids", [[]])[0][i],
        })
    return hits
