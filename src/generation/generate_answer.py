import os

from dotenv import load_dotenv
from google import genai

from src.retrieval.search import search


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.6-flash"


def build_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for index, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1
    ):
        context_parts.append(
            f"""
SOURCE {index}
Title: {metadata['title']}
Publisher: {metadata['source']}
Category: {metadata['category']}

Content:
{document}
""".strip()
        )

    return "\n\n".join(context_parts)


def build_prompt(question, context):
    return f"""
You are a Fiji travel assistant.

Answer the user's question using ONLY the information provided in the sources below.

Rules:
- Do not use outside knowledge.
- If the sources do not contain enough information to answer the question, say:
  "I don't have enough information in my current Fiji travel sources to answer that."
- Do not invent details.
- Be concise but helpful.
- Mention uncertainty when the source itself is uncertain.
- Do not treat time-sensitive information such as transport schedules as permanently current.
- At the end, include a short "Sources" section listing the source titles you used.

USER QUESTION:
{question}

SOURCES:
{context}
""".strip()


def generate_answer(question):
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY was not found. Check your .env file."
        )

    # Retrieve relevant chunks
    results = search(
        query=question,
        n_results=5
    )

    # Build context from retrieved chunks
    context = build_context(results)

    # Build grounded RAG prompt
    prompt = build_prompt(
        question,
        context
    )

    # Create Gemini client
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    # Generate answer
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    text_parts = []

    for candidate in response.candidates:
        for part in candidate.content.parts:
            if part.text:
                text_parts.append(part.text)

    answer = "\n".join(text_parts)

    return {
        "answer": answer,
        "retrieval_results": results
    }


def main():
    print("\nFiji Travel Assistant")
    print("-" * 40)

    question = input("\nAsk a Fiji travel question: ")

    print("\nSearching Fiji knowledge base...")
    print("Generating answer...\n")

    result = generate_answer(question)

    print(result["answer"])


if __name__ == "__main__":
    main()