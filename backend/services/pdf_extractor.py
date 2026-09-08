import os
import fitz


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from all pages of a PDF.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text from the PDF.
    """

    if not file_path:
        raise ValueError("PDF file path cannot be empty.")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    try:
        document = fitz.open(file_path)

        extracted_text = []

        for page in document:
            text = page.get_text()

            if text.strip():
                extracted_text.append(text)

        document.close()

        return "\n".join(extracted_text)

    except Exception as error:
        raise RuntimeError(
            f"Failed to extract text from PDF: {error}"
        )