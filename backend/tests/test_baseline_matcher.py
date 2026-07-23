from app.services.baseline_matcher import calculate_skill_match, extract_skills


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


def test_java_does_not_match_javascript() -> None:
    assert extract_skills(
        "Built frontend apps with JavaScript.",
        {"java", "javascript"},
    ) == {"javascript"}


def test_git_does_not_match_github_actions() -> None:
    assert extract_skills(
        "Automated deployments with GitHub Actions.",
        {"git", "github actions"},
    ) == {
        "github actions"
    }


def test_multi_word_skills_still_match() -> None:
    assert extract_skills("Used machine learning and REST API design.") >= {
        "machine learning",
        "rest api",
    }


def test_punctuation_around_skill_still_matches() -> None:
    assert "python" in extract_skills("Built APIs with Python, FastAPI, and Docker.")


def test_matching_remains_case_insensitive() -> None:
    assert extract_skills("Worked with FASTAPI and REACT.") == {"fastapi", "react"}


def test_skill_aliases_are_returned_as_canonical_names() -> None:
    assert extract_skills(
        "Built ML services with sklearn and RESTful APIs using GH Actions."
    ) >= {
        "github actions",
        "machine learning",
        "rest api",
        "scikit-learn",
    }
