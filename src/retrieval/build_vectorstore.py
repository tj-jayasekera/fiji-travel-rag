from pathlib import Path
import json

import chromadb
from chromadb.errors import NotFoundError
from sentence_transformers import SentenceTransformer


CHUNKS_FILE = Path("data/processed/chunks.json")
CHROMA_DIR = Path("data/chroma")

COLLECTION_NAME = "fiji_travel"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    # Load chunks
    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks.")

    # Load embedding model
    print(f"Loading embedding model: {EMBEDDING_MODEL}")

    model = SentenceTransformer(EMBEDDING_MODEL)

    # Extract the text from each chunk
    texts = [chunk["text"] for chunk in chunks]

    print("Creating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    print(f"Created {len(embeddings)} embeddings.")
    print(f"Embedding dimensions: {embeddings.shape[1]}")

    # Create persistent Chroma database
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    # Delete the existing collection if rebuilding
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Deleted existing Chroma collection.")
    except NotFoundError:
        print("No existing collection found. Creating a new one.")

    # Create a fresh collection
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    ids = []
    documents = []
    metadatas = []

    # Prepare data for Chroma
    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        documents.append(chunk["text"])

        metadatas.append({
            "document_id": chunk["document_id"],
            "title": chunk["title"],
            "category": chunk["category"],
            "source": chunk["source"],
            "url": chunk["url"]
        })

    # Store chunks, embeddings, and metadata
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print(f"Stored {collection.count()} chunks in Chroma.")
    print(f"Vector database saved to: {CHROMA_DIR}")


if __name__ == "__main__":
    main()