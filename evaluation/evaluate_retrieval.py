from pathlib import Path
import json

from src.retrieval.search import search


QUESTIONS_FILE = Path("evaluation/questions.json")


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_question(question_data, top_k):
    question = question_data["question"]
    relevant_chunk_ids = set(question_data["relevant_chunk_ids"])

    results = search(
        query=question,
        n_results=top_k
    )

    retrieved_chunk_ids = results["ids"][0]

    relevant_retrieved = [
        chunk_id
        for chunk_id in retrieved_chunk_ids
        if chunk_id in relevant_chunk_ids
    ]

    hit = 1 if relevant_retrieved else 0

    precision = len(relevant_retrieved) / top_k

    recall = (
        len(relevant_retrieved)
        / len(relevant_chunk_ids)
    )

    reciprocal_rank = 0.0

    for rank, chunk_id in enumerate(
        retrieved_chunk_ids,
        start=1
    ):
        if chunk_id in relevant_chunk_ids:
            reciprocal_rank = 1 / rank
            break

    return {
        "id": question_data["id"],
        "question": question,
        "expected_chunks": list(relevant_chunk_ids),
        "retrieved_chunks": retrieved_chunk_ids,
        "hit": hit,
        "precision_at_k": precision,
        "recall_at_k": recall,
        "reciprocal_rank": reciprocal_rank
    }


def evaluate_at_k(questions, top_k):
    results = []

    for question in questions:
        result = evaluate_question(
            question,
            top_k
        )

        results.append(result)

    total = len(results)

    hit_rate = (
        sum(result["hit"] for result in results)
        / total
    )

    mean_precision = (
        sum(
            result["precision_at_k"]
            for result in results
        )
        / total
    )

    mean_recall = (
        sum(
            result["recall_at_k"]
            for result in results
        )
        / total
    )

    mrr = (
        sum(
            result["reciprocal_rank"]
            for result in results
        )
        / total
    )

    failed_questions = [
        result["id"]
        for result in results
        if result["hit"] == 0
    ]

    return {
        "top_k": top_k,
        "hit_rate": hit_rate,
        "mean_precision": mean_precision,
        "mean_recall": mean_recall,
        "mrr": mrr,
        "failed_questions": failed_questions
    }


def main():
    questions = load_questions()

    answerable_questions = [
        question
        for question in questions
        if question["relevant_chunk_ids"]
    ]

    print(
        f"Loaded {len(questions)} total evaluation questions."
    )

    print(
        f"Evaluating {len(answerable_questions)} "
        f"answerable questions..."
    )

    top_k = 5

    print(f"\nEvaluating k={top_k}...")

    result = evaluate_at_k(
        answerable_questions,
        top_k
    )

    print("\n" + "=" * 78)
    print("RETRIEVAL EVALUATION")
    print("=" * 78)

    print(f"Top-K: {result['top_k']}")
    print(f"Hit Rate@5: {result['hit_rate']:.3f}")
    print(f"Precision@5: {result['mean_precision']:.3f}")
    print(f"Recall@5: {result['mean_recall']:.3f}")
    print(f"MRR: {result['mrr']:.3f}")

    failed = result["failed_questions"]

    if failed:
        failed_text = ", ".join(failed)
    else:
        failed_text = "None"

    print(f"\nFailed questions: {failed_text}")


if __name__ == "__main__":
    main()