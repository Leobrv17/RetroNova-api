from app.models import Users

# Test du CRUD
def test_create_user(client, test_db):
    user_data ={
        "first_name": "John",
        "last_name": "Doe",
        "nb_ticket": 3,
        "bar": False,
        "firebase_id": "unique_firebase_id"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"

    # Vérifier que l'utilisateur a été ajouté à la base de données
    db_user = test_db.query(Users).filter(Users.id == response.json()["id"]).first()
    assert db_user is not None
