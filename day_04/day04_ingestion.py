import json
from pathlib import Path
from pypdf import PdfReader


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENT_DIR = BASE_DIR / "data" / "documents"
OUTPUT_DIR = BASE_DIR / "data" / "extracted"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Function to read TXT files
def load_txt(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Function to read PDF files
def load_pdf(file_path):

    reader = PdfReader(str(file_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


# Function to ingest documents
def ingest_documents():

    documents = []

    for file_path in DOCUMENT_DIR.iterdir():

        if not file_path.is_file():
            continue

        print(f"\nProcessing: {file_path.name}")

        try:

            if file_path.suffix.lower() == ".txt":

                text = load_txt(file_path)

                documents.append({
                    "filename": file_path.name,
                    "file_type": "TXT",
                    "page": None,
                    "text": text
                })

            elif file_path.suffix.lower() == ".pdf":

                pages = load_pdf(file_path)

                for page in pages:

                    documents.append({
                        "filename": file_path.name,
                        "file_type": "PDF",
                        "page": page["page"],
                        "text": page["text"]
                    })

            else:
                print("Unsupported file type. Skipping.")

        except Exception as error:

            print(f"Error processing {file_path.name}: {error}")

    return documents


# Main program
if __name__ == "__main__":

    print("===== GSTSARAL DATA INGESTION =====")

    extracted_data = ingest_documents()

    output_file = OUTPUT_DIR / "extracted_data.json"

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            extracted_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nTotal extracted records:", len(extracted_data))

    print("Output saved at:", output_file)

    print("\nDay 04 Data Ingestion Completed!")
