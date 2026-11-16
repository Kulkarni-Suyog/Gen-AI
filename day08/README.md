# Day 8: RAG + eval

This folder is a runnable snapshot of GSTSaral as of Day 8.

## Files added or updated today
- `app/conflicts.py`
- `app/rag.py`
- `eval/__init__.py`
- `eval/eval_set.json`
- `eval/run_eval.py`
- `eval/results.md`
- `app/main.py (updated)`

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
```
