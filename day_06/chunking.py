
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "extracted" / "extracted_data.json"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "gst_chunks.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def load_documents():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("extracted_data.json not found")

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def split_text(text):
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def create_chunks(documents):
    all_chunks = []

    for document in documents:

        text = document.get("text", "")

        if not text.strip():
            continue

        filename = document.get("filename", "unknown")

        title = document.get("title") or Path(filename).stem

        source = (
            document.get("source")
            or document.get("source_url")
            or filename
        )

        page = document.get("page")

        text_chunks = split_text(text)

        for index, chunk in enumerate(text_chunks, start=1):

            all_chunks.append({
                "chunk_id": len(all_chunks) + 1,
                "title": title,
                "source": source,
                "filename": filename,
                "page": page,
                "chunk_index": index,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":

    print("===== GSTSARAL CHUNKING =====")

    documents = load_documents()

    chunks = create_chunks(documents)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Total documents:", len(documents))
    print("Total chunks:", len(chunks))
    print("Output:", OUTPUT_FILE)
    print("Chunking completed!")
