from backend.ingestion.document_loader import load_documents

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    documents = load_documents()

    total_chunks = 0

    for document in documents:
        chunks = chunk_text(document["text"])
        total_chunks += len(chunks)

        print(f"{document['filename']}: {len(chunks)} chunks")

    print(f"\nTotal chunks created: {total_chunks}")