from backend.services.pdf_extractor import extract_text_from_pdf
from backend.services.chunker import chunk_text
from backend.repositories.chunk_repository import create_chunk


def process_document(
    file_path: str,
    document_id: int,
    chunk_size: int = 1000,
    overlap: int = 200
):
    """
    Extract text from a document, split it into chunks,
    and store the chunks in PostgreSQL.
    """

    # Step 1: Extract text
    text = extract_text_from_pdf(file_path)

    if not text.strip():
        raise ValueError("No text could be extracted from the document.")

    # Step 2: Create chunks
    chunks = chunk_text(
        text,
        chunk_size=chunk_size,
        overlap=overlap
    )

    # Step 3: Store chunks
    stored_chunk_ids = []

    for index, chunk in enumerate(chunks):

        chunk_id = create_chunk(
            document_id=document_id,
            chunk_index=index,
            content=chunk
        )

        stored_chunk_ids.append(chunk_id)

    return stored_chunk_ids