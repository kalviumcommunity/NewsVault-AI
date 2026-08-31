from backend.database.connection import get_connection


def test_connection():
    connection = None

    try:
        connection = get_connection()
        print("PostgreSQL connected successfully.")

    except Exception as error:
        print(f"PostgreSQL connection failed: {error}")

    finally:
        if connection:
            connection.close()
            print("PostgreSQL connection closed.")


if __name__ == "__main__":
    test_connection()