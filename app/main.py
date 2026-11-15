
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.vectorstore import semantic_search


# Create FastAPI application
app = FastAPI(
    title="GSTSaral API",
    description="AI-powered GST Semantic Search",
    version="1.0.0"
)


# Request model
class SearchRequest(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=2000
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10
    )


# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to GSTSaral API",
        "status": "running"
    }


# Health check API
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Semantic Search API
@app.post("/search/semantic")
def search_semantic(request: SearchRequest):

    try:
        results = semantic_search(
            query=request.query,
            top_k=request.top_k
        )

        return {
            "query": request.query,
            "total_results": len(results),
            "results": results
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Semantic search failed: {str(error)}"
        )
