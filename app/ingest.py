
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

from app.models import Record


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = BASE_DIR / "data" / "records.json"

SOURCE_URLS = {
    "press_release_56th.pdf":
        "https://gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau.pdf",

    "gst_faq_page_0.html":
        "https://gstcouncil.gov.in/en/faq?page=0",

    "gst_faq_page_1.html":
        "https://gstcouncil.gov.in/en/faq?page=1",

    "gst_faq_page_2.html":
        "https://gstcouncil.gov.in/en/faq?page=2"
}


# Extract text from PDF
def read_pdf(file_path):

    reader = PdfReader(str(file_path))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"

    return text


# Extract text from HTML
def read_html(file_path):

    html = file_path.read_text(
        encoding="utf-8",
        errors="replace"
    )

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)


# Clean and extract records
def clean_records(text, filename, source_url):

    cleaned_records = []

    lines = text.splitlines()

    rate_pattern = re.compile(
        r"(?P<old>\d+(?:\.\d+)?\s*%)\s*"
        r"(?:to|→|->)\s*"
        r"(?P<new>\d+(?:\.\d+)?\s*%)",
        re.IGNORECASE
    )

    for line in lines:

        try:
            line = re.sub(r"\s+", " ", line).strip()

            if not line:
                continue

            match = rate_pattern.search(line)

            if not match:
                continue

            old_rate = match.group("old").replace(" ", "")
            new_rate = match.group("new").replace(" ", "")

            item = line[:match.start()].strip(
                " :-–—•*0123456789."
            )

            # Avoid records without an item/topic
            if not item or len(item) < 3:
                continue

            # Avoid using generic words as item names
            if item.lower() in ["gst rate", "rate", "tax rate"]:
                continue

            # Effective date should be verified from source.
            effective_date = ""

            date_match = re.search(
                r"22\s+(?:September|Sept)\s+2025",
                line,
                re.IGNORECASE
            )

            if date_match:
                effective_date = "2025-09-22"

            elif "press_release" in filename:
                effective_date = "2025-09-22"

            record = Record(
                item_or_topic=item,
                old_rule=old_rate + " GST",
                new_rule=new_rate + " GST",
                effective_from=effective_date,
                document=filename,
                source_url=source_url
            )

            cleaned_records.append(record.to_dict())

        except (ValueError, TypeError, AttributeError) as error:
            print(f"Bad row skipped: {line} | {error}")

        except Exception as error:
            print(f"Unexpected row error: {error}")

    return cleaned_records


# Main ingestion process
def ingest_data():

    all_records = []

    for filename, source_url in SOURCE_URLS.items():

        file_path = RAW_DIR / filename

        if not file_path.exists():
            print(f"File not found, skipping: {filename}")
            continue

        try:
            print(f"\nProcessing: {filename}")

            if filename.endswith(".pdf"):
                text = read_pdf(file_path)

            elif filename.endswith(".html"):
                text = read_html(file_path)

            else:
                print("Unsupported file format")
                continue

            records = clean_records(
                text,
                filename,
                source_url
            )

            all_records.extend(records)

            print("Records extracted:", len(records))

        except Exception as error:
            print(f"Document processing error: {filename} - {error}")

    # Remove exact duplicate records
    unique_records = []
    seen = set()

    for record in all_records:
        key = (
            record["item_or_topic"],
            record["old_rule"],
            record["new_rule"],
            record["document"]
        )

        if key not in seen:
            seen.add(key)
            unique_records.append(record)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            unique_records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nINGESTION COMPLETED")
    print("Total records:", len(unique_records))
    print("Saved file:", OUTPUT_FILE)


if __name__ == "__main__":
    ingest_data()
