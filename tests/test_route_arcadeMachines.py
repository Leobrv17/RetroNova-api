import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.data_base import get_db
from app.models import ArcadeMachines
from sqlalchemy.orm import Session
from app.schemas import ArcadeMachineCreate, ArcadeMachineUpdate


def test_create_arcade_machine(client, test_db):
    """Test de création d'une machine d'arcade"""
    machine_data = {
        "description": "Super Machine",
        "localisation": "Paris",
        "game1_id": str(uuid4()),
        "game2_id": str(uuid4())
    }

    response = client.post("/arcade_machines/", json=machine_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Super Machine"
    assert data["localisation"] == "Paris"


def test_get_all_arcade_machines(client, test_db):
    """Test de récupération de toutes les machines d'arcade"""
    response = client.get("/arcade_machines/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_arcade_machine_by_id(client, test_db):
    """Test de récupération d'une machine par son ID"""
    # Créer une machine pour le test
    machine = ArcadeMachines(id=uuid4(), description="Test Machine", localisation="Lyon", game1_id=uuid4(), game2_id=uuid4())
    test_db.add(machine)
    test_db.commit()

    response = client.get(f"/arcade_machines/{machine.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(machine.id)
    assert data["description"] == "Test Machine"


def test_get_nonexistent_arcade_machine(client, test_db):
    """Test de récupération d'une machine qui n'existe pas"""
    fake_machine_id = uuid4()
    response = client.get(f"/arcade_machines/{fake_machine_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Arcade machine not found"


def test_update_arcade_machine(client, test_db):
    """Test de mise à jour d'une machine existante"""
    # Créer une machine pour le test
    machine = ArcadeMachines(id=uuid4(), description="Old Machine", localisation="Nice", game1_id=uuid4(), game2_id=uuid4())
    test_db.add(machine)
    test_db.commit()

    update_data = {
        "description": "Updated Machine",
        "localisation": "Marseille",
        "game1_id": str(machine.game1_id),
        "game2_id": str(machine.game2_id)
    }

    response = client.put(f"/arcade_machines/{machine.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated Machine"
    assert data["localisation"] == "Marseille"


def test_update_nonexistent_arcade_machine(client, test_db):
    """Test de mise à jour d'une machine qui n'existe pas"""
    fake_machine_id = uuid4()
    update_data = {
        "description": "Nonexistent Machine",
        "localisation": "Nowhere",
        "game1_id": str(uuid4()),
        "game2_id": str(uuid4())
    }

    response = client.put(f"/arcade_machines/{fake_machine_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Arcade machine not found"


def test_delete_arcade_machine(client, test_db):
    """Test de suppression d'une machine existante"""
    # Créer une machine pour le test
    machine = ArcadeMachines(id=uuid4(), description="To be deleted", localisation="Bordeaux", game1_id=uuid4(), game2_id=uuid4())
    test_db.add(machine)
    test_db.commit()

    response = client.delete(f"/arcade_machines/{machine.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Arcade machine deleted successfully"}

    # Vérifier que la machine n'existe plus
    response = client.get(f"/arcade_machines/{machine.id}")
    assert response.status_code == 404


def test_delete_nonexistent_arcade_machine(client, test_db):
    """Test de suppression d'une machine inexistante"""
    fake_machine_id = uuid4()
    response = client.delete(f"/arcade_machines/{fake_machine_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Arcade machine not found"
