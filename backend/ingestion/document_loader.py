from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "text": text
        })

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    for document in documents:
        print(f"- {document['filename']}")