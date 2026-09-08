from pathlib import Path
from docx import Document


def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX file.

    Args:
        file_path: Path to the DOCX file.

    Returns:
        Extracted text as a string.

    Raises:
        ValueError: If the file path is empty or invalid.
        FileNotFoundError: If the file does not exist.
        RuntimeError: If the DOCX file cannot be read.
    """

    if not file_path:
        raise ValueError("File path cannot be empty.")

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"DOCX file not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    try:
        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)

    except Exception as error:
        raise RuntimeError(
            f"Failed to extract text from DOCX: {file_path}"
        ) from error