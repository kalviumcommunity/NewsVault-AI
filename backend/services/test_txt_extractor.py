from backend.services.txt_extractor import extract_text_from_txt


def test_valid_txt():
    file_path = "backend/data/sample.txt"

    text = extract_text_from_txt(file_path)

    assert text
    assert "India's economy" in text

    print("Valid TXT test passed.")


def test_missing_txt():
    file_path = "data/does_not_exist.txt"

    try:
        extract_text_from_txt(file_path)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        print("Missing TXT test passed.")


if __name__ == "__main__":
    test_valid_txt()
    test_missing_txt()

    print("All TXT extraction tests passed.")