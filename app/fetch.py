

import requests
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

DOCUMENTS = {
    "gst_faq_page_0.html":
        "https://gstcouncil.gov.in/en/faq?page=0",

    "press_release_56th.pdf":
        "https://gstcouncil.gov.in/sites/default/files/2025-09/press_release_press_information_bureau.pdf",

    "gst_faq_page_1.html":
        "https://gstcouncil.gov.in/en/faq?page=1",

    "gst_faq_page_2.html":
        "https://gstcouncil.gov.in/en/faq?page=2"
}


def download_documents():

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for filename, url in DOCUMENTS.items():

        file_path = RAW_DIR / filename

        try:
            print(f"\nDownloading: {filename}")

            response = requests.get(
                url,
                timeout=(10, 30),
                headers={"User-Agent": "Mozilla/5.0"}
            )

            response.raise_for_status()

            if not response.content:
                raise ValueError("Downloaded file is empty")

            file_path.write_bytes(response.content)

            print(f"Successfully saved: {file_path}")

        except requests.exceptions.Timeout:
            print(f"Timeout error: {filename}")

        except requests.exceptions.RequestException as error:
            print(f"Download error: {filename} - {error}")

        except (OSError, ValueError) as error:
            print(f"File error: {filename} - {error}")


if __name__ == "__main__":
    download_documents()
