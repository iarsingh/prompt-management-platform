from fastapi.testclient import TestClient
from prompts.main import app
from prompts import registry

client = TestClient(app)


def setup_function():
    registry.CHAMPION = next(iter(registry.MODELS))


def test_promote():
    client.post("/models", json={"name": "support-v2", "version": "2", "metrics": {"auc": 0.9}})
    payload = client.post("/promote", json={"name": "support-v2"}).json()
    assert payload["champion"] == "support-v2"
    assert payload["applied"] is False
    assert client.get("/champion").json()["champion"] == "support-v2"
