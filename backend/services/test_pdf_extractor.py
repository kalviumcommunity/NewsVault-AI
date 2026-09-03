from backend.services.pdf_extractor import extract_text_from_pdf


def test_pdf_text_extraction():
    """Test extraction from a valid PDF file."""

    pdf_path = "backend/data/sampledata1.pdf"

    try:
        text = extract_text_from_pdf(pdf_path)

        if text.strip():
            print("=== PDF TEXT EXTRACTION TEST PASSED ===")
            print(text)
        else:
            print("=== PDF TEXT EXTRACTION TEST FAILED ===")
            print("No text was extracted from the PDF.")

    except Exception as error:
        print("=== PDF TEXT EXTRACTION TEST FAILED ===")
        print(error)


def test_missing_pdf():
    """Test FileNotFoundError for a non-existent PDF."""

    pdf_path = "backend/data/sampledta1.pdf"

    try:
        extract_text_from_pdf(pdf_path)

        print("=== MISSING FILE TEST FAILED ===")
        print("Expected FileNotFoundError, but no error was raised.")

    except FileNotFoundError as error:
        print("=== MISSING FILE TEST PASSED ===")
        print(error)

    except Exception as error:
        print("=== MISSING FILE TEST FAILED ===")
        print(f"Unexpected error: {error}")


def test_empty_path():
    """Test ValueError for an empty PDF path."""

    try:
        extract_text_from_pdf("")

        print("=== EMPTY PATH TEST FAILED ===")
        print("Expected ValueError, but no error was raised.")

    except ValueError as error:
        print("=== EMPTY PATH TEST PASSED ===")
        print(error)

    except Exception as error:
        print("=== EMPTY PATH TEST FAILED ===")
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    test_pdf_text_extraction()
    print()
    test_missing_pdf()
    print()
    test_empty_path()