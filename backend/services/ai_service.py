import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load environment variables from project root
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

# Read Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Candidate text generation models in order of priority
MODEL_CANDIDATES = [
    os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-3.6-flash"
]


def generate_response(prompt: str) -> str:
    """
    Generate a response from Gemini using the provided prompt.
    Includes multi-model fallback and exponential backoff on rate limits (429).
    """
    last_error = None

    for model_name in MODEL_CANDIDATES:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = e
                err_str = str(e)

                # If quota/rate limit error (429 RESOURCE_EXHAUSTED), retry with backoff or switch model
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    wait_sec = 1.5 * (attempt + 1)
                    time.sleep(wait_sec)
                    continue
                else:
                    # Non-quota error for this model, try next model candidate
                    break

    raise RuntimeError(
        f"Unable to generate response after attempting model fallbacks. Last error: {last_error}"
    )


def embed_query(question: str) -> list[float]:
    """
    Convert a user question into a 768-dimensional embedding
    using Gemini Embedding 2. Includes retry on transient rate limits.
    """
    last_error = None
    for attempt in range(3):
        try:
            response = client.models.embed_content(
                model="gemini-embedding-2",
                contents=question,
                config={
                    "output_dimensionality": 768
                }
            )
            return response.embeddings[0].values
        except Exception as e:
            last_error = e
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                time.sleep(1.5 * (attempt + 1))
                continue
            else:
                break

    raise RuntimeError(
        f"Failed to generate query embedding: {last_error}"
    )