from backend.services.docx_extractor import extract_text_from_docx


def test_valid_docx():
    file_path = "backend/data/sample.docx"

    text = extract_text_from_docx(file_path)

    assert text
    assert "India's economy" in text

    print("Valid DOCX test passed.")


def test_missing_docx():
    file_path = "backend/data/does_not_exist.docx"

    try:
        extract_text_from_docx(file_path)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        print("Missing DOCX test passed.")


if __name__ == "__main__":
    test_valid_docx()
    test_missing_docx()

    print("All DOCX extraction tests passed.")