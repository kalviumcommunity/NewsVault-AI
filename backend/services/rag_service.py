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
):

    # Retrieve relevant chunks using the selected filters
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

    # No relevant information found
    if not results:
        return {
            "answer": (
                "The archive does not contain sufficient information "
                "to answer this question using the selected filters."
            ),
            "sources": []
        }

    # Build source-aware context
    context_parts = []

    sources = []

    for index, (
        filename,
        chunk_index,
        content,
        similarity
    ) in enumerate(results, start=1):

        source_id = f"Source {index}"

        context_parts.append(
            f"""
[{source_id}]
Filename: {filename}
Chunk: {chunk_index}
Content:
{content}
"""
        )

        sources.append({
            "id": source_id,
            "filename": filename,
            "chunk_index": chunk_index,
            "content": content,
            "similarity": similarity
        })

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are NewsVault AI, a journalism research assistant.

Answer the user's question using ONLY the information provided
in the archive context.

Do not use outside knowledge.
Do not invent facts.

Every factual claim in your answer must be supported by one or
more of the provided sources.

Cite the source immediately after the relevant claim using:
[Source 1]
[Source 2]
etc.

If multiple sources support a claim, cite them like:
[Source 1] [Source 3]

If the archive does not contain enough information to answer
the question, clearly say that the archive does not contain
sufficient information.

User question:
{question}

Archive context:
{context}

Instructions:
- Give a clear and concise answer.
- Use only information from the archive context.
- Include relevant numbers, dates, and facts.
- Add source citations to factual claims.
- Do not create or assume information not present in the sources.
"""

    answer = generate_response(prompt)

    return {
        "answer": answer,
        "sources": sources
    }