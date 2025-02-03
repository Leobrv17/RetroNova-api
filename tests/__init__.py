from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"id": 1, "name": "Item 1", "description": "First item"})
    assert response.status_code == 200
    assert response.json()["name"] == "Item 1"