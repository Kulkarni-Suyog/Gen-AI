"""'Latest rule wins': find newer rules on the same topic and build the old-vs-current warning."""

from __future__ import annotations

from app.records import load_records


def newer_rule(record: dict, records: list[dict] | None = None) -> dict | None:
    """Return the latest record on the same topic if it is newer than `record`, else None."""
    records = load_records() if records is None else records
    same = [r for r in records if r.get("topic") == record.get("topic") and r["id"] != record["id"]]
    newer = [r for r in same if r["effective_from"] > record["effective_from"]]
    if not newer:
        return None
    return max(newer, key=lambda r: r["effective_from"])


def conflict_warning(record: dict, records: list[dict] | None = None) -> dict | None:
    """Warning dict (with both citations) when `record` is superseded, else None."""
    latest = newer_rule(record, records)
    if latest is None:
        return None
    year_old = record["effective_from"][:4]
    year_prev = str(int(year_old) - 1)
    span = f"{year_prev}/{year_old[2:]}" if record["doc_year"] <= 2018 else year_old
    return {
        "message": f"This FAQ is from {span} — newer rule: {latest['new_rule']} (effective {latest['effective_from']})",
        "old": _cite(record),
        "new": _cite(latest),
    }


def _cite(r: dict) -> dict:
    return {
        "id": r["id"],
        "title": r["item_or_topic"],
        "document": r["document"],
        "source_url": r["source_url"],
        "effective_from": r["effective_from"],
        "rule": r["new_rule"],
    }


def rank_latest_first(hits: list[dict]) -> list[dict]:
    """Within the same topic keep only the newest hit first; never average old and new."""
    return sorted(hits, key=lambda h: (h.get("effective_from", ""), h.get("score", 0)), reverse=True)
