from sentence_transformers import CrossEncoder

from src.retrieval.search import search


RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

CANDIDATE_K = 20
FINAL_K = 5


reranker = CrossEncoder(RERANKER_MODEL)


def rerank_search(query: str):
    # Step 1: retrieve a broader candidate set
    results = search(
        query=query,
        n_results=CANDIDATE_K
    )

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Step 2: score each query-document pair
    pairs = [
        [query, document]
        for document in documents
    ]

    scores = reranker.predict(pairs)

    # Step 3: combine everything
    ranked_results = []

    for chunk_id, document, metadata, score in zip(
        ids,
        documents,
        metadatas,
        scores
    ):
        ranked_results.append({
            "chunk_id": chunk_id,
            "text": document,
            "metadata": metadata,
            "reranker_score": float(score)
        })

    # Step 4: sort highest score first
    ranked_results.sort(
        key=lambda item: item["reranker_score"],
        reverse=True
    )

    # Step 5: return only final top 5
    return ranked_results


def main():
    query = input(
        "\nAsk a Fiji travel question: "
    )

    results = rerank_search(query)

    for rank, result in enumerate(
        results,
        start=1
    ):
        print("\n" + "=" * 70)
        print(f"RESULT {rank}")
        print("=" * 70)

        print(
            f"Chunk ID: "
            f"{result['chunk_id']}"
        )

        print(
            f"Score: "
            f"{result['reranker_score']:.4f}"
        )

        print(
            f"Title: "
            f"{result['metadata']['title']}"
        )

        print("\nText:")
        print(result["text"])


if __name__ == "__main__":
    main()