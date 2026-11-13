
# GSTSaral - Day 05
# Text Processing and Chunking

import json
from pathlib import Path


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "extracted" / "extracted_data.json"

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "gst_chunks.json"


# Chunk configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


# Function to load extracted data
def load_data():

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Function to split text into chunks
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


# Function to process documents
def process_documents(documents):

    all_chunks = []

    for document in documents:

        text = document.get("text", "")

        if not text.strip():
            continue

        chunks = split_text(text)

        for index, chunk in enumerate(chunks, start=1):

            all_chunks.append({

                "chunk_id": len(all_chunks) + 1,
                "filename": document.get("filename"),
                "file_type": document.get("file_type"),
                "page": document.get("page"),
                "chunk_index": index,
                "text": chunk,
                "character_count": len(chunk)

            })

    return all_chunks


# Main program
if __name__ == "__main__":

    print("===== GSTSARAL TEXT CHUNKING =====")

    documents = load_data()

    print("Total documents:", len(documents))

    chunks = process_documents(documents)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Total chunks generated:", len(chunks))

    print("Chunk size:", CHUNK_SIZE)
    print("Chunk overlap:", CHUNK_OVERLAP)

    print("\nOutput saved at:", OUTPUT_FILE)

    print("\nDay 05 Text Chunking Completed!")
