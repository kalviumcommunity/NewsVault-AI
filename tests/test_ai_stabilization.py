from unittest.mock import patch

import pytest

from backend.services.rag_service import (
    INSUFFICIENT_CONTEXT_MESSAGE,
    answer_question,
    build_prompt,
)


# --------------------------------------------------
# Test 1: Empty question is handled safely
# --------------------------------------------------
def test_empty_question():

    result = answer_question("")

    assert result["answer"] == (
        "Please enter a question to search the archive."
    )

    assert result["sources"] == []
    assert result["insufficient_context"] is True


# --------------------------------------------------
# Test 2: Prompt contains evidence-grounding rules
# --------------------------------------------------
def test_prompt_contains_stabilization_rules():

    prompt = build_prompt(
        question="What is India's GDP growth?",
        context=(
            "[Source 1]\n"
            "Filename: gdp_2025_26.txt\n"
            "Chunk: 0\n"
            "Content:\n"
            "India's real GDP growth rate was estimated at 7.7%."
        )
    )

    assert "ONLY the retrieved archive evidence" in prompt
    assert "Do not use outside knowledge" in prompt
    assert "Do not invent, assume, estimate, predict" in prompt
    assert "Every factual statement must be supported" in prompt
    assert "[Source X]" in prompt
    assert "Do not repeat the same fact" in prompt


# --------------------------------------------------
# Test 3: Gemini failure is handled safely
# --------------------------------------------------
@patch("backend.services.rag_service.generate_response")
@patch("backend.services.rag_service.retrieve_chunks")
def test_gemini_failure(
    mock_retrieve,
    mock_generate
):

    mock_retrieve.return_value = [
        (
            "gdp_2025_26.txt",
            0,
            "India's real GDP growth rate was estimated at 7.7%.",
            0.92
        )
    ]

    mock_generate.side_effect = RuntimeError(
        "Gemini service unavailable"
    )

    result = answer_question(
        question="What is India's GDP growth?"
    )

    assert (
        "AI service could not generate an answer"
        in result["answer"]
    )

    assert len(result["sources"]) == 1
    assert result["sources"][0]["filename"] == (
        "gdp_2025_26.txt"
    )


# --------------------------------------------------
# Test 4: Empty Gemini response is handled safely
# --------------------------------------------------
@patch("backend.services.rag_service.generate_response")
@patch("backend.services.rag_service.retrieve_chunks")
def test_empty_gemini_response(
    mock_retrieve,
    mock_generate
):

    mock_retrieve.return_value = [
        (
            "gdp_2025_26.txt",
            0,
            "India's real GDP growth rate was estimated at 7.7%.",
            0.92
        )
    ]

    mock_generate.return_value = ""

    result = answer_question(
        question="What is India's GDP growth?"
    )

    assert (
        "AI service returned an empty response"
        in result["answer"]
    )

    assert len(result["sources"]) == 1


# --------------------------------------------------
# Test 5: Context is limited correctly
# --------------------------------------------------
@patch("backend.services.rag_service.generate_response")
@patch("backend.services.rag_service.retrieve_chunks")
def test_context_limit(
    mock_retrieve,
    mock_generate
):

    large_content = "A" * 6000

    mock_retrieve.return_value = [
        (
            "source_one.txt",
            0,
            large_content,
            0.95
        ),
        (
            "source_two.txt",
            1,
            large_content,
            0.90
        ),
        (
            "source_three.txt",
            2,
            large_content,
            0.85
        )
    ]

    mock_generate.return_value = (
        "Answer based on the retrieved evidence [Source 1]."
    )

    result = answer_question(
        question="What does the archive report?"
    )

    # The 12,000 character context limit should prevent
    # all three large chunks from being included.
    assert len(result["sources"]) < 3

    assert result["answer"] == (
        "Answer based on the retrieved evidence [Source 1]."
    )


# --------------------------------------------------
# Test 6: Insufficient retrieval never calls Gemini
# --------------------------------------------------
@patch("backend.services.rag_service.generate_response")
@patch("backend.services.rag_service.retrieve_chunks")
def test_insufficient_retrieval_does_not_call_gemini(
    mock_retrieve,
    mock_generate
):

    mock_retrieve.return_value = []

    result = answer_question(
        question="What information is unavailable?"
    )

    assert result["answer"] == INSUFFICIENT_CONTEXT_MESSAGE
    assert result["sources"] == []
    assert result["insufficient_context"] is True

    mock_generate.assert_not_called()