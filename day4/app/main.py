"""GSTSaral REST API built with FastAPI."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.smart_search import smart_search

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "records.json"


def load_records() -> list[dict[str, Any]]:
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


app = FastAPI(
    title="GSTSaral API",
    description="Explore GST rate-change records and ask questions using TF-IDF search.",
    version="1.0.0",
)


class QuestionInput(BaseModel):
    question: str = Field(..., min_length=1, description="Question about a GST rate change")
    limit: int = Field(default=3, ge=1, le=10)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "GSTSaral API"}


@app.get("/records")
def get_records(limit: int = Query(default=100, ge=1, le=500)):
    records = load_records()[:limit]
    return {"count": len(records), "records": [dict(record, record_id=i + 1) for i, record in enumerate(records)]}


@app.get("/records/{record_id}")
def get_record(record_id: int):
    records = load_records()
    if record_id < 1 or record_id > len(records):
        raise HTTPException(status_code=404, detail=f"GST record {record_id} was not found")
    return dict(records[record_id - 1], record_id=record_id)


@app.get("/search")
def search_records(q: str = Query(..., min_length=1), limit: int = Query(default=5, ge=1, le=20)):
    results = smart_search(load_records(), q, limit)
    return {"query": q, "count": len(results), "results": results}


@app.post("/questions")
def ask_question(payload: QuestionInput):
    results = smart_search(load_records(), payload.question, payload.limit)
    if not results:
        return {
            "question": payload.question,
            "answer": "I could not find a closely matching GSTSaral record. Try mentioning the item name or GST rate.",
            "matches": [],
        }

    best = results[0]
    answer = (
        f"For {best['item_or_topic']}, the recorded change is from "
        f"{best['old_rule']} to {best['new_rule']}, effective from {best['effective_from']}."
    )
    return {"question": payload.question, "answer": answer, "matches": results}
