"""Day 4 - GSTSaral FastAPI service.

Run from inside the day04 folder:
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.records import get_by_id, load_records
from app.smart_search import SmartSearch

QUESTIONS_FILE = Path(__file__).resolve().parent.parent / "data" / "questions.jsonl"

app = FastAPI(title="GSTSaral API", version="0.1.0",
              description="Simple GST helper: old vs new rules for everyday items.")

RECORDS = load_records()
SEARCH = SmartSearch(RECORDS)


class QuestionIn(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    name: str | None = Field(default=None, max_length=80)


@app.get("/health")
def health():
    return {"status": "ok", "records": len(RECORDS)}


@app.get("/records")
def list_records(limit: int = Query(10, ge=1, le=500)):
    return {"total": len(RECORDS), "limit": limit, "records": RECORDS[:limit]}


@app.get("/records/{record_id}")
def one_record(record_id: int):
    record = get_by_id(RECORDS, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    return record


@app.get("/search")
def search(q: str = Query(..., min_length=1), top_k: int = Query(5, ge=1, le=50)):
    hits = SEARCH.search(q, top_k)
    return {"query": q, "count": len(hits),
            "results": [{"score": s, **r} for r, s in hits]}


@app.post("/questions", status_code=201)
def post_question(body: QuestionIn):
    """Save a user question and return the best matching records (no LLM yet)."""
    hits = SEARCH.search(body.question, 3)
    entry = {
        "asked_at": datetime.now(timezone.utc).isoformat(),
        "name": body.name,
        "question": body.question,
        "top_record_ids": [r["id"] for r, _ in hits],
    }
    try:
        with QUESTIONS_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass  # logging must never break the answer
    return {
        "received": body.question,
        "answer": "Chatbot answers come in a later week. Closest records found:"
                  if hits else "No matching record found - I don't know yet.",
        "matches": [{"score": s, **r} for r, s in hits],
    }
