from app.services.analysis_insights import build_skill_priorities


def test_required_and_repeated_skills_receive_higher_priority() -> None:
    priorities = build_skill_priorities(
        "Python is required. We use Python daily. Docker is nice to have.",
        ["python", "docker"],
    )

    assert priorities[0]["skill"] == "python"
    assert priorities[0]["priority"] == "high"
    assert priorities[0]["mentions"] == 2
    assert priorities[1]["priority"] == "low"
