# GSTSaral - Day 3

## Goal
Download GST Council source material, prepare structured rate-change rows,
clean them with validation, and save the output as JSON.

## Files
- `app/fetch.py`: downloads three FAQ pages and the 56th GST Council PDF.
- `app/models.py`: defines the `Record` dataclass.
- `app/ingest.py`: validates and cleans raw rows, skips bad rows, and writes `data/records.json`.
- `data/raw/rate_changes_source.json`: 20 structured source-derived rows used by the ingestion exercise.
- `data/raw/`: downloaded HTML, PDF and extracted text are saved here when fetch runs.

## Sources
- FAQ: https://gstcouncil.gov.in/en/faq?page=0 (also downloads pages 1 and 2)
- Press release: https://gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau.pdf
- 56th GST Council press release dated 3 September 2025. The listed rate changes are shown
  with the announced effective date of 22 September 2025.

## Setup (Windows PowerShell)
Run these commands from the `day3` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run
Download source documents:

```powershell
python -m app.fetch
```

Clean the structured raw rows and create `data/records.json`:

```powershell
python -m app.ingest
```

## Important data note
The 20 source-derived rows are a curated learning dataset, not a claim that the
HTML/PDF parser automatically identifies every rate change. The downloaded official
documents are retained in `data/raw/` for source inspection. GST rates can depend on
HSN classification, packaging, conditions and later notifications. Verify the applicable
official notification before using any rate for a real invoice or tax filing.
