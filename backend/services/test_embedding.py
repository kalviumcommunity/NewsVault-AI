from backend.services.embedding import generate_embedding


def test_embedding_generation():
    text = "The Chennai office was established in July 2018."

    embedding = generate_embedding(text)

    print("Embedding generated successfully.")
    print("Embedding type:", type(embedding))
    print("Embedding dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])


if __name__ == "__main__":
    test_embedding_generation()