"""Download GST Council source documents into data/raw/."""

from pathlib import Path
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

PDF_URL = (
    "https://gstcouncil.gov.in/sites/default/files/2025-09/"
    "press_release_press_information_bureau.pdf"
)
FAQ_URL = "https://gstcouncil.gov.in/en/faq?page={}"
TIMEOUT = 30
HEADERS = {"User-Agent": "GSTSaralStudentProject/1.0 (educational use)"}


def download_file(url: str, destination: Path) -> bool:
    """Download one URL safely. Return True only when saved successfully."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        destination.write_bytes(response.content)
        print(f"Downloaded: {destination.name}")
        return True
    except requests.exceptions.Timeout:
        print(f"Timeout while downloading: {url}")
    except requests.exceptions.HTTPError as exc:
        print(f"HTTP error for {url}: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"Network error for {url}: {exc}")
    except OSError as exc:
        print(f"File error for {destination}: {exc}")
    return False


def save_faq_page(page_number: int) -> bool:
    """Download and save one FAQ page as HTML and extracted readable text."""
    url = FAQ_URL.format(page=page_number)
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        html_path = RAW_DIR / f"gst_faq_page_{page_number}.html"
        html_path.write_bytes(response.content)

        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup(["script", "style", "noscript"]):
            element.decompose()
        text_path = RAW_DIR / f"gst_faq_page_{page_number}.txt"
        text_path.write_text(soup.get_text("\n", strip=True), encoding="utf-8")
        print(f"Downloaded FAQ page {page_number}")
        return True
    except requests.exceptions.Timeout:
        print(f"Timeout while downloading FAQ page {page_number}")
    except requests.exceptions.RequestException as exc:
        print(f"Could not download FAQ page {page_number}: {exc}")
    except OSError as exc:
        print(f"Could not save FAQ page {page_number}: {exc}")
    return False


def extract_pdf_text(pdf_path: Path) -> None:
    """Extract text from the downloaded PDF for inspection and ingestion."""
    try:
        reader = PdfReader(str(pdf_path))
        pages = [page.extract_text() or "" for page in reader.pages]
        output = "\n\n".join(pages)
        (RAW_DIR / "press_release_text.txt").write_text(output, encoding="utf-8")
        print(f"Extracted text from {len(reader.pages)} PDF pages")
    except Exception as exc:
        print(f"Could not extract PDF text: {exc}")


def main() -> None:
    print("Starting GSTSaral source download...\n")
    # Three FAQ pages plus the press release PDF = four source documents.
    faq_successes = sum(save_faq_page(page) for page in range(3))

    pdf_path = RAW_DIR / "56th_gst_council_press_release.pdf"
    if download_file(PDF_URL, pdf_path):
        extract_pdf_text(pdf_path)

    print(f"\nFAQ pages downloaded successfully: {faq_successes}/3")
    print(f"Raw files are stored in: {RAW_DIR}")


if __name__ == "__main__":
    main()
