from pathlib import Path
import json

from src.generation.generate_answer import generate_answer


QUESTIONS_FILE = Path("evaluation/questions.json")
RESULTS_DIR = Path("evaluation/results")
RESULTS_FILE = RESULTS_DIR / "generation_results.json"


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_question(question_data):
    result = generate_answer(
        question_data["question"]
    )

    retrieved_chunk_ids = result["retrieval_results"]["ids"][0]

    return {
        "id": question_data["id"],
        "question": question_data["question"],
        "expected_answer": question_data["expected_answer"],
        "generated_answer": result["answer"],
        "is_answerable": bool(
            question_data["relevant_chunk_ids"]
        ),
        "relevant_chunk_ids": question_data["relevant_chunk_ids"],
        "retrieved_chunk_ids": retrieved_chunk_ids,
        "category": question_data["category"],
        "difficulty": question_data["difficulty"]
    }


def main():
    questions = load_questions()

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Load previously completed results if they exist
    if RESULTS_FILE.exists():
        with open(
            RESULTS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            results = json.load(file)

        completed_ids = {
            result["id"]
            for result in results
        }

        print(
            f"Found {len(results)} previously completed questions."
        )

    else:
        results = []
        completed_ids = set()

    print(
        f"Loaded {len(questions)} evaluation questions."
    )

    for index, question in enumerate(
        questions,
        start=1
    ):
        # Skip questions already completed
        if question["id"] in completed_ids:
            print(
                f"[{index}/{len(questions)}] "
                f"Skipping {question['id']} — already completed."
            )
            continue

        print(
            f"[{index}/{len(questions)}] "
            f"Generating answer for {question['id']}..."
        )

        try:
            result = evaluate_question(question)

            results.append(result)

            # Save immediately after every successful question
            with open(
                RESULTS_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    results,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception as error:
            print(
                f"\nStopped at {question['id']}: {error}"
            )

            print(
                f"Saved {len(results)} completed results."
            )

            break

    print("\nGeneration evaluation run finished.")
    print(
        f"Results currently saved: {len(results)}"
    )
    print(
        f"Saved to: {RESULTS_FILE}"
    )


if __name__ == "__main__":
    main()