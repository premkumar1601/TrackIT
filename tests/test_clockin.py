# tests/test_clockin.py
import os
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

API_KEY = os.environ.get("API_KEY", "123")

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_create_clockin(client):
    response = client.post("/clockin/", json={
        "email": "test@example.com",
        "location": "Office",
        "insert_datetime": "2024-10-11"
    }, headers={"api-key": API_KEY})
    
    assert response.status_code == 200

def test_get_clockin(client):
    create_response = client.post("/clockin/", json={
        "email": "test@example.com",
        "location": "Office",
    }, headers={"api-key": API_KEY})

    clockin_id = create_response.json()["inserted_id"]

    response = client.get(f"/clockin/id/{clockin_id}", headers={"api-key": API_KEY})

    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == clockin_id

def test_group_emails(client):
    response = client.get("/clockin/emails/", headers={"api-key": API_KEY})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_filter_clockins(client):
    response = client.get("/clockin/", params={"email": "test@example.com"}, headers={"api-key": API_KEY})
    
    assert response.status_code == 200
    clockins = response.json()
    assert isinstance(clockins, list)

def test_update_clockin(client):
    create_response = client.post("/clockin/", json={
        "email": "test@example.com",
        "location": "Office",
        "insert_datetime": "2024-10-11"
    }, headers={"api-key": API_KEY})

    clockin_id = create_response.json()["inserted_id"]

    response = client.put(f"/clockin/id/{clockin_id}", json={
        "email": "test_updated@example.com",
        "location": "Home",
        "insert_datetime": "2024-10-11T10:00:00"
    }, headers={"api-key": API_KEY})

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_updated@example.com"

def test_delete_clockin(client):
    create_response = client.post("/clockin/", json={
        "email": "test@example.com",
        "location": "Office",
        "insert_datetime": "2024-10-11"
    }, headers={"api-key": API_KEY})

    clockin_id = create_response.json()["inserted_id"]

    response = client.delete(f"/clockin/id/{clockin_id}", headers={"api-key": API_KEY})

    assert response.status_code == 200
    assert response.json()["detail"] == "Clock-in entry deleted successfully"