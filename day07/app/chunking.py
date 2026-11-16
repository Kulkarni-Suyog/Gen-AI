"""Chunk GSTSaral documents/records, keeping source, page and title."""

from __future__ import annotations

from app.records import load_records


def chunk_text(text: str, size: int = 500, overlap: int = 50) -> list[str]:
    """Split long text (e.g. a PDF page) into overlapping character chunks."""
    if size <= overlap:
        raise ValueError("size must be larger than overlap")
    text = " ".join(text.split())
    if not text:
        return []
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start : start + size])
        if start + size >= len(text):
            break
        start += size - overlap
    return chunks


def chunk_records(records: list[dict] | None = None, group_size: int = 1) -> list[dict]:
    """One chunk per record (group_size=1) or per group of N same-category records."""
    records = load_records() if records is None else records
    chunks = []
    if group_size <= 1:
        for r in records:
            chunks.append(_make(f"c{r['id']}", _record_text(r), [r]))
        return chunks
    by_cat: dict[str, list[dict]] = {}
    for r in records:
        by_cat.setdefault(r.get("category", "General"), []).append(r)
    n = 0
    for cat, rs in by_cat.items():
        for i in range(0, len(rs), group_size):
            grp = rs[i : i + group_size]
            n += 1
            chunks.append(_make(f"g{n}", " ".join(_record_text(r) for r in grp), grp))
    return chunks


def _record_text(r: dict) -> str:
    return f"{r['item_or_topic']}. Old rule: {r['old_rule']}. New rule: {r['new_rule']}. Effective from {r['effective_from']}."


def _make(cid: str, text: str, recs: list[dict]) -> dict:
    first = recs[0]
    return {
        "id": cid,
        "text": text,
        "metadata": {
            "title": first["item_or_topic"],
            "source": first["document"],
            "source_url": first["source_url"],
            "page": first.get("page") or 0,
            "effective_from": first["effective_from"],
            "topic": first.get("topic", ""),
            "record_ids": ",".join(str(r["id"]) for r in recs),
            "verified": bool(first.get("verified", True)),
        },
    }


def chunk_document_pages(pages: list[str], title: str, source_url: str, size: int = 500, overlap: int = 50) -> list[dict]:
    """Chunk a multi-page document; each chunk remembers its page number."""
    chunks = []
    for page_no, page in enumerate(pages, start=1):
        for j, piece in enumerate(chunk_text(page, size, overlap)):
            chunks.append(
                {
                    "id": f"p{page_no}-{j}",
                    "text": piece,
                    "metadata": {
                        "title": title,
                        "source": title,
                        "source_url": source_url,
                        "page": page_no,
                        "effective_from": "",
                        "topic": "",
                        "record_ids": "",
                        "verified": True,
                    },
                }
            )
    return chunks
