# GSTSaral - Day 2

## What this day builds

- Stores 23 sample GST rate-change records in `data/sample_records.py`.
- Prints all records, searches by keyword, and counts records by category.
- Refactors reusable operations into `app/records.py`.
- Provides a menu-driven command-line interface in `app/cli.py`.

## Record fields

Each record contains `id`, `category`, `item_or_topic`, `old_rule`, `new_rule`,
`effective_from`, `document`, and `source_url`. The `id` supports `get_by_id`;
`category` supports category counts.

## Data source

56th GST Council Meeting: Recommendations / Press Release (3 September 2025)

Official press release: https://pib.gov.in/PressReleasePage.aspx?PRID=2163793

The entries are educational summaries of selected rate changes. Product classification,
packaging/label conditions, HSN codes, notifications and exceptions can affect the actual
GST treatment. Verify the applicable official notification before using a rate for billing
or tax compliance.

## Run on Windows PowerShell

From this `day2` folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m app.cli
```

No third-party packages are required. `requirements.txt` is included for the project setup.

If PowerShell blocks activation, run the program directly with:

```powershell
.\.venv\Scripts\python.exe -m app.cli
```
