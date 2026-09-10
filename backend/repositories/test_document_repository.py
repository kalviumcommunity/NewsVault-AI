from backend.repositories.document_repository import filter_documents


def test_filter_by_author():
    results = filter_documents(author="Test Author")

    print("\nAuthor filter:")
    print("Results:", results)


def test_filter_by_topic():
    results = filter_documents(topic="India")

    print("\nTopic filter:")
    print("Results:", results)


def test_filter_by_type():
    results = filter_documents(document_type="pdf")

    print("\nType filter:")
    print("Results:", results)


def test_filter_by_date():
    results = filter_documents(
        document_date="2018-12-31"
    )

    print("\nDate filter:")
    print("Results:", results)


def test_filter_by_multiple_metadata():
    results = filter_documents(
        author="Test Author",
        topic="India",
        document_type="pdf"
    )

    print("\nMultiple metadata filters:")
    print("Results:", results)


def test_filter_by_date_range():
    results = filter_documents(
        date_from="2020-01-01",
        date_to="2030-12-31"
    )

    print("\nDate range filter:")
    print("Results:", results)

results = filter_documents(
    author="This Author Does Not Exist"
)


if __name__ == "__main__":
    test_filter_by_author()
    test_filter_by_topic()
    test_filter_by_type()
    test_filter_by_date()
    test_filter_by_multiple_metadata()
    test_filter_by_date_range()