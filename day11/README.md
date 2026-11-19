# GSTSaral — Day 11

This package contains **only the files added for Day 11**. It does not contain the full GSTSaral application.

## 1. Copy the files into your existing project

1. Extract this ZIP.
2. Open your existing GSTSaral project folder — the folder that already contains `day9/` and `ui/`.
3. Copy the `day11` folder into that project folder.
4. Copy `Dockerfile`, `.dockerignore`, `docker-compose.yml`, and `pyproject.toml` into the same project root.
5. Make the small `ui/app.py` change described in Section 4.

Your project should look like this:

```text
Gen-AI/
├── day9/                  # Existing application — keep it
├── ui/                    # Existing UI — keep it
├── day11/
│   ├── README.md
│   ├── requirements-dev.txt
│   └── tests/
│       ├── conftest.py
│       ├── test_records.py
│       ├── test_search.py
│       ├── test_api.py
│       └── test_agent_tool.py
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
└── pyproject.toml
```

**Important:** Day 11 tests use your existing Day 9 application code. Do not remove `day9/` or `ui/`.

## 2. Run tests (Windows PowerShell)

Open PowerShell in the **project root** (the folder containing `day9` and `day11`) and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r day11/requirements-dev.txt
python -m pytest day11/tests -v
```

Expected result: **16 tests pass**.

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Run Ruff

From the project root:

```powershell
ruff check .
```

Ruff configuration is provided in the root `pyproject.toml`.

## 4. Small UI change needed for Docker

In `ui/app.py`:

- Add `import os` with the other imports.
- Set the API URL variable to:

```python
API_URL = os.getenv("GSTSARAL_API_URL", "http://127.0.0.1:8000")
```

If your existing variable has another name, keep that name and apply the same `os.getenv(...)` value. Docker Compose sets `GSTSARAL_API_URL=http://api:8000` inside the UI container.

## 5. Run API and UI using Docker

Install and start Docker Desktop. Open PowerShell in the project root.

Optional — set your Groq key for live LLM answers:

```powershell
$env:GROQ_API_KEY = "your_groq_api_key"
```

Build and start the services:

```powershell
docker compose up --build
```

Open:

- UI: http://localhost:8501
- API documentation: http://localhost:8000/docs
- API health: http://localhost:8000/health

Stop with `Ctrl+C`. To remove the Compose containers, run:

```powershell
docker compose down
```

The first start may take longer because the application may download its embedding model and build the vector index. Internet access may be required.

## 6. What Day 11 includes

- Pytest tests for records/chunking, vector search, `/health`, `/ask` using a fake LLM, and the agent calculator tool.
- Development requirements for pytest and Ruff.
- Dockerfile, Docker Compose, `.dockerignore`, and Ruff configuration.

## 7. Common issues

- Run commands from the project root, not from inside `day11`.
- If `pytest` or `ruff` is not found, activate `.venv` and install `day11/requirements-dev.txt` again.
- If Docker is unavailable, start Docker Desktop and retry.
- If the UI cannot connect to the API in Docker, check the `GSTSARAL_API_URL` change in `ui/app.py`.
