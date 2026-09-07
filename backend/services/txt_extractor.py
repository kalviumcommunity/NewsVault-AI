from pathlib import Path


def extract_text_from_txt(file_path):
    """
    Extract text from a TXT file.

    Args:
        file_path: Path to the TXT file.

    Returns:
        Extracted text as a string.

    Raises:
        ValueError: If the file path is empty or invalid.
        FileNotFoundError: If the file does not exist.
        RuntimeError: If the TXT file cannot be read.
    """

    if not file_path:
        raise ValueError("File path cannot be empty.")

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"TXT file not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    try:
        return path.read_text(encoding="utf-8")

    except UnicodeDecodeError as error:
        raise RuntimeError(
            f"TXT file is not encoded as UTF-8: {file_path}"
        ) from error

    except Exception as error:
        raise RuntimeError(
            f"Failed to extract text from TXT: {file_path}"
        ) from error