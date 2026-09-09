from backend.services.document_ingestion import ingest_document


def test_document_ingestion():

    file_path = "backend/data/uploads/sample.pdf"

    result = ingest_document(
        file_path=file_path,
        title="Sample News Article",
        filename="sample.pdf",
        document_type="pdf",
        author="Test Author",
        topic="India"
    )

    print("\nDocument ingestion successful.")

    print(
        "Document ID:",
        result["document_id"]
    )

    print(
        "Chunks stored:",
        result["chunk_count"]
    )

    print(
        "Chunk IDs:",
        result["chunk_ids"]
    )


if __name__ == "__main__":
    test_document_ingestion()