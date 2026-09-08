from backend.services.document_pipeline import process_document


def test_document_pipeline():

    file_path = "backend/data/sampledata1.pdf"

    document_id = 3

    chunk_ids = process_document(
        file_path=file_path,
        document_id=document_id
    )

    print("Document pipeline completed successfully.")
    print("Number of chunks stored:", len(chunk_ids))
    print("Chunk IDs:", chunk_ids)


if __name__ == "__main__":
    test_document_pipeline()