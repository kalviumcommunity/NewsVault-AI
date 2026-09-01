from backend.database.connection import get_connection


def format_vector(vector):
    if vector is None:
        return None

    return "[" + ",".join(str(value) for value in vector) + "]"


def create_chunk(
    document_id,
    chunk_index,
    content,
    page_start=None,
    page_end=None,
    embedding=None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            embedding = format_vector(embedding)

            cursor.execute(
                """
                INSERT INTO chunks
                (
                    document_id,
                    chunk_index,
                    content,
                    page_start,
                    page_end,
                    embedding
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    document_id,
                    chunk_index,
                    content,
                    page_start,
                    page_end,
                    embedding
                )
            )

            chunk_id = cursor.fetchone()[0]
            connection.commit()

            return chunk_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

        

def get_chunks(document_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    document_id,
                    chunk_index,
                    content,
                    page_start,
                    page_end,
                    embedding,
                    created_at
                FROM chunks
                WHERE document_id = %s
                ORDER BY chunk_index;
                """,
                (document_id,)
            )

            return cursor.fetchall()

    finally:
        connection.close()