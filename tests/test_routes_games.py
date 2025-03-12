import uuid
from app.models import Games

def test_create_game(client, test_db):
    game_data = {
        "name": "Super Mario",
        "description": "A classic platformer game",
        "nb_max_player": 4
    }

    response = client.post("/games/", json=game_data)

    assert response.status_code == 200
    assert response.json()["name"] == "Super Mario"
    assert response.json()["nb_max_player"] == 4

    game_id = uuid.UUID(response.json()["id"])
    db_game = test_db.query(Games).filter(Games.id == game_id).first()
    assert db_game is not None


def test_get_all_games(client, test_db):
    response = client.get("/games/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_game_by_id(client, test_db):
    game = Games(name="Zelda", description="Adventure game", nb_max_player=1)
    test_db.add(game)
    test_db.commit()

    response = client.get(f"/games/{game.id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Zelda"
    assert response.json()["nb_max_player"] == 1


def test_get_game_by_id_not_found(client):
    fake_game_id = uuid.uuid4()
    response = client.get(f"/games/{fake_game_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_update_game(client, test_db):
    game = Games(name="Pac-Man", description="Arcade game", nb_max_player=1)
    test_db.add(game)
    test_db.commit()

    updated_data = {
        "name": "Pac-Man Updated",
        "description": "Updated description",
        "nb_max_player": 2
    }

    response = client.put(f"/games/{game.id}", json=updated_data)

    assert response.status_code == 200
    assert response.json()["name"] == "Pac-Man Updated"
    assert response.json()["nb_max_player"] == 2


def test_update_game_not_found(client):
    fake_game_id = uuid.uuid4()
    updated_data = {
        "name": "New Game",
        "description": "New Description",
        "nb_max_player": 4  # S'assurer que ce champ est bien présent
    }

    response = client.put(f"/games/{fake_game_id}", json=updated_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


def test_delete_game(client, test_db):
    game = Games(name="Tetris", description="Puzzle game", nb_max_player=2)
    test_db.add(game)
    test_db.commit()

    response = client.delete(f"/games/{game.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Game deleted successfully"

    db_game = test_db.query(Games).filter(Games.id == game.id).first()
    assert db_game is None


def test_delete_game_not_found(client):
    fake_game_id = uuid.uuid4()
    response = client.delete(f"/games/{fake_game_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"
