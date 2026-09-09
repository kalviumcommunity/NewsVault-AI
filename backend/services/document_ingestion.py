import os

from backend.services.pdf_extractor import extract_text_from_pdf
from backend.services.chunker import chunk_text
from backend.services.embedding import generate_embedding

from backend.repositories.document_repository import create_document
from backend.repositories.chunk_repository import create_chunk


def ingest_document(
    file_path: str,
    title: str,
    filename: str,
    document_type: str = "pdf",
    author=None,
    document_date=None,
    topic=None
):
    """
    Complete document ingestion pipeline.

    Flow:

    File
        ↓
    Document Record
        ↓
    Text Extraction
        ↓
    Chunking
        ↓
    Embedding
        ↓
    PostgreSQL
    """

    # --------------------------------------------------
    # 1. Validate file
    # --------------------------------------------------

    if not file_path:
        raise ValueError("File path cannot be empty.")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    # --------------------------------------------------
    # 2. Create document record
    # --------------------------------------------------

    document_id = create_document(
        title=title,
        filename=filename,
        document_type=document_type,
        author=author,
        document_date=document_date,
        topic=topic
    )

    # --------------------------------------------------
    # 3. Extract text
    # --------------------------------------------------

    if document_type.lower() == "pdf":

        text = extract_text_from_pdf(file_path)

    else:
        raise ValueError(
            f"Unsupported document type: {document_type}"
        )

    # --------------------------------------------------
    # 4. Validate extracted text
    # --------------------------------------------------

    if not text or not text.strip():
        raise ValueError(
            "No text could be extracted from the document."
        )

    # --------------------------------------------------
    # 5. Split text into chunks
    # --------------------------------------------------

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=200
    )

    # --------------------------------------------------
    # 6. Generate embeddings and store chunks
    # --------------------------------------------------

    stored_chunk_ids = []

    for index, chunk in enumerate(chunks):

        # Generate embedding
        embedding = generate_embedding(chunk)

        # Store chunk and embedding
        chunk_id = create_chunk(
            document_id=document_id,
            chunk_index=index,
            content=chunk,
            embedding=embedding
        )

        stored_chunk_ids.append(chunk_id)

    # --------------------------------------------------
    # 7. Return ingestion result
    # --------------------------------------------------

    return {
        "document_id": document_id,
        "chunk_count": len(stored_chunk_ids),
        "chunk_ids": stored_chunk_ids
    }