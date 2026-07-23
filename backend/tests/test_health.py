from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["content-type"].startswith("application/json")
    assert response.json()["service"] == "careercraft-ai"
    assert response.json()["version"] == "0.4.0"
    assert response.json()["version"] == "0.4.0"
    assert response.headers["content-type"].startswith("application/json")
