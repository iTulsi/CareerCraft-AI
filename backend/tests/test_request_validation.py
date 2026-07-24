from fastapi.testclient import TestClient

from app.config import MAX_ANALYSIS_TEXT_CHARACTERS
from app.main import app


client = TestClient(app)
VALID_TEXT = (
    "Python FastAPI PostgreSQL testing deployment collaboration experience. "
)


def test_analyze_rejects_oversized_resume_text() -> None:
    response = client.post(
        "/api/analyze",
        json={
            "resume_text": "x" * (MAX_ANALYSIS_TEXT_CHARACTERS + 1),
            "job_description": VALID_TEXT,
        },
    )

    assert response.status_code == 422
    assert any(
        error["loc"][-1] == "resume_text"
        and error["type"] == "string_too_long"
        for error in response.json()["detail"]
    )

def test_analyze_rejects_oversized_job_description() -> None:
    response = client.post(
        "/api/analyze",
        json={
            "resume_text": VALID_TEXT,
            "job_description": "x" * (MAX_ANALYSIS_TEXT_CHARACTERS + 1),
        },
    )

    assert response.status_code == 422
    assert any(
        error["loc"][-1] == "job_description"
        and error["type"] == "string_too_long"
        for error in response.json()["detail"]
    )
