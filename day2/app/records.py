"""Reusable functions for loading and querying GSTSaral records."""

from data.sample_records import SAMPLE_RECORDS


def load_records():
    """Return a copy of all sample GST records."""
    return [record.copy() for record in SAMPLE_RECORDS]


def search(records, keyword):
    """Return records where keyword appears in any text field."""
    keyword = keyword.strip().casefold()
    if not keyword:
        return []

    results = []
    for record in records:
        searchable_text = " ".join(str(value) for value in record.values())
        if keyword in searchable_text.casefold():
            results.append(record)
    return results


def count_by(records, field="category"):
    """Count records grouped by a dictionary field, such as category."""
    counts = {}
    for record in records:
        key = record.get(field, "Uncategorized")
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def get_by_id(records, record_id):
    """Return one record matching its ID, or None when not found."""
    for record in records:
        if record.get("id", "").casefold() == record_id.strip().casefold():
            return record
    return None
