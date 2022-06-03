import pytest
from starlette.testclient import TestClient
from app import app


FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_predict_request(client):
    response = client.post("predict", json=dict(list(zip(FEATURES, list(range(len(FEATURES)))))))
    assert 200 == response.status_code
    assert len(response.json()) >= 0


def test_health_request(client):
    response = client.get("health")
    assert 200 == response.status_code
