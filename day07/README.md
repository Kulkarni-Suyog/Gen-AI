# GSTSaral – Day 7: Chunking, embeddings, Chroma

- `app/chunking.py` – chunks keep source, page and title
- `app/embed.py` – embeddings
- `app/vectorstore.py` – persistent Chroma collection (`PersistentClient`)
- `app/main.py` – `GET /search/semantic?q=...&k=4`
- `app/evaluate_search.py` – runs the 10 GST questions, writes `eval/search_results.md`
- `eval/search_results.md` – top hits per question (generated)

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
python -m app.evaluate_search     # regenerate eval/search_results.md
```
Commit message: `day-07: chunking, embeddings, Chroma, GET /search/semantic, search_results`
