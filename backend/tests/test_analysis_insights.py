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


def test_skill_evidence_identifies_sections_and_quantified_snippets() -> None:
    from app.services.analysis_insights import build_skill_evidence

    evidence = build_skill_evidence(
        "Projects\n- Built a Python service that reduced latency by 35%.\n"
        "Skills\nPython, Docker",
        ["python"],
    )

    assert evidence == [
        {
            "skill": "python",
            "sections": ["Projects", "Skills"],
            "snippet": "Built a Python service that reduced latency by 35%.",
            "quantified": True,
        }
    ]
