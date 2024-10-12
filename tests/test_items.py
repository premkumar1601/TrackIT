
import os
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

from dotenv import load_dotenv
load_dotenv(dotenv_path="app.env")
API_KEY = os.environ.get("API_KEY")

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_create_item(client):
    response = client.post("/items/", json={
        "name": "fooo",
        "email": "fooo@example.com",
        "expiry_date": "2024-12-31T00:00:00",  
        "item_name": "item1",
        "quantity": 10
    }, headers={'api-key' : API_KEY})  
    
    assert response.status_code in {200, 201}, f"Unexpected status code: {response.status_code}"
    assert 'inserted_id' in response.json()  


def test_get_item(client):
    
    create_response = client.post("/items/", json={
        "email": "foo1@example.com",
        "expiry_date": "2024-12-31",
        "name": "foo1",
        "item_name" : "item1",
        "quantity": 100
    }, headers={"api-key": API_KEY})

    item_id = create_response.json()["inserted_id"]

    response = client.get(f"/items/id/{item_id}", headers={"api-key": API_KEY})

    assert response.status_code == 200

def test_filter_items(client):
    response = client.get("/items/", params={"email": "foo@example.com"}, headers={"api-key": API_KEY})
    items = response.json()
    print(items)
    
    assert response.status_code == 200
    assert isinstance(items, list)

def test_update_item(client):
    
    create_response = client.post("/items/", json={
        "email": "foo2@example.com",
        "expiry_date": "2024-12-31",
        "name": "foo2",
        "item_name" : "item3",
        "quantity": 99
    }, headers={"api-key": API_KEY})

    item_id = create_response.json()["inserted_id"]

    
    response = client.put(f"/items/id/{item_id}", json={
        "email": "test_updated@example.com",
        "expiry_date": "2025-01-01",
        "quantity": 20
    }, headers={"api-key": API_KEY})

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_updated@example.com"

def test_delete_item(client):
    create_response = client.post("/items/", json={
        "email": "foo@example.com",
        "expiry_date": "2024-12-31",
        "name": "ahvhv",
        "item_name" : "dgdgd",
        "quantity": 10
    }, headers={"api-key": API_KEY})

    item_id = create_response.json()["inserted_id"]

    
    response = client.delete(f"/items/id/{item_id}", headers={"api-key": API_KEY})

    assert response.status_code == 200
    assert response.json()["detail"] == "Item deleted successfully"

def test_group_emails(client):
    response = client.get("/items/emails/", headers={"api-key": API_KEY})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)