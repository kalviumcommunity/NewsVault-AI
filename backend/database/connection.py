import psycopg2
from backend.config.settings import DATABASE_URL


def get_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not configured.")

    try:
        connection = psycopg2.connect(DATABASE_URL)
        return connection

    except psycopg2.Error as error:
        raise ConnectionError(
            f"Failed to connect to PostgreSQL: {error}"
        )