import uuid

from app.models import Payments



def test_create_payment(client, test_db):
    """Test de création d'un paiement."""
    payment_data = {
        "user_id": str(uuid.uuid4()),
        "session_stripe_token": "test_token_123",
        "amount": 100,
        "nb_ticket": 2
    }
    response = client.post("/payments/", json=payment_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["session_stripe_token"] == payment_data["session_stripe_token"]
    assert data["amount"] == payment_data["amount"]

def test_get_all_payments(client, test_db):
    """Test de récupération de tous les paiements."""
    response = client.get("/payments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_payment_by_id(client, test_db):
    """Test de récupération d'un paiement existant."""
    payment = Payments(
        user_id=uuid.uuid4(),
        session_stripe_token="token_abc",
        amount=120,
        nb_ticket=1
    )
    test_db.add(payment)
    test_db.commit()
    test_db.refresh(payment)

    response = client.get(f"/payments/{payment.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(payment.id)
    assert data["session_stripe_token"] == "token_abc"

def test_get_payment_by_id_not_found(client, test_db):
    """Test de récupération d'un paiement inexistant (404)."""
    fake_id = str(uuid.uuid4())
    response = client.get(f"/payments/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"


def test_update_payment(client, test_db):
    """Test de mise à jour d'un paiement."""
    # Création d'un paiement pour test
    payment = Payments(
        user_id=uuid.uuid4(),
        session_stripe_token="old_token",
        amount=50,
        nb_ticket=1
    )
    test_db.add(payment)
    test_db.commit()
    test_db.refresh(payment)

    update_data = {
        "session_stripe_token": "new_token",
        "amount": 200,
        "nb_ticket": 3
    }
    response = client.put(f"/payments/{payment.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["session_stripe_token"] == "new_token"
    assert data["amount"] == 200
    assert data["nb_ticket"] == 3

def test_update_payment_not_found(client, test_db):
    """Test de mise à jour d'un paiement inexistant (404)."""
    fake_id = str(uuid.uuid4())
    update_data = {
        "session_stripe_token": "new_token",
        "amount": 200,
        "nb_ticket": 3
    }
    response = client.put(f"/payments/{fake_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"

def test_delete_payment(client, test_db):
    """Test de suppression d'un paiement."""
    # Création d'un paiement pour test
    payment = Payments(
        user_id=uuid.uuid4(),
        session_stripe_token="delete_token",
        amount=75,
        nb_ticket=2
    )
    test_db.add(payment)
    test_db.commit()
    test_db.refresh(payment)

    response = client.delete(f"/payments/{payment.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Payment deleted successfully"

def test_delete_payment_not_found(client, test_db):
    """Test de suppression d'un paiement inexistant (404)."""
    fake_id = str(uuid.uuid4())
    response = client.delete(f"/payments/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"