import pytest
from app import app
import json

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_successful_audit(client):
    payload = {
        "user": "alice",
        "app": "survey_app",
        "action": "create",
        "entry": "record_123",
        "result": "200"
    }
    response = client.post("/audit", 
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 200
    assert response.get_json()["status"] == "logged"

def test_missing_fields(client):
    payload = {
        "user": "alice",
        "app": "survey_app"
    }
    response = client.post("/audit", 
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_invalid_json(client):
    # Send invalid JSON to trigger exception
    response = client.post("/audit", 
                           data="not-json",
                           content_type="application/json")
    assert response.status_code == 500
    assert "error" in response.get_json()
