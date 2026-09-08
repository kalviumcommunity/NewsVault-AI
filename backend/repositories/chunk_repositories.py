from backend.database.db_connection import get_connection


def create_chunk(
    document_id: int,
    chunk_index: int,
    content: str,
    page_start: int | None = None,
    page_end: int | None = None
):
    """
    Store a document chunk in PostgreSQL.
    """

    if not content or not content.strip():
        raise ValueError("Chunk content cannot be empty.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO chunks (
                document_id,
                chunk_index,
                content,
                page_start,
                page_end
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """

        cursor.execute(
            query,
            (
                document_id,
                chunk_index,
                content,
                page_start,
                page_end
            )
        )

        chunk_id = cursor.fetchone()[0]

        connection.commit()

        return chunk_id

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def get_chunks(document_id: int):
    """
    Retrieve all chunks belonging to a document.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                id,
                document_id,
                chunk_index,
                content,
                page_start,
                page_end,
                created_at
            FROM chunks
            WHERE document_id = %s
            ORDER BY chunk_index;
        """

        cursor.execute(query, (document_id,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()