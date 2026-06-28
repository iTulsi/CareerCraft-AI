from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page_is_served() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "CareerCraft AI" in response.text
    assert 'src="/static/app.js' in response.text


def test_frontend_static_assets_are_served() -> None:
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "analyzeResume" in response.text
