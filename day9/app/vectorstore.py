"""Chroma vector store with two retrieval configurations for Day 8 evaluation."""
import json
from pathlib import Path
from typing import Any, Dict, List
import chromadb
from app.chunking import chunk_records
from app.embed import embed_texts

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "records.json"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "gstsaral_day8_rag"


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(name=f"{COLLECTION_NAME}_a", metadata={"hnsw:space": "cosine"})


def _chunks_for_config(records: List[Dict[str, Any]], config: str) -> List[Dict[str, Any]]:
    # Config A: one complete chunk per record. Config B: split long record text into smaller chunks.
    chunks = chunk_records(records)
    if config == "A":
        return chunks
    if config != "B":
        raise ValueError("config must be 'A' or 'B'")
    result = []
    chunk_size, overlap = 250, 40
    for chunk in chunks:
        text = chunk["text"]
        if len(text) <= chunk_size:
            result.append(chunk)
            continue
        start = 0
        part = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            new_chunk = dict(chunk)
            new_chunk["id"] = f"{chunk['id']}-part{part}"
            new_chunk["text"] = text[start:end]
            new_chunk["metadata"] = dict(chunk["metadata"], chunk_part=str(part))
            result.append(new_chunk)
            if end == len(text):
                break
            start = max(end - overlap, start + 1)
            part += 1
    return result


def rebuild_index(config: str = "A") -> int:
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    chunks = _chunks_for_config(records, config)
    collection = get_collection()
    # Use a config-specific collection, so A and B can be compared without overwriting.
    collection_name = f"{COLLECTION_NAME}_{config.lower()}"
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    existing = collection.get()
    if existing.get("ids"):
        collection.delete(ids=existing["ids"])
    if chunks:
        embeddings = embed_texts([c["text"] for c in chunks])
        collection.add(ids=[c["id"] for c in chunks], documents=[c["text"] for c in chunks], embeddings=embeddings, metadatas=[c["metadata"] for c in chunks])
    return len(chunks)


def search_chunks(query: str, top_k: int = 3, config: str = "A") -> List[Dict[str, Any]]:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection_name = f"{COLLECTION_NAME}_{config.lower()}"
    collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    if collection.count() == 0:
        rebuild_index(config)
        collection = client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    embedding = embed_texts([query])[0]
    result = collection.query(query_embeddings=[embedding], n_results=min(top_k, collection.count()))
    hits = []
    for i, doc in enumerate(result.get("documents", [[]])[0]):
        hits.append({"id": result["ids"][0][i], "text": doc, "metadata": result["metadatas"][0][i], "distance": result.get("distances", [[]])[0][i]})
    return hits
