import psycopg2

from backend.config.settings import (
    DATABASE_URL,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_connection():
    try:
        if DATABASE_URL:
            return psycopg2.connect(DATABASE_URL)

        if not DB_PASSWORD:
            raise ValueError(
                "PostgreSQL database configuration is not configured."
            )

        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )

    except psycopg2.Error as error:
        raise ConnectionError(
            f"Failed to connect to PostgreSQL: {error}"
        ) from error