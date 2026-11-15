
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "gst_chunks.json"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "gst_embeddings.json"

MODEL_NAME = "all-MiniLM-L6-v2"

def load_chunks():
    """Load processed GST text chunks."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "gst_chunks.json not found. Run chunking first."
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def generate_embeddings(chunks):
    """Generate embeddings for all text chunks."""

    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    results = []

    for chunk, vector in zip(chunks, vectors):

        results.append({
            "chunk_id": chunk["chunk_id"],
            "title": chunk["title"],
            "source": chunk["source"],
            "page": chunk["page"],
            "filename": chunk["filename"],
            "text": chunk["text"],
            "embedding": vector.tolist()
        })

    return results

if __name__ == "__main__":

    print("===== GSTSARAL DAY 07 EMBEDDINGS =====")

    chunks = load_chunks()

    if not chunks:
        raise ValueError("No chunks available for embedding.")

    embeddings = generate_embeddings(chunks)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            embeddings,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Total embeddings:", len(embeddings))
    print("Embedding dimensions:", len(embeddings[0]["embedding"]))
    print("Output file:", OUTPUT_FILE)
    print("Embedding generation completed!")