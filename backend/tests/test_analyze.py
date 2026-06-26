from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_endpoint_returns_skill_match() -> None:
    response = client.post(
        "/api/analyze",
        json={
            "resume_text": (
                "Built Python and FastAPI services with React, Docker and Git."
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
