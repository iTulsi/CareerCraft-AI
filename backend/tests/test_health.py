from fastapi.testclient import TestClient

from app.config import API_TITLE, API_VERSION, SERVICE_NAME
from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["content-type"].startswith("application/json")
    assert response.json()["service"] == "careercraft-ai"
    assert response.json()["version"] == "0.4.0"

def test_health_and_openapi_metadata_stay_aligned() -> None:
    health = client.get("/api/health")
    schema = client.get("/openapi.json")

    assert health.status_code == 200
    assert schema.status_code == 200
    assert health.json()["service"] == SERVICE_NAME
    assert health.json()["version"] == API_VERSION
    assert schema.json()["info"]["title"] == API_TITLE
    assert schema.json()["info"]["version"] == API_VERSION

def test_health_response_includes_security_headers() -> None:
    response = client.get("/api/health")

    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["permissions-policy"] == (
        "camera=(), microphone=(), geolocation=()"
    )
