from pathlib import Path
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter


PROCESSED_DATA_DIR = Path("data/processed")
CHUNKS_OUTPUT_FILE = Path("data/processed/chunks.json")


def load_processed_documents():
    documents = []

    for file_path in PROCESSED_DATA_DIR.glob("*.json"):
        if file_path.name == "chunks.json":
            continue

        with open(file_path, "r", encoding="utf-8") as file:
            document = json.load(file)
            documents.append(document)

    return documents


def create_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""]
    )


def chunk_documents(documents):
    text_splitter = create_text_splitter()

    chunks = []

    for document in documents:
        split_texts = text_splitter.split_text(document["text"])

        for chunk_index, chunk_text in enumerate(split_texts):
            chunk = {
                "chunk_id": f"{document['id']}_chunk_{chunk_index}",
                "document_id": document["id"],
                "title": document["title"],
                "category": document["category"],
                "source": document["source"],
                "url": document["url"],
                "text": chunk_text
            }

            chunks.append(chunk)

    return chunks


def save_chunks(chunks):
    with open(CHUNKS_OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2
        )


def main():
    documents = load_processed_documents()

    print(f"Loaded {len(documents)} processed documents.")

    chunks = chunk_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    save_chunks(chunks)

    print(f"Saved chunks to {CHUNKS_OUTPUT_FILE}")


if __name__ == "__main__":
    main()