from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


CHROMA_DIR = Path("data/chroma")

COLLECTION_NAME = "fiji_travel"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_collection():
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    return client.get_collection(
        name=COLLECTION_NAME
    )


def search(query: str, n_results: int = 5):
    # Load the same embedding model used for documents
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Convert the user's question into an embedding
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    # Load vector database
    collection = load_collection()

    # Find the most semantically similar chunks
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    return results


def print_results(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for index, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1
    ):
        print("\n" + "=" * 70)
        print(f"RESULT {index}")
        print("=" * 70)

        print(f"Title: {metadata['title']}")
        print(f"Category: {metadata['category']}")
        print(f"Source: {metadata['source']}")
        print(f"Distance: {distance:.4f}")

        print("\nText:")
        print(document)


def main():
    query = input("\nAsk a Fiji travel question: ")

    results = search(query)

    print_results(results)


if __name__ == "__main__":
    main()