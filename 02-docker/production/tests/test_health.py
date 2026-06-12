"""CI smoke tests — chạy trước mỗi deploy Railway."""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready_returns_200(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["ready"] is True


def test_ask_requires_question(client):
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_ask_with_question(client):
    response = client.post("/ask", json={"question": "Hello Railway"})
    assert response.status_code == 200
    assert "answer" in response.json()
