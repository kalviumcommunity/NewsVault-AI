from datetime import date

from backend.repositories.document_repository import (
    create_document,
    get_document
)


def test_document_metadata():

    document_id = create_document(
        title="Company Annual Report 2018",
        filename="annual_report_2018.pdf",
        document_type="PDF",
        author="Company",
        document_date=date(2018, 12, 31),
        topic="Business"
    )

    print("Created document:", document_id)

    document = get_document(document_id)

    print("Retrieved document:", document)


if __name__ == "__main__":
    test_document_metadata()