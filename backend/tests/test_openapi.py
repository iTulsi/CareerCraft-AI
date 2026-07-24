from fastapi.testclient import TestClient

from app.config import MAX_ANALYSIS_TEXT_CHARACTERS
from app.main import app


client = TestClient(app)


def test_openapi_schema_documents_public_endpoints() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    assert schema["info"]["title"] == "CareerCraft AI API"
    assert schema["info"]["version"] == "0.4.0"

    expected_paths = {
        "/api/health",
        "/api/resume/parse",
        "/api/analyze",
        "/api/report",
    }
    assert expected_paths.issubset(schema["paths"])

def test_openapi_documents_analysis_text_limits() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    properties = response.json()["components"]["schemas"]["AnalyzeRequest"][
        "properties"
    ]

    assert properties["resume_text"]["maxLength"] == MAX_ANALYSIS_TEXT_CHARACTERS
    assert (
        properties["job_description"]["maxLength"]
        == MAX_ANALYSIS_TEXT_CHARACTERS
    )
    assert properties["resume_text"]["description"]
    assert properties["job_description"]["description"]

