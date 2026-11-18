"""Clean raw GST rate-change rows and write data/records.json."""

import json
import re
from pathlib import Path

from app.models import Record

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw" / "rate_changes_source.json"
OUTPUT_FILE = BASE_DIR / "data" / "records.json"
REQUIRED_FIELDS = (
    "item_or_topic", "old_rule", "new_rule",
    "effective_from", "document", "source_url"
)


def clean_text(value: str) -> str:
    """Normalize whitespace and remove common scraping leftovers."""
    value = re.sub(r"\s+", " ", str(value)).strip()
    value = re.sub(r"\s+([,.;:])", r"\1", value)
    value = value.replace(" OR ", " or ")
    return value


def clean_item_name(value: str) -> str:
    """Turn noisy scraped fragments into readable item names."""
    value = clean_text(value)
    value = re.sub(r"^reduction of gst from\s+", "", value, flags=re.I)
    value = re.sub(r"^gst rate on\s+", "", value, flags=re.I)
    value = re.sub(r"\s+(?:from|at)\s+\d+(?:\.\d+)?%.*$", "", value, flags=re.I)
    return value.strip(" -:;,.|")


def ingest() -> list[dict]:
    """Load raw rows, validate each row, and save clean records."""
    try:
        raw_rows = json.loads(RAW_FILE.read_text(encoding="utf-8"))
        if not isinstance(raw_rows, list):
            raise ValueError("The raw source JSON must contain a list of records.")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Could not read raw records: {exc}")
        return []

    cleaned_records = []
    for row_number, row in enumerate(raw_rows, start=1):
        try:
            if not isinstance(row, dict):
                raise TypeError("record must be a dictionary")

            values = {field: clean_text(row[field]) for field in REQUIRED_FIELDS}
            values["item_or_topic"] = clean_item_name(values["item_or_topic"])

            if any(not values[field] for field in REQUIRED_FIELDS):
                raise ValueError("one or more required fields are empty")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", values["effective_from"]):
                raise ValueError("effective_from must use YYYY-MM-DD format")
            if not values["source_url"].startswith(("https://", "http://")):
                raise ValueError("source_url must be a valid HTTP(S) URL")

            record = Record(**values)
            cleaned_records.append(record.to_dict())
        except (KeyError, TypeError, ValueError) as exc:
            print(f"Skipping bad row {row_number}: {exc}")
        except Exception as exc:
            print(f"Unexpected error in row {row_number}: {exc}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(cleaned_records, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"Ingestion complete: saved {len(cleaned_records)} clean records to {OUTPUT_FILE}")
    return cleaned_records


if __name__ == "__main__":
    ingest()
