"""Convert GST records into searchable text chunks with metadata."""
from typing import Any, Dict, List


def chunk_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Create one chunk per GST record, preserving source/title/page metadata."""
    chunks = []
    for index, record in enumerate(records, start=1):
        title = record.get("title") or record.get("item_or_topic") or f"GST record {index}"
        source = record.get("source") or record.get("document") or "GSTSaral dataset"
        page = record.get("page") or record.get("page_number") or "not specified"
        text_parts = [
            f"Title: {title}",
            f"Topic: {record.get('item_or_topic', '')}",
            f"Old rule: {record.get('old_rule', '')}",
            f"New rule: {record.get('new_rule', '')}",
            f"Effective from: {record.get('effective_from', '')}",
            f"Document: {record.get('document', source)}",
        ]
        if record.get("notes"):
            text_parts.append(f"Notes: {record['notes']}")
        if record.get("source_url"):
            text_parts.append(f"Source URL: {record['source_url']}")
        chunks.append({
            "id": str(record.get("id", index)),
            "text": "\n".join(part for part in text_parts if part.strip()),
            "metadata": {
                "title": str(title),
                "source": str(source),
                "page": str(page),
                "record_id": str(record.get("id", index)),
                "source_url": str(record.get("source_url", "")),
            },
        })
    return chunks
