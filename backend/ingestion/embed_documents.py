import os
import time
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

from backend.ingestion.document_loader import load_documents
from backend.ingestion.text_chunker import chunk_text
from backend.services.ai_service import client


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


def get_embedding_with_retry(text, retries=5):
    for attempt in range(retries):
        try:
            response = client.models.embed_content(
                model="gemini-embedding-2",
                contents=text,
                config={"output_dimensionality": 768}
            )

            return response.embeddings[0].values

        except Exception as e:
            if attempt == retries - 1:
                raise

            wait_time = 2 ** attempt

            print(
                f"Gemini request failed: {type(e).__name__}"
            )
            print(f"Retrying in {wait_time} seconds...")

            time.sleep(wait_time)


def embed_documents():
    documents = load_documents()

    conn = get_connection()
    cursor = conn.cursor()

    stored_count = 0
    skipped_count = 0

    for document in documents:

        filename = document["filename"]
        chunks = chunk_text(document["text"])

        cursor.execute(
            """
            INSERT INTO documents (filename)
            VALUES (%s)
            ON CONFLICT (filename)
            DO UPDATE SET filename = EXCLUDED.filename
            RETURNING id
            """,
            (filename,)
        )

        document_id = cursor.fetchone()[0]
        conn.commit()

        print(f"\nProcessing: {filename}")

        for index, chunk in enumerate(chunks):

            # Check whether this chunk is already stored
            cursor.execute(
                """
                SELECT id
                FROM chunks
                WHERE document_id = %s
                AND chunk_index = %s
                """,
                (document_id, index)
            )

            existing_chunk = cursor.fetchone()

            if existing_chunk:
                skipped_count += 1
                print(
                    f"Skipped: {filename} "
                    f"chunk {index + 1}/{len(chunks)}"
                )
                continue

            # Generate embedding with retry
            embedding = get_embedding_with_retry(chunk)

            embedding_string = "[" + ",".join(
                str(value) for value in embedding
            ) + "]"

            cursor.execute(
                """
                INSERT INTO chunks
                (document_id, chunk_index, content, embedding)
                VALUES (%s, %s, %s, %s::vector)
                """,
                (
                    document_id,
                    index,
                    chunk,
                    embedding_string
                )
            )

            conn.commit()

            stored_count += 1

            print(
                f"Stored: {filename} "
                f"chunk {index + 1}/{len(chunks)}"
            )

    cursor.close()
    conn.close()

    print("\nEmbedding process completed!")
    print(f"New chunks stored: {stored_count}")
    print(f"Existing chunks skipped: {skipped_count}")


if __name__ == "__main__":
    embed_documents()