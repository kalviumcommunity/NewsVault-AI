from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables from project root
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

# Read Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)


def generate_response(prompt: str) -> str:
    """
    Generate a response from Gemini using the provided prompt.
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


def embed_query(question: str) -> list[float]:
    """
    Convert a user question into a 768-dimensional embedding
    using Gemini Embedding 2.
    """
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=question,
        config={
            "output_dimensionality": 768
        }
    )

    return response.embeddings[0].values