import pytest
from fastapi.testclient import TestClient
from app.auth import routers
from app.main import app

client = TestClient(app)
data = {"login": "test", "password": "test"}

def test_registration(monkeypatch: pytest.MonkeyPatch):
    response = client.post("/register", json=data)
    assert response.status_code == 200
    assert response.content == b"null"

def test_double_registration(monkeypatch: pytest.MonkeyPatch):
    response = client.post("/register", json=data)
    print(routers.database)
    monkeypatch.setattr(routers, "database", None)
    print(routers.database)
    response = client.post("/register", json=data)
    assert response.status_code == 409

def test_correct_unregistration():
    response = client.post("/register", json=data)
    response = client.post("/unregister", params={"user_login": "test"})
    assert response.status_code == 200

def test_unregistration():
    response = client.post("/unregister", params={"user_login": "123"})
    assert response.status_code == 404
