from backend.retrieval.retriever import retrieve_chunks
from backend.services.ai_service import generate_response


INSUFFICIENT_CONTEXT_MESSAGE = (
    "The archive does not contain sufficient information "
    "to answer this question using the retrieved evidence."
)


# --------------------------------------------------
# RAG answer generation
# --------------------------------------------------
def answer_question(
    question: str,
    date_start: int | None = None,
    date_end: int | None = None,
    content_type: str | None = None,
    author: str | None = None,
    topic: str | None = None,
    keywords: str | None = None
):

    # --------------------------------------------------
    # Retrieve relevant chunks
    # --------------------------------------------------
    results = retrieve_chunks(
        question=question,
        top_k=5,
        similarity_threshold=0.70,
        date_start=date_start,
        date_end=date_end,
        content_type=content_type,
        author=author,
        topic=topic,
        keywords=keywords
    )

    # --------------------------------------------------
    # Handle insufficient context
    # --------------------------------------------------
    if not results:
        return {
            "answer": INSUFFICIENT_CONTEXT_MESSAGE,
            "sources": [],
            "insufficient_context": True
        }

    # --------------------------------------------------
    # Limit retrieved context
    # --------------------------------------------------
    MAX_CONTEXT_CHARS = 12000

    context_parts = []
    sources = []
    current_context_length = 0

    for index, (
        filename,
        chunk_index,
        content,
        similarity
    ) in enumerate(results, start=1):

        source_id = f"Source {index}"

        source_block = (
            f"[{source_id}]\n"
            f"Filename: {filename}\n"
            f"Chunk: {chunk_index}\n"
            f"Content:\n{content}"
        )

        separator_length = 8

        if (
            current_context_length
            + len(source_block)
            + separator_length
            > MAX_CONTEXT_CHARS
        ):
            break

        context_parts.append(source_block)

        sources.append({
            "id": source_id,
            "filename": filename,
            "chunk_index": chunk_index,
            "content": content,
            "similarity": similarity
        })

        current_context_length += (
            len(source_block)
            + separator_length
        )

    # --------------------------------------------------
    # Handle case where context limit removes all chunks
    # --------------------------------------------------
    if not context_parts:
        return {
            "answer": INSUFFICIENT_CONTEXT_MESSAGE,
            "sources": [],
            "insufficient_context": True
        }

    context = "\n\n---\n\n".join(context_parts)

    # --------------------------------------------------
    # Optimized evidence-aware Gemini prompt
    # --------------------------------------------------
    prompt = f"""
You are NewsVault AI, a journalism research assistant.

Answer the user's question using ONLY the retrieved archive evidence.

STRICT RULES:

1. Do not use outside knowledge or information from your training.
2. Do not invent, assume, estimate, predict, or fill missing information.
3. Every factual claim must be supported by the retrieved evidence.
4. Cite factual claims immediately using [Source 1], [Source 2], etc.
5. Use multiple source citations when a claim is supported by multiple sources.
6. Never cite a source that does not support the claim.
7. If only part of the question is supported, answer only that part and
   clearly state what information is missing.
8. If the evidence is insufficient, return exactly:

"The archive does not contain sufficient information to answer this
question using the retrieved evidence."

ANSWER STYLE:

- Be concise and directly answer the question.
- Do not repeat the same fact or idea.
- Combine overlapping information from multiple sources.
- Do not unnecessarily restate the question.
- Do not add a conclusion that is not supported by the evidence.
- Prefer short paragraphs or bullet points when appropriate.
- Include numbers and dates only when supported by the evidence.

User question:
{question}

Retrieved archive evidence:
{context}

Now provide the most relevant, concise, evidence-grounded answer.
"""

    # --------------------------------------------------
    # Generate answer
    # --------------------------------------------------
    answer = generate_response(prompt)

    # --------------------------------------------------
    # Return answer and exact supporting sources
    # --------------------------------------------------
    return {
        "answer": answer,
        "sources": sources,
        "insufficient_context": False
    }