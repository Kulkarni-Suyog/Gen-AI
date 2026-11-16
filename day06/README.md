# GSTSaral – Day 6: LLM API + prompt engineering

- `app/llm.py` – provider wrapper (Groq / Gemini, offline fake fallback)
- `app/main.py` – `POST /chat` with the GSTSaral system prompt, returns JSON `{answer, confidence, follow_up}`
- `prompts/system.md`, `prompts/task_answer_v1.md`, `prompts/task_answer_v2.md` (+ `task_plan.md`)
- `eval/prompt_compare.md` – 2 prompt versions compared on the 10 questions
- `.env.example` committed; `.env` NOT committed

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Commit message: `day-06: LLM wrapper, /chat, prompts, prompt_compare`
