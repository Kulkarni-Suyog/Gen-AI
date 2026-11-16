# Day 5: LLM notes + 10 questions + checkpoint 1

This folder is a runnable snapshot of GSTSaral as of Day 5.

## Files added or updated today
- `docs/how_llms_work.md`
- `docs/questions.md`
- `app/main.py (updated)`

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
```

Git tag for this milestone: `checkpoint-1`
