from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_openapi_schema_documents_public_endpoints() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    assert schema["info"]["title"] == "CareerCraft AI API"
    assert schema["info"]["version"] == "0.3.0"

    expected_paths = {
        "/api/health",
        "/api/resume/parse",
        "/api/analyze",
        "/api/report",
    }
    assert expected_paths.issubset(schema["paths"])
