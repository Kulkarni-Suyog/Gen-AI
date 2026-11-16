"""Clean raw GST documents + curated seeds into data/records.json.

    python -m app.ingest

Steps:
1. Seed records (data/seed_records.json): curated rows from the 56th Council press release
   and old/new FAQ rule pairs.
2. If data/raw/press_release_56th.pdf exists, parse its annexure tables
   ("(12% to 5%)" headers followed by numbered rows) into extra records.
3. Bad rows are skipped with try/except and counted.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from app.models import Record

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
SEED = ROOT / "data" / "seed_records.json"
OUT = ROOT / "data" / "records.json"

PRESS_DOC = "56th GST Council press release (PIB, 3 Sep 2025)"
PRESS_URL = "https://gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau.pdf"

HEADER_RE = re.compile(r"\(?\s*(\d+%|Nil|NIL)\s+to\s+(\d+%|Nil|NIL)\s*\)?\s*$", re.I)
ROW_RE = re.compile(r"^\s*(\d{1,3})\.\s+(?:[\d ]{2,}\s+)?([A-Za-z].{3,})$")


def pdf_to_text(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def parse_annexure(text: str, start_id: int = 1000) -> tuple[list[dict], int]:
    """Parse '(old to new)' sections. Returns (records, skipped_count)."""
    records, skipped, nid = [], 0, start_id
    old = new = None
    for line in text.splitlines():
        line = line.strip()
        m = HEADER_RE.search(line)
        if m and len(line) < 30:
            old, new = m.group(1).upper().replace("NIL", "Nil"), m.group(2).upper().replace("NIL", "Nil")
            continue
        if old is None:
            continue
        try:
            rm = ROW_RE.match(line)
            if not rm:
                continue
            item = re.sub(r"\s+", " ", rm.group(2)).strip()
            rec = Record.from_dict(
                {
                    "id": nid,
                    "item_or_topic": item[:120],
                    "old_rule": f"GST {old}",
                    "new_rule": f"GST {new}",
                    "effective_from": "2025-09-22",
                    "document": PRESS_DOC,
                    "source_url": PRESS_URL,
                    "category": "Annexure (parsed)",
                    "verified": False,
                }
            )
            records.append(rec.to_dict())
            nid += 1
        except (ValueError, TypeError):
            skipped += 1
    return records, skipped


def build(include_parsed: bool = True) -> list[dict]:
    good, bad = [], 0
    for row in json.loads(SEED.read_text(encoding="utf-8")):
        try:
            good.append(Record.from_dict(row).to_dict())
        except (ValueError, TypeError, KeyError) as e:
            bad += 1
            print(f"[skip seed row] {e}: {row}")
    pdf = RAW / "press_release_56th.pdf"
    if include_parsed and pdf.exists():
        parsed, skipped = parse_annexure(pdf_to_text(pdf))
        seen = {r["item_or_topic"].lower() for r in good}
        good += [r for r in parsed if r["item_or_topic"].lower() not in seen]
        bad += skipped
        print(f"parsed {len(parsed)} annexure rows ({skipped} skipped)")
    print(f"records: {len(good)} good, {bad} bad")
    return good


def main() -> None:
    records = build()
    OUT.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"saved {len(records)} records to {OUT}")


if __name__ == "__main__":
    main()
