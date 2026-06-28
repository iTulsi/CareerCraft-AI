from fastapi.testclient import TestClient

import app.main as main_module
from app.main import app


client = TestClient(app)


def test_analyze_endpoint_returns_explainable_assessment() -> None:
    response = client.post(
        "/api/analyze",
        json={
            "resume_text": (
                "Skills\nPython, FastAPI, React, Docker\n"
                "Experience\nBuilt reliable Python services.\n"
                "Projects\nCreated a React analytics dashboard.\n"
                "Education\nB.Tech in Computer Science."
            ),
            "job_description": (
                "Seeking Python, FastAPI, React, Docker and AWS experience."
            ),
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["matched_skills"] == [
        "docker",
        "fastapi",
        "python",
        "react",
    ]
    assert payload["result"]["missing_skills"] == ["aws"]
    assert payload["result"]["match_score"] == 80.0
    assert payload["assessment"]["skill_score"] == 80.0
    assert payload["assessment"]["structure_score"] == 100.0
    assert payload["assessment"]["overall_score"] == 85.0
    assert payload["assessment"]["found_sections"] == [
        "Skills",
        "Experience",
        "Projects",
        "Education",
    ]
    assert payload["assessment"]["missing_sections"] == []
    assert payload["semantic"]["status"] == "not_requested"
    assert payload["semantic"]["score"] is None

    questions = payload["interview_questions"]
    assert any(item["category"] == "technical" for item in questions)
    assert any(item["category"] == "learning_gap" for item in questions)
    assert any(item["category"] == "behavioral" for item in questions)
    assert all(item["question"] for item in questions)
    assert all(item["answer_outline"] for item in questions)

    assert "not an employer ATS score" in payload["methodology"]


def test_analyze_returns_semantic_similarity_when_requested(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        main_module,
        "calculate_semantic_similarity",
        lambda **_: 78.25,
    )

    response = client.post(
        "/api/analyze",
        json={
            "resume_text": (
                "Skills\nPython and FastAPI\n"
                "Projects\nBuilt a production API service."
            ),
            "job_description": (
                "Seeking an engineer to build Python API systems with FastAPI."
            ),
            "include_semantic": True,
        },
    )

    assert response.status_code == 200
    semantic = response.json()["semantic"]
    assert semantic["status"] == "available"
    assert semantic["score"] == 78.25
    assert "not a hiring probability" in semantic["note"]


def test_analyze_rejects_short_resume() -> None:
    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "Too short.",
            "job_description": (
                "Seeking Python, FastAPI, React, Docker and AWS experience."
            ),
        },
    )

    assert response.status_code == 422


def test_analyze_rejects_short_job_description() -> None:
    response = client.post(
        "/api/analyze",
        json={
            "resume_text": (
                "Built Python and FastAPI services with React, Docker and Git."
            ),
            "job_description": "Too short.",
        },
    )

    assert response.status_code == 422
