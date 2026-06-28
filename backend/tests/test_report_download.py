import json

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

ANALYSIS_PAYLOAD = {
    "assessment": {
        "overall_score": 81,
        "skill_score": 75,
        "structure_score": 90,
        "found_sections": ["Skills", "Projects"],
        "missing_sections": ["Experience"],
        "recommendations": ["Add measurable project outcomes."],
    },
    "result": {
        "matched_skills": ["Python", "FastAPI"],
        "missing_skills": ["AWS"],
    },
    "semantic": {
        "status": "available",
        "score": 84,
        "note": "Semantic matching completed.",
    },
    "interview_questions": [
        {
            "category": "technical",
            "question": "How did you structure the FastAPI service?",
            "answer_outline": "Explain routing, validation, and testing.",
        }
    ],
    "methodology": "Combined skill, structure, and semantic matching.",
}


def test_report_download_returns_text_attachment() -> None:
    response = client.post(
        "/api/report",
        data={"payload": json.dumps(ANALYSIS_PAYLOAD)},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    assert "attachment; filename=" in response.headers[
        "content-disposition"
    ]
    assert "CareerCraft AI Analysis Report" in response.text
    assert "Python" in response.text
    assert "How did you structure the FastAPI service?" in response.text


def test_report_download_rejects_invalid_json() -> None:
    response = client.post(
        "/api/report",
        data={"payload": "{invalid-json"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "The report payload is not valid JSON."
    )


def test_report_download_requires_assessment_data() -> None:
    response = client.post(
        "/api/report",
        data={"payload": json.dumps({"result": {}})},
    )

    assert response.status_code == 422
    assert response.json()["detail"] == (
        "The report payload is missing assessment data."
    )
