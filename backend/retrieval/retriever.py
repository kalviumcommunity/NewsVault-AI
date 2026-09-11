import os
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
    # Create query embedding
    # --------------------------------------------------
    query_embedding = embed_query(question)

    embedding_string = (
        "["
        + ",".join(str(value) for value in query_embedding)
        + "]"
    )

    # --------------------------------------------------
    # Base query
    # --------------------------------------------------
    query = """
        SELECT
            d.filename,
            c.chunk_index,
            c.content,
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
    params.append(top_k)

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
        if result[3] >= similarity_threshold
    ]

    return results