from app.services.analysis_service import calculate_resume_assessment


def test_assessment_combines_skill_and_structure_scores() -> None:
    skill_match, assessment = calculate_resume_assessment(
        resume_text=(
            "Skills\nPython and Docker\n"
            "Projects\nBuilt a deployment tool.\n"
            "Education\nB.Tech Computer Science."
        ),
        job_description=(
            "Seeking Python, Docker, FastAPI and AWS for backend services."
        ),
    )

    assert skill_match["match_score"] == 50.0
    assert assessment["structure_score"] == 75.0
    assert assessment["overall_score"] == 56.25
    assert assessment["missing_sections"] == ["Experience"]


def test_recommendations_do_not_encourage_false_claims() -> None:
    _, assessment = calculate_resume_assessment(
        resume_text="Skills\nPython\nProjects\nBuilt a Python API.",
        job_description="Seeking Python, Docker and AWS engineering experience.",
    )

    recommendations = assessment["recommendations"]

    assert any("only where truthful" in item for item in recommendations)
    assert any("Experience section" in item for item in recommendations)
    assert any("Education section" in item for item in recommendations)
