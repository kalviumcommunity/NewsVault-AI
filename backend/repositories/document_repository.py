from datetime import date
from typing import Optional

from backend.database.connection import get_connection


def create_document(
    title: str,
    filename: str,
    document_type: str,
    author: Optional[str] = None,
    document_date: Optional[date] = None,
    topic: Optional[str] = None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents
                (filename, content_type, author, document_date, topic)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
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
                    filename,
                    content_type,
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
        connection.close()


def filter_documents(
    document_date=None,
    author=None,
    document_type=None,
    topic=None,
    date_from=None,
    date_to=None
):
    connection = get_connection()

    try:
        query = """
            SELECT
                id,
                filename,
                content_type,
                author,
                document_date,
                topic,
                created_at
            FROM documents
        """

        conditions = []
        parameters = []

        if document_date is not None:
            conditions.append("document_date = %s")
            parameters.append(document_date)

        if date_from is not None:
            conditions.append("document_date >= %s")
            parameters.append(date_from)

        if date_to is not None:
            conditions.append("document_date <= %s")
            parameters.append(date_to)

        if author is not None:
            conditions.append("author = %s")
            parameters.append(author)

        if document_type is not None:
            conditions.append("content_type = %s")
            parameters.append(document_type)

        if topic is not None:
            conditions.append("topic = %s")
            parameters.append(topic)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY document_date DESC, id DESC"

        with connection.cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()

    finally:
        connection.close()