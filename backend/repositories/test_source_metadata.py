from backend.repositories.document_repository import get_document_metadata


def test_source_metadata():

    document_id = 3

    metadata = get_document_metadata(document_id)

    print("Source metadata:")
    print(metadata)


if __name__ == "__main__":
    test_source_metadata()