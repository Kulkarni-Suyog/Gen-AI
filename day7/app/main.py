"""GSTSaral Day 7 semantic search API."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from app.vectorstore import get_collection, rebuild_index, search_semantic


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Build the persistent index the first time the service is started.
    if get_collection().count() == 0:
        rebuild_index()
    yield


app = FastAPI(title="GSTSaral Day 7 Semantic Search", version="1.0.0", lifespan=lifespan)


class SearchResponse(BaseModel):
    query: str
    results: list


@app.get("/health")
def health():
    return {"status": "ok", "collection_count": get_collection().count()}


@app.get("/search/semantic", response_model=SearchResponse)
def semantic_search(q: str = Query(..., min_length=2), top_k: int = Query(3, ge=1, le=10)):
    try:
        hits = search_semantic(q, top_k)
        return {"query": q, "results": hits}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Semantic search failed: {exc}") from exc


@app.post("/index/rebuild")
def rebuild():
    try:
        count = rebuild_index()
        return {"status": "rebuilt", "chunks_indexed": count}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Index rebuild failed: {exc}") from exc
