"""GSTSaral Day 9: RAG, tool-using agent, and LangGraph API."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.vectorstore import get_collection, rebuild_index
from app.rag import answer_question
from app.agent_loop import run_agent
from app.graph import run_graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    collection = get_collection()
    if collection.count() == 0:
        rebuild_index("A")
    yield

app = FastAPI(title="GSTSaral Day 9 Agent", version="1.0.0", lifespan=lifespan)

class AgentRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=1000)
    price: Optional[float] = Field(None, ge=0)
    gst_rate: Optional[float] = Field(None, ge=0, le=100)
    intra_state: Optional[bool] = None
    inclusive: Optional[bool] = False
    use_graph: bool = True
    approved: bool = False
    thread_id: str = "default"
    top_k: int = Field(3, ge=1, le=10)
    config: str = Field("A", pattern="^[AB]$")

@app.get("/health")
def health():
    return {"status": "ok", "day": 9}

@app.post("/ask")
def ask(payload: dict):

    try:
        print("\n========== ASK API STARTED ==========")

        question = payload.get("question", "")
        top_k = payload.get("top_k", 3)

        # Get config as a string
        config = payload.get("config", "A")

        # Handle dictionary config safely
        if isinstance(config, dict):
            config = (
                config.get("name")
                or config.get("variant")
                or config.get("id")
                or "A"
            )

        if config is None:
            config = "A"

        config = str(config)

        if not question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )

        print("Question:", question)
        print("Top K:", top_k)
        print("Config:", config)

        result = answer_question(
            question=question,
            top_k=top_k,
            config=config
        )

        print("RAG RESULT:", result)

        print("========== ASK API COMPLETED ==========\n")

        return result

    except HTTPException:
        raise

    except Exception as e:

        import traceback

        print("\n========== ASK API ERROR ==========")
        traceback.print_exc()
        print("===================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post("/agent")
def agent(payload: AgentRequest):
    calculator_args = None
    if payload.price is not None or payload.gst_rate is not None or payload.intra_state is not None:
        if payload.price is None or payload.gst_rate is None or payload.intra_state is None:
            raise HTTPException(status_code=422, detail="For GST calculation, provide price, gst_rate, and intra_state together.")
        calculator_args = {"price": payload.price, "gst_rate": payload.gst_rate, "intra_state": payload.intra_state, "inclusive": payload.inclusive or False}
    try:
        if payload.use_graph:
            return run_graph({"question": payload.question, "calculator_args": calculator_args, "top_k": payload.top_k, "config": payload.config, "approved": payload.approved}, payload.thread_id)
        return run_agent(payload.question, calculator_args=calculator_args, top_k=payload.top_k, config=payload.config)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agent failed: {exc}") from exc

@app.post("/index/rebuild")
def rebuild(config: str = "A"):
    try:
        return {"status": "rebuilt", "config": config, "chunks_indexed": rebuild_index(config)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Index rebuild failed: {exc}") from exc
