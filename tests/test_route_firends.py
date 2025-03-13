import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4
from app.models import Friends
from app.schemas import FriendsCreate, FriendsUpdate
from app.services.friends import create_friend_service


def test_create_friend(client, test_db):
    """Test de la création d'une amitié."""
    friend_data = {
        "friend_from_id": str(uuid4()),
        "friend_to_id": str(uuid4())
    }
    response = client.post("/friends/", json=friend_data)
    assert response.status_code == 200
    data = response.json()
    assert data["friend_from_id"] == friend_data["friend_from_id"]
    assert data["friend_to_id"] == friend_data["friend_to_id"]
    assert data["accept"] is False
    assert data["decline"] is False
    assert data["delete"] is False


def test_create_duplicate_friendship(client, test_db):
    """Test de création d'une amitié déjà existante."""
    friend_data = FriendsCreate(friend_from_id=uuid4(), friend_to_id=uuid4())
    create_friend_service(test_db, friend_data)

    response = client.post("/friends/", json=friend_data.model_dump(mode="json"))
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_all_friends(client, test_db):
    """Test de récupération de toutes les amitiés."""
    response = client.get("/friends/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_friend_by_id(client, test_db):
    """Test de récupération d'une amitié par son ID."""
    friend = Friends(friend_from_id=uuid4(), friend_to_id=uuid4())
    test_db.add(friend)
    test_db.commit()
    test_db.refresh(friend)

    response = client.get(f"/friends/{friend.id}")
    assert response.status_code == 200
    assert response.json()["id"] == str(friend.id)


def test_get_friend_by_id_not_found(client, test_db):
    """Test de récupération d'une amitié inexistante."""
    fake_id = uuid4()
    response = client.get(f"/friends/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Friend not found"

def test_update_friend(client, test_db):
    """Test de mise à jour d'une amitié."""
    friend = Friends(friend_from_id=uuid4(), friend_to_id=uuid4())
    test_db.add(friend)
    test_db.commit()

    update_data = {"accept": True}
    response = client.put(f"/friends/{friend.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["accept"] is True

def test_update_friend_not_found(client, test_db):
    """Test de mise à jour d'une amitié inexistante."""
    fake_id = uuid4()
    update_data = {"accept": True}
    response = client.put(f"/friends/{fake_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Friend not found"

def test_delete_friend(client, test_db):
    """Test de suppression d'une amitié."""
    friend = Friends(friend_from_id=uuid4(), friend_to_id=uuid4())
    test_db.add(friend)
    test_db.commit()

    response = client.delete(f"/friends/{friend.id}")
    assert response.status_code == 200

def test_delete_friend_not_found(client, test_db):
    """Test de suppression d'une amitié inexistante."""
    fake_id = uuid4()
    response = client.delete(f"/friends/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Friend not found"
