from src.retrieval.search import search


FAILED_QUESTIONS = [
    {
        "id": "q005",
        "question": "What precautions should I take when using ATMs in Fiji?",
        "relevant_chunk_ids": [
            "fiji_travel_safety_chunk_2",
            "fiji_travel_safety_chunk_9"
        ]
    },
    {
        "id": "q015",
        "question": "What should I check before travelling by boat in Fiji?",
        "relevant_chunk_ids": [
            "fiji_travel_safety_chunk_43"
        ]
    },
    {
        "id": "q020",
        "question": "What is the most convenient way to travel to and island-hop around the Yasawa Islands?",
        "relevant_chunk_ids": [
            "yasawa_guide_chunk_3",
            "yasawa_guide_chunk_4"
        ]
    },
    {
        "id": "q040",
        "question": "What areas can I explore using Nadi as a base?",
        "relevant_chunk_ids": [
            "nadi_guide_chunk_1"
        ]
    }
]


DIAGNOSTIC_K = 50


def main():

    print(
        f"\nSearching top {DIAGNOSTIC_K} results "
        "for persistent retrieval failures..."
    )

    for question_data in FAILED_QUESTIONS:

        print("\n" + "=" * 80)
        print(
            f"{question_data['id']}: "
            f"{question_data['question']}"
        )
        print("=" * 80)

        results = search(
            query=question_data["question"],
            n_results=DIAGNOSTIC_K
        )

        retrieved_ids = results["ids"][0]
        distances = results["distances"][0]

        relevant_ids = set(
            question_data["relevant_chunk_ids"]
        )

        print("\nExpected chunks:")

        for chunk_id in relevant_ids:
            print(f"  - {chunk_id}")

        print("\nRanks of expected chunks:")

        found_any = False

        for rank, (chunk_id, distance) in enumerate(
            zip(retrieved_ids, distances),
            start=1
        ):
            if chunk_id in relevant_ids:

                found_any = True

                print(
                    f"  {chunk_id}: "
                    f"rank {rank} "
                    f"(distance: {distance:.4f})"
                )

        if not found_any:
            print(
                f"  No expected chunks found "
                f"in top {DIAGNOSTIC_K}."
            )

        print("\nTop 10 retrieved chunks:")

        for rank, (chunk_id, distance) in enumerate(
            zip(
                retrieved_ids[:10],
                distances[:10]
            ),
            start=1
        ):

            marker = (
                "✓"
                if chunk_id in relevant_ids
                else ""
            )

            print(
                f"  {rank:>2}. "
                f"{chunk_id:<45} "
                f"{distance:.4f} {marker}"
            )


if __name__ == "__main__":
    main()