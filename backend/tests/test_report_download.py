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
    "skill_priorities": [
        {
            "skill": "AWS",
            "mentions": 2,
            "priority": "high",
            "reason": "Required for deployment.",
        }
    ],
    "skill_evidence": [
        {
            "skill": "Python",
            "sections": ["Projects"],
            "snippet": "Built a Python API used by 500 users.",
            "quantified": True,
        }
    ],
    "resume_quality": {
        "word_count": 420,
        "bullet_count": 12,
        "action_oriented_statements": 9,
        "quantified_statements": 6,
        "quantified_statement_ratio": 50,
        "suggestions": ["Quantify one more project outcome."],
    },
    "job_requirements": {
        "experience_requirements": ["2 years"],
        "seniority_signals": ["Junior"],
        "education_requirements": ["Bachelor's degree"],
        "work_arrangements": ["Remote"],
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
    assert "Job skill priorities" in response.text
    assert "Built a Python API used by 500 users." in response.text
    assert "Resume writing diagnostics" in response.text
    assert "Explicit job requirements" in response.text


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
