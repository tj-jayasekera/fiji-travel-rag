from pathlib import Path
import json
import re

from pypdf import PdfReader


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
SOURCES_FILE = Path("data/sources.json")


def clean_text(text: str) -> str:
    # Remove tracking parameters
    text = re.sub(r"\?utm_source=[^\s]+", "", text)

    # Remove printed webpage headers
    text = re.sub(
        r"\d{2}/\d{2}/\d{4},\s*\d{1,2}:\d{2}.*?\n",
        "",
        text
    )

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Remove standalone page numbers
    text = re.sub(
        r"^\s*\d+/\d+\s*$",
        "",
        text,
        flags=re.MULTILINE
    )

    # Remove common webpage UI leftovers
    text = re.sub(
        r"^\s*(Less|More)\s*$",
        "",
        text,
        flags=re.MULTILINE
    )

    # Fix spaces around apostrophes
    text = re.sub(r"\s+[’']\s+", "’", text)

    # Collapse repeated spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)

    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text)

    return "\n".join(pages_text)


def load_sources():
    with open(SOURCES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_processed_document(source: dict, text: str):
    output_file = PROCESSED_DATA_DIR / f"{source['id']}.json"

    document = {
        "id": source["id"],
        "title": source["title"],
        "category": source["category"],
        "source": source["source"],
        "url": source["url"],
        "file": source["file"],
        "text": text
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            document,
            file,
            ensure_ascii=False,
            indent=2
        )


def main():
    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    sources = load_sources()

    print(f"Found {len(sources)} sources.\n")

    for source in sources:
        pdf_path = RAW_DATA_DIR / source["file"]

        if not pdf_path.exists():
            print(f"Missing: {pdf_path}")
            continue

        print(f"Processing: {source['title']}")

        raw_text = extract_pdf_text(pdf_path)
        cleaned_text = clean_text(raw_text)

        save_processed_document(
            source,
            cleaned_text
        )

        print(
            f"  Raw characters: {len(raw_text)}"
        )

        print(
            f"  Cleaned characters: {len(cleaned_text)}"
        )

        print("  Saved.\n")

    print("Ingestion complete.")


if __name__ == "__main__":
    main()