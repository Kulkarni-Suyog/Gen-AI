"""Load, search and summarise GSTSaral records."""

from collections import Counter

from data.sample_records import RECORDS


def load_records():
    """Return a copy of all records (list of dicts)."""
    return [dict(r) for r in RECORDS]


def search(keyword, records=None):
    """Case-insensitive keyword search over item, category, old and new rule."""
    records = load_records() if records is None else records
    kw = keyword.strip().lower()
    if not kw:
        return []
    hits = []
    for r in records:
        haystack = " ".join(
            str(r[k]) for k in ("item_or_topic", "category", "old_rule", "new_rule")
        ).lower()
        if kw in haystack:
            hits.append(r)
    return hits


def count_by(field="category", records=None):
    """Return {value: count} for the given field."""
    records = load_records() if records is None else records
    return dict(Counter(r[field] for r in records))


def get_by_id(record_id, records=None):
    """Return the record with this id, or None."""
    records = load_records() if records is None else records
    for r in records:
        if r["id"] == record_id:
            return r
    return None
