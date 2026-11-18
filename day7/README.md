# GSTSaral Day 7 - Semantic Search with ChromaDB

This folder chunks GSTSaral records, creates semantic embeddings using `sentence-transformers/all-MiniLM-L6-v2`, indexes them in a persistent Chroma collection, and exposes semantic search through FastAPI.

## Setup (Windows PowerShell)

```powershell
cd 7
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Build the index and evaluate the 10 questions

```powershell
python -m eval.run_eval
```

This rebuilds the persistent Chroma collection and writes real hits to `eval/search_results.md`.

## Start API

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

Try:

- `GET /health`
- `GET /search/semantic?q=GST%20rate%20on%20shampoo`
- `POST /index/rebuild`

The first model download can take time. Chroma data is stored in `chroma_db/` and ignored by Git.

## Chunk metadata

Each chunk stores a title, source/document, page (when available), record ID and source URL. The current supplied records do not contain individual page numbers, so page is recorded as `not specified` rather than invented.
