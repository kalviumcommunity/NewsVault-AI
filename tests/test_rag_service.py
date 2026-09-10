from unittest.mock import patch

from backend.services.rag_service import answer_question


# --------------------------------------------------
# Test 1: Answer is generated from retrieved sources
# --------------------------------------------------
@patch("backend.services.rag_service.generate_response")
@patch("backend.services.rag_service.retrieve_chunks")
def test_answer_question_with_results(
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

    mock_generate.return_value = (
        "India's real GDP growth rate was estimated at 7.7% [Source 1]."
    )

    result = answer_question(
        question="What is India's GDP growth rate?"
    )

    assert result["answer"] == (
        "India's real GDP growth rate was estimated at 7.7% [Source 1]."
    )

    assert len(result["sources"]) == 1

    assert result["sources"][0]["filename"] == (
        "gdp_2025_26.txt"
    )

    assert result["sources"][0]["id"] == "Source 1"


# --------------------------------------------------
# Test 2: Filters are passed to retrieval
# --------------------------------------------------
@patch("backend.services.rag_service.generate_response")
@patch("backend.services.rag_service.retrieve_chunks")
def test_answer_question_passes_filters(
    mock_retrieve,
    mock_generate
):

    mock_retrieve.return_value = [
        (
            "finance_report.txt",
            1,
            "Financial information.",
            0.88
        )
    ]

    mock_generate.return_value = (
        "Financial information [Source 1]."
    )

    answer_question(
        question="What is the financial outlook?",
        date_start=2025,
        date_end=2025,
        content_type="Reports",
        author="Ministry of Finance",
        topic="Finance",
        keywords="GDP"
    )

    mock_retrieve.assert_called_once_with(
        question="What is the financial outlook?",
        top_k=5,
        date_start=2025,
        date_end=2025,
        content_type="Reports",
        author="Ministry of Finance",
        topic="Finance",
        keywords="GDP"
    )


# --------------------------------------------------
# Test 3: Empty retrieval gives insufficient response
# --------------------------------------------------
@patch("backend.services.rag_service.generate_response")
@patch("backend.services.rag_service.retrieve_chunks")
def test_answer_question_without_results(
    mock_retrieve,
    mock_generate
):

    mock_retrieve.return_value = []

    result = answer_question(
        question="What is the population of Brazil?"
    )

    assert (
        "does not contain sufficient information"
        in result["answer"]
    )

    assert result["sources"] == []

    # Gemini should not be called when there is no evidence
    mock_generate.assert_not_called()


# --------------------------------------------------
# Test 4: Multiple sources are associated correctly
# --------------------------------------------------
@patch("backend.services.rag_service.generate_response")
@patch("backend.services.rag_service.retrieve_chunks")
def test_answer_question_with_multiple_sources(
    mock_retrieve,
    mock_generate
):

    mock_retrieve.return_value = [
        (
            "source_one.txt",
            0,
            "First source information.",
            0.91
        ),
        (
            "source_two.txt",
            2,
            "Second source information.",
            0.87
        )
    ]

    mock_generate.return_value = (
        "Combined answer [Source 1] [Source 2]."
    )

    result = answer_question(
        question="What does the archive report?"
    )

    assert len(result["sources"]) == 2

    assert result["sources"][0]["id"] == "Source 1"
    assert result["sources"][0]["filename"] == "source_one.txt"

    assert result["sources"][1]["id"] == "Source 2"
    assert result["sources"][1]["filename"] == "source_two.txt"

    assert "[Source 1]" in result["answer"]
    assert "[Source 2]" in result["answer"]