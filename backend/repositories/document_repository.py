from datetime import date
from typing import Optional

from backend.database.connection import get_connection


def create_document(
    title:str,
    filename:str,
    document_type:str,
    author:Optional[str]=None,
    document_date:Optional[date]=None,
    topic:Optional[str]=None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents
                (title, filename, document_type, author, document_date, topic)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    title,
                    filename,
                    document_type,
                    author,
                    document_date,
                    topic
                )
            )

            document_id = cursor.fetchone()[0]
            connection.commit()

            return document_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_document(document_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    filename,
                    document_type,
                    author,
                    document_date,
                    topic,
                    created_at
                FROM documents
                WHERE id = %s;
                """,
                (document_id,)
            )

            return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()