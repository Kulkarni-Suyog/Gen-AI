# GSTSaral | Day 04

Day 04 adds a FastAPI service, TF-IDF smart search, a question endpoint, and a small pandas exploration script.

## Project structure

```text
day4/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── smart_search.py
├── analysis/
│   └── explore.py
├── data/
│   └── records.json
├── .gitignore
├── README.md
└── requirements.txt
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check whether the API is running |
| GET | `/records?limit=10` | Return GST records, with an optional limit |
| GET | `/records/{record_id}` | Return one record; returns HTTP 404 when missing |
| GET | `/search?q=toothpaste` | Rank records using TF-IDF and cosine similarity |
| POST | `/questions` | Answer a question using the best matching GST record |

The API assigns record IDs based on each record's position in `data/records.json` (starting at 1).

## How to run

Open PowerShell in the `day4` folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

Try these URLs in your browser:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/records?limit=5
http://127.0.0.1:8000/records/1
http://127.0.0.1:8000/search?q=toothpaste
```

To test the question endpoint, use `/docs`, open `POST /questions`, click **Try it out**, and submit:

```json
{
  "question": "What happened to the GST rate on toothpaste?",
  "limit": 3
}
```

### Run the pandas analysis

Open a second PowerShell terminal in the `day4` folder. Activate the same environment if needed, then run:

```powershell
python -m analysis.explore
```

The script prints three facts about the local records dataset.

## Dataset note

This folder contains a 13-record learning subset copied from the Day 03 curated GST rate-change dataset. TF-IDF ranks text similarity. It is not a generative AI model and does not verify legal GST classification. Check the applicable official notification and HSN conditions before using any rate for tax compliance.

## Git: commit and tag Week 1

Run these commands from the main repository root (`sanjivani-sj-36-gstsaral`):

```powershell
git add day4
git commit -m "day-04: add FastAPI and TF-IDF smart search"
git tag -a week-1 -m "GSTSaral Week 1 complete"
git push origin main
git push origin week-1
```

If the `week-1` tag already exists, inspect it before creating another tag. To check tags:

```powershell
git tag --list
```
