"""GSTSaral Day 8 RAG API."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from app.vectorstore import get_collection, rebuild_index, search_chunks
from app.rag import answer_question

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create config A index on first startup; config B is created when requested.
    collection = get_collection()
    if collection.count() == 0:
        rebuild_index("A")
    yield

app = FastAPI(title="GSTSaral Day 8 RAG", version="1.0.0", lifespan=lifespan)

class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    top_k: int = Field(3, ge=1, le=10)
    config: str = Field("A", pattern="^[AB]$")

class AskResponse(BaseModel):
    question: str
    answer: str
    citations: list
    retrieved: list
    config: str

@app.get("/health")
def health():
    return {"status": "ok", "day": 8}

@app.get("/search")
def search(q: str = Query(..., min_length=2), top_k: int = Query(3, ge=1, le=10), config: str = Query("A", pattern="^[AB]$")):
    try:
        return {"query": q, "config": config, "results": search_chunks(q, top_k=top_k, config=config)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Search failed: {exc}") from exc

@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    try:
        result = answer_question(payload.question, top_k=payload.top_k, config=payload.config)
        return {"question": payload.question, **result, "config": payload.config}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG request failed: {exc}") from exc

@app.post("/index/rebuild")
def rebuild(config: str = Query("A", pattern="^[AB]$")):
    try:
        count = rebuild_index(config)
        return {"status": "rebuilt", "config": config, "chunks_indexed": count}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Index rebuild failed: {exc}") from exc
