from pathlib import Path
import json
import traceback

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.llm import generate_response


# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

PROMPT_DIR = BASE_DIR / "prompts"


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="GSTSaral Day 06",
    description="LLM Integration and Prompt Comparison",
    version="1.0.0"
)


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class ChatRequest(BaseModel):

    question: str

    prompt_version: str = "v1"


# --------------------------------------------------
# PROMPT LOADER
# --------------------------------------------------

def read_prompt(filename):

    prompt_path = PROMPT_DIR / filename

    if not prompt_path.exists():

        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    with open(prompt_path, "r", encoding="utf-8") as file:

        return file.read()


# --------------------------------------------------
# HOME ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "project": "GSTSaral",
        "day": 6,
        "status": "running",
        "message": "GSTSaral LLM API is working"
    }


# --------------------------------------------------
# HEALTH ENDPOINT
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# CHAT ENDPOINT
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # Validate question
    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )


    # Validate prompt version
    if request.prompt_version not in ["v1", "v2"]:

        raise HTTPException(
            status_code=400,
            detail="prompt_version must be v1 or v2"
        )


    try:

        # Load system prompt
        system_prompt = read_prompt("system.txt")


        # Load selected task prompt
        task_prompt = read_prompt(
            request.prompt_version + ".txt"
        )


        # Prepare user prompt
        user_prompt = task_prompt.replace(
            "{question}",
            request.question
        )


        # Call Groq LLM
        raw_answer = generate_response(
            system_prompt,
            user_prompt
        )


        # Convert response into JSON
        result = json.loads(raw_answer)


        # Extract values
        answer = result.get("answer", "")

        confidence = result.get(
            "confidence",
            0.5
        )

        follow_up = result.get(
            "follow_up",
            None
        )


        # Return response
        return {
            "answer": answer,
            "confidence": confidence,
            "follow_up": follow_up,
            "prompt_version": request.prompt_version,
            "model": "Groq"
        }


    except HTTPException:

        raise


    except Exception as e:

        # Print complete error in terminal
        print("\n")
        print("=" * 50)
        print("GSTSARAL ERROR")
        print("=" * 50)

        traceback.print_exc()

        print("=" * 50)


        # Return error to Swagger
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )