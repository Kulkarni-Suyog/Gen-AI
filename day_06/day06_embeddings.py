import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed" / "gst_chunks.json"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "gst_embeddings.json"

# Load embedding model
MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "gst_chunks.json not found. Complete Day 05 first."
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_embeddings(chunks):
    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    results = []

    for chunk, vector in zip(chunks, vectors):
        results.append({
            "chunk_id": chunk["chunk_id"],
            "filename": chunk.get("filename"),
            "text": chunk["text"],
            "embedding": vector.tolist()
        })

    return results


if __name__ == "__main__":
    print("===== GSTSARAL DAY 06: EMBEDDINGS =====")

    chunks = load_chunks()

    print("Total chunks:", len(chunks))

    if not chunks:
        print("No chunks found. Check Day 05 output.")
    else:
        embeddings = generate_embeddings(chunks)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            json.dump(
                embeddings,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nTotal embeddings generated:", len(embeddings))
        print("Embedding dimensions:", len(embeddings[0]["embedding"]))
        print("Output saved at:", OUTPUT_FILE)
        print("\nDay 06 Embeddings Completed!")
