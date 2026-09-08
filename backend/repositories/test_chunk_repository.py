from backend.repositories.chunk_repository import (
    create_chunk,
    get_chunks
)


def test_chunk_repository():

    # Use an existing document ID from your database.
    document_id = 3

    chunk_id = create_chunk(
        document_id=document_id,
        chunk_index=0,
        content="This is a test document chunk.",
        page_start=1,
        page_end=1
    )

    print("Chunk created successfully.")
    print("Chunk ID:", chunk_id)

    chunks = get_chunks(document_id)

    print("\nStored chunks:")

    for chunk in chunks:
        print(chunk)


if __name__ == "__main__":
    test_chunk_repository()