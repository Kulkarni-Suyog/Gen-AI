"""Load, search and summarise GSTSaral records (data/records.json)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "records.json"


def load_records(path: Path | str | None = None) -> list[dict]:
    p = Path(path) if path else DATA_FILE
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def search(keyword: str, records: list[dict] | None = None) -> list[dict]:
    records = load_records() if records is None else records
    kw = keyword.strip().lower()
    if not kw:
        return []
    hits = []
    for r in records:
        hay = " ".join(str(r.get(k, "")) for k in ("item_or_topic", "category", "old_rule", "new_rule")).lower()
        if kw in hay:
            hits.append(r)
    return hits


def count_by(field: str = "category", records: list[dict] | None = None) -> dict:
    records = load_records() if records is None else records
    return dict(Counter(r.get(field, "?") for r in records))


def get_by_id(record_id: int, records: list[dict] | None = None) -> dict | None:
    records = load_records() if records is None else records
    for r in records:
        if r["id"] == record_id:
            return r
    return None
