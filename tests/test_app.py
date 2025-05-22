import pytest
from fastapi.testclient import TestClient
from serving.app import app

client = TestClient(app)

def test_initial_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "NOT_DEPLOYED"}

def test_model_deployment():
    response = client.post("/model", json={"model_id": "test-model"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["model_id"] == "test-model"

def test_model_get():
    response = client.get("/model")
    assert response.status_code == 200
    assert "model_id" in response.json()

def test_completion_while_not_running():
    # Reset state manually if needed
    from serving.app import model_state
    model_state["status"] = "NOT_DEPLOYED"
    
    response = client.post("/completion", json={
        "messages": [{"role": "user", "content": "hello"}]
    })
    assert response.status_code == 200
    assert response.json()["status"] == "error"