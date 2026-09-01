import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def generate_embedding(text: str) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    try:
        response = client.embeddings.create(
            model="gemini-embedding-2",
            input=text,
            dimensions=768
        )

        return response.data[0].embedding

    except Exception as error:
        raise RuntimeError(
            f"Failed to generate embedding: {error}"
        )