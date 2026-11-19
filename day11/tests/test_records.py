"""Tests for the GST records dataset and chunk preparation."""
import json
from pathlib import Path

from app.chunking import chunk_records

ROOT = Path(__file__).resolve().parents[2]
RECORDS_FILE = ROOT / "day9" / "data" / "records.json"

def test_records_file_exists():
    assert RECORDS_FILE.is_file()

def test_records_file_is_valid_nonempty_json_list():
    records = json.loads(RECORDS_FILE.read_text(encoding="utf-8"))
    assert isinstance(records, list)
    assert len(records) >= 1

def test_records_have_topic_and_source_fields():
    records = json.loads(RECORDS_FILE.read_text(encoding="utf-8"))
    assert all(record.get("item_or_topic") for record in records)
    assert all(record.get("document") for record in records)

def test_chunk_records_preserves_record_count_and_metadata():
    records = json.loads(RECORDS_FILE.read_text(encoding="utf-8"))
    chunks = chunk_records(records)
    assert len(chunks) == len(records)
    assert chunks[0]["metadata"]["record_id"] == "1"
    assert chunks[0]["metadata"]["source_url"].startswith("https://")
