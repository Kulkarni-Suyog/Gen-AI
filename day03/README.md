# Day 3: Ingest, models, fetch

This folder is a runnable snapshot of GSTSaral as of Day 3.

## Files added or updated today
- `app/__init__.py`
- `app/models.py`
- `app/records.py`
- `app/fetch.py`
- `app/ingest.py`
- `data/seed_records.json`
- `data/records.json`
- `data/raw/.gitkeep`

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.ingest      # builds data/records.json
python -m app.fetch       # downloads documents into data/raw/ (needs internet)
```
