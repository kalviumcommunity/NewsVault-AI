from backend.services.chunker import chunk_text


def test_chunk_text():
    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=200
    )

    print("Chunking successful.")
    print("Number of chunks:", len(chunks))

    for index, chunk in enumerate(chunks):
        print(f"Chunk {index}: {len(chunk)} characters")


if __name__ == "__main__":
    test_chunk_text()