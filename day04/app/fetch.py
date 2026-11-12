"""Download GST documents into data/raw/ with requests (timeouts + error handling).

Run on your own machine (needs internet):  python -m app.fetch
"""

from __future__ import annotations

import sys
from pathlib import Path

import requests

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
TIMEOUT = (5, 30)  # connect, read seconds
HEADERS = {"User-Agent": "GSTSaral/1.0 (learning project)"}

DOCUMENTS = [
    ("faq_index.html", "https://gstcouncil.gov.in/en/faq?page=0"),
    (
        "press_release_56th.pdf",
        "https://gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau.pdf",
    ),
    ("gst_council_home.html", "https://gstcouncil.gov.in/"),
]


def download(url: str, dest: Path, session: requests.Session | None = None) -> bool:
    """Download one URL. Returns True on success, False on any handled error."""
    sess = session or requests
    try:
        resp = sess.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"[timeout] {url}", file=sys.stderr)
        return False
    except requests.exceptions.HTTPError as e:
        print(f"[http error] {url}: {e}", file=sys.stderr)
        return False
    except requests.exceptions.RequestException as e:
        print(f"[network error] {url}: {e}", file=sys.stderr)
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)
    print(f"[ok] {dest.name} ({len(resp.content)} bytes)")
    return True


def fetch_all(documents=DOCUMENTS, raw_dir: Path = RAW_DIR) -> int:
    ok = 0
    with requests.Session() as s:
        for name, url in documents:
            if download(url, raw_dir / name, s):
                ok += 1
    print(f"Downloaded {ok}/{len(documents)} documents into {raw_dir}")
    return ok


if __name__ == "__main__":
    sys.exit(0 if fetch_all() else 1)
