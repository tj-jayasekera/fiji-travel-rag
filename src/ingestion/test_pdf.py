from pathlib import Path
import re
from pypdf import PdfReader


pdf_path = Path("data/raw/general.pdf")

reader = PdfReader(pdf_path)

pages_text = []

for page in reader.pages:
    text = page.extract_text()

    if text:
        pages_text.append(text)

raw_text = "\n".join(pages_text)


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
    text = re.sub(r"^\s*\d+/\d+\s*$", "", text, flags=re.MULTILINE)

    # Remove common webpage UI leftovers
    text = re.sub(r"^\s*(Less|More)\s*$", "", text, flags=re.MULTILINE)

    # Fix spaces around apostrophes
    text = re.sub(r"\s+[’']\s+", "’", text)

    # Collapse repeated spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


cleaned_text = clean_text(raw_text)


print(f"Number of pages: {len(reader.pages)}")
print(f"Raw characters: {len(raw_text)}")
print(f"Cleaned characters: {len(cleaned_text)}")

print("\n--- CLEANED TEXT PREVIEW ---\n")
print(cleaned_text[:3000])