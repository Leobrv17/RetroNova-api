from app.models import Users
import uuid


def test_create_user(client, test_db):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "nb_ticket": 3,
        "bar": False,
        "firebase_id": "unique_firebase_id"
    }

    # Faire la requête pour créer un utilisateur
    response = client.post("/users/", json=user_data)

    # Vérifier que le statut est 200 pour une création réussie
    if response.status_code == 400:
        print(f"Error message: {response.json()['detail']}")  # Afficher le détail de l'erreur dans les logs
        assert response.json()["detail"] == "User with this Firebase ID already exists"

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert response.json()["first_name"] == "John"
    assert response.json()["last_name"] == "Doe"

    # Convertir l'ID en UUID avant la requête
    user_id = uuid.UUID(response.json()["id"])

    # Vérifier que l'utilisateur a été ajouté à la base de données
    db_user = test_db.query(Users).filter(Users.id == user_id).first()
    assert db_user is not None, f"User with ID {user_id} not found in database"


def test_create_user_with_existing_firebase_id(client, test_db):
    # Utilisateur déjà existant
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "nb_ticket": 3,
        "bar": False,
        "firebase_id": "unique_firebase_id"  # ID utilisé dans le test précédent
    }

    # Faire la requête pour créer un utilisateur avec un Firebase ID existant
    response = client.post("/users/", json=user_data)

    # Vérifier qu'une erreur est renvoyée
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this Firebase ID already exists"


def test_get_all_users(client, test_db):
    # Assurez-vous qu'il y a des utilisateurs dans la base de données de test
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "nb_ticket": 5,
        "bar": True,
        "firebase_id": "unique_firebase_id_2"
    }
    client.post("/users/", json=user_data)

    # Faire la requête pour récupérer tous les utilisateurs
    response = client.get("/users/")

    # Vérifier le statut de la réponse
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Au moins un utilisateur


def test_get_user_by_id(client, test_db):
    # Créer un utilisateur d'abord
    user_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "nb_ticket": 2,
        "bar": False,
        "firebase_id": "unique_firebase_id_3"
    }
    response = client.post("/users/", json=user_data)
    user_id = uuid.UUID(response.json()["id"])

    # Faire la requête pour récupérer l'utilisateur par ID
    response = client.get(f"/users/{user_id}")

    # Vérifier que la réponse est correcte
    assert response.status_code == 200
    assert response.json()["id"] == str(user_id)
    assert response.json()["first_name"] == "Jane"
    assert response.json()["last_name"] == "Doe"


def test_get_user_by_id_not_found(client):
    # ID d'un utilisateur qui n'existe pas
    non_existent_user_id = uuid.uuid4()

    # Faire la requête pour récupérer l'utilisateur par ID
    response = client.get(f"/users/{non_existent_user_id}")

    # Vérifier que le code de statut est 404
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user(client, test_db):
    # Créer un utilisateur d'abord
    user_data = {
        "first_name": "Alex",
        "last_name": "Johnson",
        "nb_ticket": 1,
        "bar": True,
        "firebase_id": "unique_firebase_id_4"
    }
    response = client.post("/users/", json=user_data)
    user_id = uuid.UUID(response.json()["id"])

    # Nouvelle donnée pour la mise à jour
    updated_user_data = {
        "first_name": "Alex",
        "last_name": "Johnson Updated",
        "nb_ticket": 10,
        "bar": False,
        "firebase_id": "unique_firebase_id_4"
    }

    # Faire la requête pour mettre à jour l'utilisateur
    response = client.put(f"/users/{user_id}", json=updated_user_data)

    # Vérifier que la réponse est correcte
    assert response.status_code == 200
    assert response.json()["first_name"] == "Alex"
    assert response.json()["last_name"] == "Johnson Updated"
    assert response.json()["nb_ticket"] == 10


def test_delete_user(client, test_db):
    # Créer un utilisateur d'abord
    user_data = {
        "first_name": "Chris",
        "last_name": "Green",
        "nb_ticket": 7,
        "bar": False,
        "firebase_id": "unique_firebase_id_5"
    }
    response = client.post("/users/", json=user_data)
    user_id = uuid.UUID(response.json()["id"])

    # Faire la requête pour supprimer l'utilisateur
    response = client.delete(f"/users/{user_id}")

    # Vérifier que la réponse est correcte
    assert response.status_code == 200
    assert response.json()["id"] == str(user_id)

    # Vérifier que l'utilisateur n'existe plus dans la base de données
    db_user = test_db.query(Users).filter(Users.id == user_id).first()
    assert db_user is None, f"User with ID {user_id} still exists in the database"

def test_delete_non_existent_user(client):
    non_existent_user_id = uuid.uuid4()  # Générer un UUID qui n'existe pas

    response = client.delete(f"/users/{non_existent_user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_update_non_existent_user(client):
    non_existent_user_id = uuid.uuid4()  # Générer un ID aléatoire

    updated_user_data = {
        "first_name": "Updated",
        "last_name": "User",
        "nb_ticket": 5,
        "bar": True,
        "firebase_id": "random_firebase_id"
    }

    response = client.put(f"/users/{non_existent_user_id}", json=updated_user_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
