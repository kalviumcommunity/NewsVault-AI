from unittest.mock import patch

from backend.services.rag_service import answer_question


@patch("backend.services.rag_service.generate_response")
@patch("backend.services.rag_service.retrieve_chunks")
def test_complete_rag_workflow(
    mock_retrieve,
    mock_generate
):
    # Step 1: Retrieval
    mock_retrieve.return_value = [
        (
            "gdp_2025_26.txt",
            0,
            "India's real GDP growth rate was estimated at 7.7%.",
            0.92
        ),
        (
            "economic_survey_services_2025_26.txt",
            2,
            "The services sector continued to support economic growth.",
            0.87
        )
    ]

    # Step 2: Gemini generates grounded answer
    mock_generate.return_value = (
        "India's real GDP growth rate was estimated at 7.7% "
        "[Source 1]. The services sector supported economic growth "
        "[Source 2]."
    )

    # Step 3: Complete RAG flow
    result = answer_question(
        question="What is India's GDP growth rate?"
    )

    # Step 4: Verify retrieval happened
    mock_retrieve.assert_called_once()

    # Step 5: Verify Gemini was called with retrieved context
    mock_generate.assert_called_once()

    prompt = mock_generate.call_args[0][0]

    assert "gdp_2025_26.txt" in prompt
    assert "India's real GDP growth rate was estimated at 7.7%" in prompt
    assert "Source 1" in prompt
    assert "Source 2" in prompt

    # Step 6: Verify final answer
    assert "7.7%" in result["answer"]

    # Step 7: Verify sources are returned
    assert len(result["sources"]) == 2

    assert result["sources"][0]["id"] == "Source 1"
    assert result["sources"][0]["filename"] == "gdp_2025_26.txt"

    assert result["sources"][1]["id"] == "Source 2"
    assert (
        result["sources"][1]["filename"]
        == "economic_survey_services_2025_26.txt"
    )

    # Step 8: Verify source citations
    assert "[Source 1]" in result["answer"]
    assert "[Source 2]" in result["answer"]