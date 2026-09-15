import os
import re
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

from backend.services.ai_service import embed_query


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# Database connection
# --------------------------------------------------

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# --------------------------------------------------
# Text normalization
# --------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Normalize text for keyword matching.
    """

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text
    )

    return " ".join(text.split())


# --------------------------------------------------
# Extract meaningful keywords
# --------------------------------------------------

def extract_keywords(question: str) -> list[str]:
    """
    Extract important keywords from the user question.
    """

    stop_words = {
        "what",
        "was",
        "were",
        "is",
        "are",
        "the",
        "a",
        "an",
        "in",
        "of",
        "for",
        "to",
        "on",
        "at",
        "and",
        "or",
        "with",
        "by",
        "from",
        "during",
        "this",
        "that",
        "which",
        "how",
        "much",
        "many",
        "did",
        "do",
        "does",
        "can",
        "could",
        "would",
        "should"
    }

    normalized = normalize_text(question)

    words = normalized.split()

    return [
        word
        for word in words
        if word not in stop_words
        and len(word) >= 2
    ]


# --------------------------------------------------
# Calculate lexical relevance
# --------------------------------------------------

def calculate_keyword_score(
    question: str,
    filename: str,
    content: str
) -> float:
    """
    Calculate additional relevance based on
    keyword matches in the filename and content.
    """

    keywords = extract_keywords(question)

    if not keywords:
        return 0.0

    normalized_filename = normalize_text(filename)
    normalized_content = normalize_text(content)

    score = 0.0

    for keyword in keywords:

        # Strong signal when keyword appears in filename
        if keyword in normalized_filename:
            score += 0.15

        # Content keyword match
        if keyword in normalized_content:
            score += 0.03

    # --------------------------------------------------
    # Phrase-level relevance
    # --------------------------------------------------

    normalized_question = normalize_text(question)

    important_phrases = [
        "real gdp",
        "gdp growth",
        "growth rate",
        "fy 2025 26",
        "2025 26"
    ]

    for phrase in important_phrases:

        if phrase in normalized_question:

            if phrase in normalized_filename:
                score += 0.10

            if phrase in normalized_content:
                score += 0.05

    return score


# --------------------------------------------------
# Filter-aware vector retrieval
# --------------------------------------------------

def retrieve_chunks(
    question: str,
    top_k: int = 5,
    similarity_threshold: float = 0.70,
    date_start: int | None = None,
    date_end: int | None = None,
    content_type: str | None = None,
    author: str | None = None,
    topic: str | None = None,
    keywords: str | None = None
):

    # --------------------------------------------------
    # Validate question
    # --------------------------------------------------

    if not question or not question.strip():
        return []

    question = question.strip()

    # --------------------------------------------------
    # Create query embedding
    # --------------------------------------------------

    query_embedding = embed_query(question)

    embedding_string = (
        "["
        + ",".join(str(value) for value in query_embedding)
        + "]"
    )

    # --------------------------------------------------
    # Retrieve more candidates before reranking
    # --------------------------------------------------

    candidate_limit = max(
        top_k * 4,
        20
    )

    # --------------------------------------------------
    # Base query
    # --------------------------------------------------

    query = """
        SELECT
            c.id AS chunk_id,
            c.document_id,
            c.chunk_index,
            c.content,
            d.filename,
            d.content_type,
            d.author,
            d.document_date,
            d.topic,
            1 - (c.embedding <=> %s::vector) AS similarity
        FROM chunks c
        JOIN documents d
            ON d.id = c.document_id
    """

    params = [embedding_string]
    conditions = []

    # --------------------------------------------------
    # Date filter
    # --------------------------------------------------

    if date_start is not None:
        conditions.append(
            "EXTRACT(YEAR FROM d.document_date) >= %s"
        )
        params.append(date_start)

    if date_end is not None:
        conditions.append(
            "EXTRACT(YEAR FROM d.document_date) <= %s"
        )
        params.append(date_end)

    # --------------------------------------------------
    # Content type filter
    # --------------------------------------------------

    if content_type and content_type != "All Types":
        conditions.append(
            "d.content_type = %s"
        )
        params.append(content_type)

    # --------------------------------------------------
    # Author filter
    # --------------------------------------------------

    if author and author != "All Authors":
        conditions.append(
            "d.author = %s"
        )
        params.append(author)

    # --------------------------------------------------
    # Topic filter
    # --------------------------------------------------

    if topic and topic != "All Topics":
        conditions.append(
            "d.topic = %s"
        )
        params.append(topic)

    # --------------------------------------------------
    # Keyword filter
    # --------------------------------------------------

    if keywords:
        conditions.append(
            "c.content ILIKE %s"
        )
        params.append(f"%{keywords}%")

    # --------------------------------------------------
    # Add WHERE conditions
    # --------------------------------------------------

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # --------------------------------------------------
    # Vector similarity ranking
    # --------------------------------------------------

    query += """
        ORDER BY c.embedding <=> %s::vector
        LIMIT %s
    """

    params.append(embedding_string)
    params.append(candidate_limit)

    # --------------------------------------------------
    # Execute query
    # --------------------------------------------------

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            query,
            tuple(params)
        )

        results = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    # --------------------------------------------------
    # Remove low-relevance chunks
    # --------------------------------------------------

    results = [
        result
        for result in results
        if result[9] >= similarity_threshold
    ]

    # --------------------------------------------------
    # Rerank using semantic + keyword relevance
    # --------------------------------------------------

    reranked_results = []

    for result in results:

        filename = result[4]
        content = result[3]
        similarity = result[9]

        keyword_score = calculate_keyword_score(
            question=question,
            filename=filename,
            content=content
        )

        final_score = similarity + keyword_score

        reranked_results.append(
            (
                final_score,
                result
            )
        )

    # --------------------------------------------------
    # Sort by final relevance
    # --------------------------------------------------

    reranked_results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    # --------------------------------------------------
    # Select top results
    # --------------------------------------------------

    reranked_results = reranked_results[:top_k]

    # --------------------------------------------------
    # Return RAG-compatible format
    # --------------------------------------------------

    formatted_results = []

    for _, result in reranked_results:

        formatted_results.append(
            (
                result[4],   # filename
                result[2],   # chunk_index
                result[3],   # content
                result[9]    # original similarity
            )
        )

    return formatted_results