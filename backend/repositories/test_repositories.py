from backend.repositories.document_repository import (
    create_document,
    get_document
)

from backend.repositories.chunk_repository import (
    create_chunk,
    get_chunks
)

from backend.services.embedding import generate_embedding


def test_repositories():

    # 1. Create document
    document_id = create_document(
        title="Company Annual Report 2018",
        filename="annual_report_2018.pdf",
        document_type="PDF",
        author="Company",
        document_date="2018-12-31",
        topic="Business"
    )

    print("Created document:", document_id)

    # 2. Retrieve document
    document = get_document(document_id)

    print("Retrieved document:", document)

    # 3. Generate embedding
    text = "The Chennai office was established in July 2018."

    embedding = generate_embedding(text)

    print("Embedding dimensions:", len(embedding))

    # 4. Create chunk
    chunk_id = create_chunk(
        document_id=document_id,
        chunk_index=0,
        content=text,
        page_start=12,
        page_end=12,
        embedding=embedding
    )

    print("Created chunk:", chunk_id)

    # 5. Retrieve chunks
    chunks = get_chunks(document_id)

    print("Retrieved chunks:", chunks)


if __name__ == "__main__":
    test_repositories()