# GSTSaral Checkpoint 2

GSTSaral is a GST question-answering chatbot
using Retrieval-Augmented Generation (RAG)
and an Agent workflow.

## Features

- Streamlit chat interface
- RAG API integration
- Agent API integration
- Source citations
- Old vs Current Rule warning
- Thumbs-up feedback
- Thumbs-down feedback
- Feedback storage
- Signature footer

## Folder Structure

ui/
    app.py
    feedback.py
    README.md
    feedback.jsonl

## Requirements

Python 3.10+

Install dependencies:

    pip install streamlit requests

## Run Backend

Open terminal 1.

Navigate to Day 9:

    cd 9

Activate virtual environment:

    ..\.venv\Scripts\Activate.ps1

Start API:

    uvicorn app.main:app --reload

Backend:

    http://127.0.0.1:8000

## Run UI

Open terminal 2 in project root.

Activate environment:

    .\.venv\Scripts\Activate.ps1

Run Streamlit:

    streamlit run ui/app.py

UI:

    http://localhost:8501

## Feedback

Feedback is saved in:

    ui/feedback.jsonl

## Screenshot

After running the application:

1. Open the chatbot.
2. Ask a GST question.
3. Wait for the response.
4. Display citations.
5. Capture screenshot using Win + Shift + S.
6. Save screenshot in docs.

Screenshot path:

    docs/checkpoint2-ui.png

## Git Checkpoint

    git add .
    git commit -m "checkpoint-2: Streamlit UI and feedback"
    git tag checkpoint-2

Verify tag:

    git tag