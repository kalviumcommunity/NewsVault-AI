from backend.retrieval.retriever import retrieve_chunks
from backend.services.ai_service import generate_response


def answer_question(
    question: str,
    date_start: int | None = None,
    date_end: int | None = None,
    content_type: str | None = None,
    author: str | None = None,
    topic: str | None = None,
    keywords: str | None = None
) -> str:

    # --------------------------------------------------
    # Retrieve filtered chunks
    # --------------------------------------------------
    results = retrieve_chunks(
        question=question,
        top_k=5,
        date_start=date_start,
        date_end=date_end,
        content_type=content_type,
        author=author,
        topic=topic,
        keywords=keywords
    )

    if not results:
        return (
            "The archive does not contain sufficient information "
            "to answer this question using the selected filters."
        )

    # --------------------------------------------------
    # Build archive context
    # --------------------------------------------------
    context_parts = []

    for (
        filename_result,
        chunk_index,
        content,
        similarity
    ) in results:

        context_parts.append(
            f"Source: {filename_result}\n"
            f"Chunk: {chunk_index}\n"
            f"Content:\n{content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # --------------------------------------------------
    # Gemini prompt
    # --------------------------------------------------
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
- Do not use information outside the archive context.
- At the end, provide the source filename(s) used.
- Format each source like this:
  Source: filename.txt
"""

    return generate_response(prompt)