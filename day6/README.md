# GSTSaral — Day 6 (LLM Chat)

This folder adds an LLM-powered chat API using GSTSaral's selected GST records.

## Files
- `app/main.py`: FastAPI `/chat` endpoint, record context retrieval, and JSON response.
- `app/llm.py`: provider wrapper for Groq and Gemini.
- `prompts/system.txt`: safety and response-format instructions.
- `prompts/v1.txt`, `prompts/v2.txt`: two prompt approaches for comparison.
- `eval/questions.json`: the same 10 GSTSaral questions from the project documentation.
- `eval/run_eval.py`: sends each question to both prompts using a real configured model.
- `eval/prompt_compare.md`: comparison protocol and scoring sheet.

## Setup (Windows PowerShell)
```powershell
cd 6
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and add your Groq key. Keep `.env` private and untracked.

## Start the API
```powershell
uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs`.

## Test `/chat`
Use the Swagger UI POST `/chat` body:
```json
{
  "question": "What is the revised GST rate for shampoo?",
  "prompt_version": "v1"
}
```
Response contains `answer`, `confidence`, `follow_up`, `prompt_version`, and `matched_records`.

## Run prompt comparison
From the `6` folder:
```powershell
python -m eval.run_eval
```
Actual responses are saved to `eval/raw_results.json`. Review and score them in
`eval/prompt_compare.md`. The evaluation makes real API calls and requires an API key.
