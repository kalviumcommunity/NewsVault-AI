import psycopg2
from backend.config.settings import DATABASE_URL


def get_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not configured.")

    return psycopg2.connect(DATABASE_URL)