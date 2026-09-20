"""API-тесты без сети: TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_plan(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/plan", json={"topic": "morning coffee", "posts": 3, "tone": "friendly"}
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert len(payload["posts"]) == 3
    assert payload["posts"][0]["hashtags"] == ["#morning", "#coffee", "#dailybrew"]


def test_plan_rejects_too_many(client: TestClient) -> None:
    resp = client.post("/api/v1/plan", json={"topic": "tea", "posts": 99})
    assert resp.status_code == 422


@pytest.mark.integration()
def test_plan_single_shape(client: TestClient) -> None:
    """Интеграционный по маркеру: один пост, без сети."""
    resp = client.post("/api/v1/plan", json={"topic": "tea", "posts": 1})
    assert resp.status_code == 200
    assert resp.json()["posts"][0]["pillar"] == "education"
