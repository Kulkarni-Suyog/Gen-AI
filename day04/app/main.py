"""GSTSaral FastAPI service (Day 4 version).  uvicorn app.main:app --reload"""

import json
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.records import get_by_id, load_records
from app.smart_search import smart_search

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_FILE = ROOT / "data" / "questions.jsonl"
app = FastAPI(title="GSTSaral API", version="0.4")


class QuestionIn(BaseModel):
    question: str = Field(..., max_length=500)


@app.get("/health")
def health():
    return {"status": "ok", "records": len(load_records())}


@app.get("/records")
def list_records(limit: int = Query(10, ge=1, le=200)):
    return load_records()[:limit]


@app.get("/records/{record_id}")
def one_record(record_id: int):
    rec = get_by_id(record_id)
    if rec is None:
        raise HTTPException(status_code=404, detail=f"record {record_id} not found")
    return rec


@app.get("/search")
def search_records(q: str = Query(..., min_length=1, max_length=200), k: int = Query(5, ge=1, le=20)):
    return smart_search(q, k)


@app.post("/questions")
def save_question(body: QuestionIn):
    qid = uuid.uuid4().hex[:8]
    QUESTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUESTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"id": qid, "question": body.question, "ts": time.time()}) + "\n")
    return {"id": qid, "saved": True}
