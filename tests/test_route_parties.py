import uuid
from app.models import Parties



def test_create_party(client, test_db):
    """Test de création d'une partie."""
    party_data = {
        "player1_id": str(uuid.uuid4()),
        "player2_id": str(uuid.uuid4()),
        "game_id": str(uuid.uuid4()),
        "machine_id": str(uuid.uuid4()),
        "total_score": 500,
        "p1_score": 300,
        "p2_score": 200,
        "password": 1234,
        "done": False,
        "cancel": False,
        "bar": True
    }
    response = client.post("/parties/", json=party_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["total_score"] == party_data["total_score"]

def test_get_all_parties(client, test_db):
    """Test de récupération de toutes les parties."""
    response = client.get("/parties/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_party_by_id(client, test_db):
    """Test de récupération d'une partie existante."""
    party = Parties(
        player1_id=uuid.uuid4(),
        player2_id=uuid.uuid4(),
        game_id=uuid.uuid4(),
        machine_id=uuid.uuid4(),
        total_score=300,
        p1_score=150,
        p2_score=150,
        password=5678,
        done=False,
        cancel=False,
        bar=False
    )
    test_db.add(party)
    test_db.commit()
    test_db.refresh(party)

    response = client.get(f"/parties/{party.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(party.id)
    assert data["total_score"] == 300

def test_get_party_by_id_not_found(client, test_db):
    """Test de récupération d'une partie inexistante (404)."""
    fake_id = str(uuid.uuid4())
    response = client.get(f"/parties/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Party not found"

def test_update_party(client, test_db):
    """Test de mise à jour d'une partie existante."""
    party = Parties(
        player1_id=uuid.uuid4(),
        player2_id=uuid.uuid4(),
        game_id=uuid.uuid4(),
        machine_id=uuid.uuid4(),
        total_score=100,
        p1_score=50,
        p2_score=50,
        password=1234,
        done=False,
        cancel=False,
        bar=False
    )
    test_db.add(party)
    test_db.commit()
    test_db.refresh(party)

    update_data = {
        "total_score": 700,
        "p1_score": 400,
        "p2_score": 300,
        "done": True
    }
    response = client.put(f"/parties/{party.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["total_score"] == 700
    assert data["done"] is True

def test_update_party_not_found(client, test_db):
    """Test de mise à jour d'une partie inexistante (404)."""
    fake_id = str(uuid.uuid4())
    update_data = {
        "total_score": 800,
        "p1_score": 450,
        "p2_score": 350,
        "done": True
    }
    response = client.put(f"/parties/{fake_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Party not found"

def test_delete_party(client, test_db):
    """Test de suppression d'une partie existante."""
    party = Parties(
        player1_id=uuid.uuid4(),
        player2_id=uuid.uuid4(),
        game_id=uuid.uuid4(),
        machine_id=uuid.uuid4(),
        total_score=200,
        p1_score=100,
        p2_score=100,
        password=4321,
        done=True,
        cancel=False,
        bar=True
    )
    test_db.add(party)
    test_db.commit()
    test_db.refresh(party)

    response = client.delete(f"/parties/{party.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Party deleted successfully"

def test_delete_party_not_found(client, test_db):
    """Test de suppression d'une partie inexistante (404)."""
    fake_id = str(uuid.uuid4())
    response = client.delete(f"/parties/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Party not found"
