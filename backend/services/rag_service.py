from backend.retrieval.retriever import retrieve_chunks
from backend.services.ai_service import generate_response


def answer_question(question: str) -> str:
    results = retrieve_chunks(question, top_k=5)

    if not results:
        return "I could not find relevant information in the archive."

    context_parts = []

    for filename, chunk_index, content, similarity in results:
        context_parts.append(
            f"Source: {filename}\n"
            f"Chunk: {chunk_index}\n"
            f"Content:\n{content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are NewsVault AI, a journalism research assistant.

Answer the user's question using ONLY the information provided
in the archive context below.

If the context does not contain enough information to answer,
clearly say that the archive does not contain sufficient information.

Do not invent facts or use outside knowledge.

User question:
{question}

Archive context:
{context}

Instructions:
- Give a clear and concise answer.
- Mention relevant numbers, dates, and facts from the context.
- At the end, provide the source filename(s) used.
"""

    return generate_response(prompt)


if __name__ == "__main__":
    question = "What is India's GDP growth rate for FY 2025-26?"

    answer = answer_question(question)

    print("\nNewsVault AI Answer:\n")
    print(answer)