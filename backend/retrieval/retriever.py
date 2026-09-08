import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

from backend.services.ai_service import embed_query


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def retrieve_chunks(question: str, top_k: int = 5):
    query_embedding = embed_query(question)

    embedding_string = "[" + ",".join(
        str(value) for value in query_embedding
    ) + "]"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            d.filename,
            c.chunk_index,
            c.content,
            1 - (c.embedding <=> %s::vector) AS similarity
        FROM chunks c
        JOIN documents d
            ON d.id = c.document_id
        ORDER BY c.embedding <=> %s::vector
        LIMIT %s
        """,
        (embedding_string, embedding_string, top_k)
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


if __name__ == "__main__":
    question = "What is the current GDP growth rate of India?"

    results = retrieve_chunks(question)

    print("\nTop relevant chunks:\n")

    for filename, chunk_index, content, similarity in results:
        print(f"Source: {filename}")
        print(f"Chunk: {chunk_index}")
        print(f"Similarity: {similarity:.4f}")
        print(f"Content: {content[:300]}...")
        print("-" * 60)