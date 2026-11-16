# Day 6: LLM wrapper, prompts, /chat

This folder is a runnable snapshot of GSTSaral as of Day 6.

## Files added or updated today
- `app/llm.py`
- `prompts/system.md`
- `prompts/task_answer_v1.md`
- `prompts/task_answer_v2.md`
- `prompts/task_plan.md`
- `.env.example`
- `eval/prompt_compare.md`
- `app/main.py (updated)`

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
```
