from app.services.baseline_matcher import calculate_skill_match


def test_calculate_skill_match_returns_explainable_result() -> None:
    result = calculate_skill_match(
        resume_text=(
            "Built Python and FastAPI services with React, Docker and Git."
        ),
        job_description=(
            "Seeking Python, FastAPI, React, Docker and AWS experience."
        ),
    )

    assert result["matched_skills"] == [
        "docker",
        "fastapi",
        "python",
        "react",
    ]
    assert result["missing_skills"] == ["aws"]
    assert result["match_score"] == 80.0
