# GSTSaral

GSTSaral is a learning project that organizes selected GST rate-change information and provides a small FastAPI service to browse records and search them using TF-IDF with cosine similarity.

## Project folders

- `day1/` - project introduction and menu
- `day2/` - record structure, search and command-line interface
- `day3/` - source fetching and data ingestion
- `day4/` - FastAPI endpoints, TF-IDF search and pandas exploration
- `docs/` - project documentation and example user questions

## How to run

The API is in `day4/`. Open a terminal at the repository root and run:

```powershell
cd day4
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

When the server starts, open these addresses in a browser:

- API interactive documentation (Swagger UI): http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Records: http://127.0.0.1:8000/records
- Search example: http://127.0.0.1:8000/search?q=shampoo

To stop the server, press `Ctrl+C` in the terminal.

### Try the POST `/questions` endpoint

In Swagger UI, expand `POST /questions`, select **Try it out**, and enter:

```json
{
  "question": "What is the new GST rate on shampoo?",
  "limit": 3
}
```

Select **Execute** to see the matching record and generated response.

## Explore the records with pandas

Open a second terminal at the repository root:

```powershell
cd day4
.\.venv\Scripts\Activate.ps1
python -m pip install pandas
python -m analysis.explore
```

## Checkpoint 1 documentation

- [How LLMs work](docs/how_llms_work.md)
- [10 GSTSaral user questions](docs/questions.md)

The LLM document includes a Mermaid flow diagram. The question list maps realistic questions to the record IDs available to the Day 4 API and marks the future-rate question as not answerable by the current dataset.

## Explain one function: `smart_search`

The `smart_search()` function in `day4/app/smart_search.py` finds records related to a user's search phrase:

1. It combines useful fields from each GST record into searchable text.
2. `TfidfVectorizer` converts the record text and query into TF-IDF numerical vectors.
3. `cosine_similarity` compares the query vector with every record vector.
4. It sorts the similarity scores from highest to lowest and returns the best matching records.

For example, searching for `shampoo` should rank the shampoo record near the top. The function retrieves matching stored information; it does not independently verify tax law or predict future GST rates.

## Checkpoint 1: run and show the API

1. Start the FastAPI server using the commands above.
2. Open http://127.0.0.1:8000/docs.
3. Take a screenshot showing the GSTSaral API title and its available endpoints. Save it as `docs/checkpoint1_swagger.png` if your class submission requires screenshot evidence.
4. Explain `smart_search()` using the steps in the section above.

## Git checkpoint commands

Run these commands from the repository root after reviewing your changes:

```powershell
git add README.md docs/
git commit -m "checkpoint-1: add LLM and GSTSaral question documentation"
git tag checkpoint-1
git push origin main
git push origin checkpoint-1
```

If the tag already exists, inspect it with `git tag --list checkpoint-1` before trying to create it again.

## Data accuracy note

This project uses a small curated learning dataset of selected announced rate changes. Product classification, HSN code, packaging and other conditions can affect actual GST treatment. Verify official notifications and applicable rules before relying on a rate for business or tax filing.

## Running the numbered checkpoints (Days 6–9)

Each numbered folder is an independent checkpoint. Open a terminal in the folder you want to run, create its own virtual environment, install that folder's `requirements.txt`, and start the API from that folder. Do not run `uvicorn app.main:app` from the repository root.

### Windows PowerShell example (Day 9)

```powershell
cd 9
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and add GROQ_API_KEY
uvicorn app.main:app --reload
```

### Linux example (Day 9)

```bash
cd 9
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GROQ_API_KEY
uvicorn app.main:app --reload
```

Replace `9` with `6`, `7`, or `8` to run another checkpoint. Days 6, 8 and 9 need an LLM API key for answer-generation endpoints. Days 7–9 download the Sentence Transformers model on first index build, so first startup can take time and requires internet access. See `DUPLICATE_AND_RUN_AUDIT.md` for the checks and limitations from the cleanup.



# Checkpoint 2 - GSTSaral UI

## Streamlit Chat Interface

GSTSaral provides a Streamlit interface for interacting
with the Day 9 RAG and Agent backend.

### Features

- Chat interface
- RAG-based question answering
- Agent workflow
- Source citations
- Old vs Current Rule warning
- User feedback
- Feedback storage
- GSTSaral signature

### Screenshot

![GSTSaral Checkpoint 2 UI](docs/checkpoint2-ui.png)

### Run the Backend

```bash
cd 9
uvicorn app.main:app --reload