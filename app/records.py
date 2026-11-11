"""Day 4 - load GSTSaral records from data/records.json (made on Day 3)."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "records.json"
FALLBACK = Path(__file__).resolve().parent.parent.parent / "day03" / "data" / "records.json"


def load_records(path=None):
    """Return list[dict]. Falls back to day03's file; returns [] if none found."""
    for candidate in ([Path(path)] if path else [DATA_FILE, FALLBACK]):
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return []


def get_by_id(records, record_id):
    for record in records:
        if record.get("id") == record_id:
            return record
    return None
