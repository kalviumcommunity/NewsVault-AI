from backend.retrieval.retriever import retrieve_chunks
from backend.services.ai_service import generate_response


# --------------------------------------------------
# RAG configuration
# --------------------------------------------------

TOP_K = 5
SIMILARITY_THRESHOLD = 0.70
MAX_CONTEXT_CHARS = 12000

INSUFFICIENT_CONTEXT_MESSAGE = (
    "The archive does not contain sufficient information to answer "
    "this question using the retrieved evidence."
)


# --------------------------------------------------
# Build retrieval context
# --------------------------------------------------

def build_context(results: list[tuple]) -> str:
    """
    Convert retrieved chunks into structured evidence.

    Each source is numbered so Gemini can cite evidence
    using [Source X].
    """

    if not results:
        return ""

    context_parts = []

    for index, result in enumerate(results, start=1):
        filename, chunk_index, content, similarity = result

        source_block = (
            f"[Source {index}]\n"
            f"Filename: {filename}\n"
            f"Chunk: {chunk_index}\n"
            f"Content:\n"
            f"{content}\n"
        )

        context_parts.append(source_block)

    return "\n".join(context_parts)


# --------------------------------------------------
# Build Gemini prompt
# --------------------------------------------------

def build_prompt(question: str, context: str) -> str:
    """
    Build the evidence-grounded prompt used by Gemini.
    """

    return (
        "You are NewsVault AI, an AI-powered journalism research assistant.\n\n"
        "Your task is to answer the user's question using ONLY the retrieved archive evidence provided below.\n\n"

        "EVIDENCE RULES:\n\n"
        "1. Use only information explicitly present in the evidence.\n"
        "2. Do not use outside knowledge or information from training.\n"
        "3. Do not invent, assume, estimate, predict, or fill missing information.\n"
        "4. Every factual statement must be supported by the evidence.\n"
        "5. Cite factual statements immediately using [Source X].\n"
        "6. Use multiple source citations when multiple sources support the same claim.\n"
        "7. Never cite a source that does not support the statement.\n"
        "8. If the evidence supports only part of the question, answer only the supported part and clearly identify the missing information.\n"
        "9. Do not infer facts that are not explicitly stated in the evidence.\n\n"

        "ANSWER RULES:\n\n"
        "- Answer the question directly.\n"
        "- Keep the response concise and informative.\n"
        "- Do not repeat the same fact.\n"
        "- Combine overlapping information from different sources.\n"
        "- Do not unnecessarily restate the question.\n"
        "- Do not repeat the same source citation unnecessarily.\n"
        "- Do not add an unsupported conclusion or opinion.\n"
        "- Preserve important numbers, dates, names, and facts exactly as supported by the evidence.\n"
        "- Use short paragraphs or bullet points when they improve readability.\n"
        "- If the evidence is insufficient, return exactly:\n\n"

        "\"The archive does not contain sufficient information to answer this question using the retrieved evidence.\"\n\n"

        f"USER QUESTION:\n{question}\n\n"
        f"RETRIEVED ARCHIVE EVIDENCE:\n{context}\n\n"

        "Provide the final answer now."
    )


# --------------------------------------------------
# Answer user question
# --------------------------------------------------

def answer_question(
    question: str,
    date_start=None,
    date_end=None,
    content_type=None,
    author=None,
    topic=None,
    keywords=None
) -> dict:
    """
    Complete RAG workflow:

    Question
        ↓
    Query Embedding
        ↓
    Vector Retrieval
        ↓
    Similarity Filtering
        ↓
    Context Limiting
        ↓
    Gemini Answer Generation
        ↓
    Answer + Sources
    """

    # --------------------------------------------------
    # Validate question
    # --------------------------------------------------

    if not question or not question.strip():
        return {
            "answer": "Please enter a question to search the archive.",
            "sources": [],
            "insufficient_context": True
        }

    question = question.strip()

    # --------------------------------------------------
    # Retrieve relevant chunks
    # --------------------------------------------------

    try:
        results = retrieve_chunks(
            question=question,
            top_k=TOP_K,
            similarity_threshold=SIMILARITY_THRESHOLD,
            date_start=date_start,
            date_end=date_end,
            content_type=content_type,
            author=author,
            topic=topic,
            keywords=keywords
        )

    except Exception as error:
        return {
            "answer": f"Unable to retrieve archive evidence: {error}",
            "sources": [],
            "insufficient_context": True
        }

    # --------------------------------------------------
    # Handle insufficient retrieval
    # --------------------------------------------------

    if not results:
        return {
            "answer": INSUFFICIENT_CONTEXT_MESSAGE,
            "sources": [],
            "insufficient_context": True
        }

    # --------------------------------------------------
    # Select chunks within context limit
    # --------------------------------------------------

    selected_results = []
    current_context_length = 0

    for result in results:
        filename, chunk_index, content, similarity = result

        source_number = len(selected_results) + 1

        source_block = (
            f"[Source {source_number}]\n"
            f"Filename: {filename}\n"
            f"Chunk: {chunk_index}\n"
            f"Content:\n"
            f"{content}\n"
        )

        block_length = len(source_block)

        if (
            current_context_length + block_length
            > MAX_CONTEXT_CHARS
        ):
            break

        selected_results.append(result)
        current_context_length += block_length

    # --------------------------------------------------
    # Handle context limit
    # --------------------------------------------------

    if not selected_results:
        return {
            "answer": INSUFFICIENT_CONTEXT_MESSAGE,
            "sources": [],
            "insufficient_context": True
        }

    # --------------------------------------------------
    # Build context
    # --------------------------------------------------

    context = build_context(selected_results)

    if not context.strip():
        return {
            "answer": INSUFFICIENT_CONTEXT_MESSAGE,
            "sources": [],
            "insufficient_context": True
        }

    # --------------------------------------------------
    # Build prompt
    # --------------------------------------------------

    prompt = build_prompt(
        question=question,
        context=context
    )

    # --------------------------------------------------
    # Generate Gemini answer
    # --------------------------------------------------

    try:
        answer = generate_response(prompt)

    except Exception:
        return {
            "answer": (
                "AI service could not generate an answer. "
                "Please try again later."
            ),
            "sources": [
                {
                    "id": f"Source {index}",
                    "filename": result[0],
                    "chunk_index": result[1],
                    "similarity": result[3]
                }
                for index, result in enumerate(
                    selected_results,
                    start=1
                )
            ],
            "insufficient_context": False
        }

    # --------------------------------------------------
    # Handle empty Gemini response
    # --------------------------------------------------

    if not answer or not answer.strip():
        return {
            "answer": (
                "AI service returned an empty response. "
                "Please try again."
            ),
            "sources": [
                {
                    "id": f"Source {index}",
                    "filename": result[0],
                    "chunk_index": result[1],
                    "similarity": result[3]
                }
                for index, result in enumerate(
                    selected_results,
                    start=1
                )
            ],
            "insufficient_context": False
        }

    # --------------------------------------------------
    # Prepare source metadata
    # --------------------------------------------------

    sources = [
        {
            "id": f"Source {index}",
            "filename": result[0],
            "chunk_index": result[1],
            "similarity": result[3]
        }
        for index, result in enumerate(
            selected_results,
            start=1
        )
    ]

    # --------------------------------------------------
    # Return final RAG result
    # --------------------------------------------------

    return {
        "answer": answer.strip(),
        "sources": sources,
        "insufficient_context": False
    }