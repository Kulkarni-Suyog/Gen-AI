# Day 7: Chunking, embeddings, Chroma

This folder is a runnable snapshot of GSTSaral as of Day 7.

## Files added or updated today
- `app/embed.py`
- `app/chunking.py`
- `app/vectorstore.py`
- `eval/search_results.md`
- `app/main.py (updated)`

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
```
