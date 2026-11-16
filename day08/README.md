# Day 8: RAG + eval

## Files
- `app/rag.py` – answers from retrieved chunks with citations; says "I don't know" when nothing relevant is found (Q6)
- `app/main.py` – adds `POST /ask`
- `eval/eval_set.json` – 15 questions (12 answerable, 3 unanswerable incl. Q6)
- `eval/run_eval.py` – runs the configs below and prints the table
- `app/conflicts.py` – helper imported by `rag.py` ("latest rule wins")

## Run
```bash
uvicorn app.main:app --reload      # POST /ask  {"question": "..."}
python -m eval.run_eval            # writes eval/results.md
```
(Needs the Day 6–7 files: `llm.py`, `records.py`, `chunking.py`, `embed.py`, `vectorstore.py`, `prompts/`, `data/`.)

## Eval: winner table (15 questions)
| Config | Answerable hit rate | Correct "I don't know" | Overall |
|---|---|---|---|
| A: per-record chunks, top-k 3 **(winner)** | 12/12 | 3/3 | 100% |
| B: grouped chunks (4 records), top-k 3 | 11/12 | 3/3 | 93% |
| C: per-record chunks, top-k 5 | 12/12 | 3/3 | 100% |

**Winner: A** – ties with C on score, but uses fewer chunks (top-k 3). Grouped chunks (B) lose precision.

Commit message: `day-08: RAG /ask with citations, eval set, run_eval`
