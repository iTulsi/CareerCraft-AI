import pytest

from app.services.evaluation import build_evaluation_comparison


def test_evaluation_marks_similar_scores_as_close() -> None:
    result = build_evaluation_comparison(
        deterministic_score=82.0,
        semantic_score=76.5,
        semantic_status="available",
    )

    assert result["status"] == "available"
    assert result["score_gap"] == 5.5
    assert result["gap_category"] == "close"
    assert "different signals" in str(result["interpretation"])


def test_evaluation_marks_large_difference_as_wide() -> None:
    result = build_evaluation_comparison(
        deterministic_score=90.0,
        semantic_score=45.0,
        semantic_status="available",
    )

    assert result["score_gap"] == 45.0
    assert result["gap_category"] == "wide"


def test_evaluation_handles_semantic_comparison_not_requested() -> None:
    result = build_evaluation_comparison(
        deterministic_score=80.0,
        semantic_score=None,
        semantic_status="not_requested",
    )

    assert result["status"] == "not_requested"
    assert result["semantic_score"] is None
    assert result["score_gap"] is None
    assert result["gap_category"] == "not_available"


def test_evaluation_requires_available_semantic_score() -> None:
    with pytest.raises(
        ValueError,
        match="semantic_score is required",
    ):
        build_evaluation_comparison(
            deterministic_score=80.0,
            semantic_score=None,
            semantic_status="available",
        )
