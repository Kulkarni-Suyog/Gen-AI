
import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

EMBEDDINGS_FILE = (
    BASE_DIR / "data" / "processed" / "gst_embeddings.json"
)

CHROMA_DIR = (
    BASE_DIR / "data" / "processed" / "chroma_db"
)

MODEL_NAME = "all-MiniLM-L6-v2"

# Initialize ChromaDB
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

model = None


# Load embedding model
def get_model():
    global model

    if model is None:
        model = SentenceTransformer(MODEL_NAME)

    return model


# Get ChromaDB collection
def get_collection():
    return client.get_or_create_collection(
        name="gstsaral",
        metadata={"hnsw:space": "cosine"}
    )


# Store embeddings in ChromaDB
def build_vectorstore():

    if not EMBEDDINGS_FILE.exists():
        raise FileNotFoundError(
            "gst_embeddings.json not found. Run embeddings first."
        )

    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    if not records:
        raise ValueError("No embeddings found.")

    collection = get_collection()

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for item in records:

        chunk_id = str(item["chunk_id"])

        ids.append(f"chunk_{chunk_id}")

        documents.append(item["text"])

        embeddings.append(item["embedding"])

        metadata = {
            "title": str(item.get("title") or "Unknown"),
            "source": str(item.get("source") or "Unknown"),
            "filename": str(item.get("filename") or "Unknown")
        }

        if item.get("page") is not None:
            metadata["page"] = str(item["page"])

        metadatas.append(metadata)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Collection:", collection.name)
    print("Total stored chunks:", collection.count())


# Semantic search
def semantic_search(query, top_k=3):

    collection = get_collection()

    if collection.count() == 0:
        raise ValueError(
            "ChromaDB is empty. Build the vectorstore first."
        )

    query_embedding = get_model().encode(
        [query],
        normalize_embeddings=True
    )[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count())
    )

    output = []

    for i in range(len(results["ids"][0])):

        metadata = results["metadatas"][0][i]

        distance = results["distances"][0][i]

        output.append({
            "text": results["documents"][0][i],
            "title": metadata.get("title", "Unknown"),
            "source": metadata.get("source", "Unknown"),
            "page": metadata.get("page"),
            "similarity": round(1 - distance, 4)
        })

    return output
