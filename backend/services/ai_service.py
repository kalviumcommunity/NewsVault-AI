import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# Gemini configuration
# --------------------------------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

EMBEDDING_MODEL = "gemini-embedding-2"

MAX_RETRIES = 3
EMBEDDING_DIMENSION = 768


# --------------------------------------------------
# Gemini client
# --------------------------------------------------

client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# Helper: identify rate-limit errors
# --------------------------------------------------

def is_rate_limit_error(error: Exception) -> bool:
    error_message = str(error).upper()

    return (
        "429" in error_message
        or "RESOURCE_EXHAUSTED" in error_message
        or "RATE LIMIT" in error_message
    )


# --------------------------------------------------
# Helper: retry delay
# --------------------------------------------------

def get_retry_delay(attempt: int) -> float:
    """
    Exponential backoff:
    attempt 0 -> 1.5 seconds
    attempt 1 -> 3 seconds
    attempt 2 -> 6 seconds
    """
    return 1.5 * (2 ** attempt)


# --------------------------------------------------
# Generate Gemini response
# --------------------------------------------------

def generate_response(prompt: str) -> str:
    """
    Generate an AI response using Gemini.

    Retries only when Gemini returns a rate-limit/quota error.
    Other errors are raised immediately.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            if response and response.text:
                answer = response.text.strip()

                if answer:
                    return answer

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        except Exception as error:
            last_error = error

            if not is_rate_limit_error(error):
                raise RuntimeError(
                    f"Gemini answer generation failed: {error}"
                ) from error

            if attempt < MAX_RETRIES - 1:
                time.sleep(get_retry_delay(attempt))

    raise RuntimeError(
        f"Gemini answer generation failed after "
        f"{MAX_RETRIES} attempts: {last_error}"
    )


# --------------------------------------------------
# Generate query embedding
# --------------------------------------------------

def embed_query(question: str) -> list[float]:
    """
    Convert a user question into a 768-dimensional
    Gemini embedding.

    Retries only on rate-limit/quota errors.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty")

    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=question,
                config={
                    "output_dimensionality": EMBEDDING_DIMENSION
                }
            )

            if (
                response
                and response.embeddings
                and response.embeddings[0].values
            ):
                embedding = response.embeddings[0].values

                if len(embedding) != EMBEDDING_DIMENSION:
                    raise RuntimeError(
                        f"Expected {EMBEDDING_DIMENSION}-dimensional "
                        f"embedding, got {len(embedding)} dimensions."
                    )

                return embedding

            raise RuntimeError(
                "Gemini returned an empty embedding."
            )

        except Exception as error:
            last_error = error

            if not is_rate_limit_error(error):
                raise RuntimeError(
                    f"Query embedding generation failed: {error}"
                ) from error

            if attempt < MAX_RETRIES - 1:
                time.sleep(get_retry_delay(attempt))

    raise RuntimeError(
        f"Query embedding generation failed after "
        f"{MAX_RETRIES} attempts: {last_error}"
    )