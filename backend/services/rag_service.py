from backend.retrieval.retriever import retrieve_chunks
from backend.services.ai_service import generate_response


INSUFFICIENT_CONTEXT_MESSAGE = (
    "The archive does not contain sufficient information "
    "to answer this question using the retrieved evidence."
)


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
    # Retrieve relevant chunks using selected filters
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

    # --------------------------------------------------
    # Handle insufficient archive context
    # --------------------------------------------------
    if not results:
        return {
            "answer": INSUFFICIENT_CONTEXT_MESSAGE,
            "sources": [],
            "insufficient_context": True
        }

    # --------------------------------------------------
    # Build source-aware context
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Evidence-aware Gemini prompt
    # --------------------------------------------------
    prompt = f"""
You are NewsVault AI, a journalism research assistant.

Your ONLY source of information is the retrieved archive evidence
provided below.

STRICT EVIDENCE RULES:

- Use ONLY information explicitly present in the retrieved evidence.
- Do NOT use outside knowledge or information from your training.
- Do NOT invent, assume, estimate, predict, or fill in missing information.
- Every factual claim must be directly supported by the retrieved evidence.
- Cite the supporting source immediately after each factual claim using
  [Source 1], [Source 2], etc.
- If multiple sources support a claim, cite all relevant sources.
- Never cite a source that does not support the claim.
- If the evidence supports only part of the question, answer only the
  supported part and clearly mention what information is missing.
- If the retrieved evidence does not contain enough information to
  answer the question, return exactly this message:

"The archive does not contain sufficient information to answer this
question using the retrieved evidence."

User question:
{question}

Retrieved archive evidence:
{context}

Instructions:

- Give a clear and concise answer.
- Use only the retrieved archive evidence.
- Include numbers, dates, and facts only when supported by the evidence.
- Add [Source X] citations to factual claims.
- Do not add information that is not present in the retrieved evidence.
- Do not answer using general knowledge.
- Do not guess or make assumptions.
"""

    # --------------------------------------------------
    # Generate evidence-grounded answer
    # --------------------------------------------------
    answer = generate_response(prompt)

    return {
        "answer": answer,
        "sources": sources,
        "insufficient_context": False
    }