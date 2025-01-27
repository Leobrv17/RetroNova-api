from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data_base import get_db
from schemas import GameCreate, GameResponse, GameUpdate
from services.games import (
    create_game_service,
    get_all_games_service,
    get_game_by_id_service,
    update_game_service,
    delete_game_service,
)
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=GameResponse, tags=["Games"], name="Create Games")
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new game.

    Args:
        game (GameCreate): The data required to create a new game, provided in the request body.
        db (Session): Database session dependency.

    Returns:
        GameResponse: The newly created game's information.

    Raises:
        HTTPException:
            - 400 status code if the game creation fails due to invalid input or other validation errors.
    """
    return create_game_service(db, game)


@router.get("/", response_model=list[GameResponse], tags=["Games"], name="Get Games")
def get_all_games(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all games.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[GameResponse]: A list of all games.

    Raises:
        HTTPException: If an error occurs while fetching the games (optional, if implemented).
    """
    return get_all_games_service(db)


@router.get("/{game_id}", response_model=GameResponse, tags=["Games"], name="Get Games by id")
def get_game_by_id(game_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a game by its unique ID.

    Args:
        game_id (UUID): The unique identifier of the game to retrieve.
        db (Session): Database session dependency.

    Returns:
        GameResponse: The retrieved game's information.

    Raises:
        HTTPException:
            - 404 status code if the game is not found.
    """
    return get_game_by_id_service(db, game_id)


@router.put("/{game_id}", response_model=GameResponse, tags=["Games"], name="Update Games")
def update_game(game_id: UUID, game: GameUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing game.

    Args:
        game_id (UUID): The unique identifier of the game to be updated.
        game (GameUpdate): The updated game data provided in the request body.
        db (Session): Database session dependency.

    Returns:
        GameResponse: The updated game's information.

    Raises:
        HTTPException: If the game is not found or the update fails.
    """
    return update_game_service(db, game_id, game)


@router.delete("/{game_id}", tags=["Games"], name="Delete Games")
def delete_game(game_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to delete an existing game.

    Args:
        game_id (UUID): The unique identifier of the game to be deleted.
        db (Session): Database session dependency.

    Returns:
        dict: A message confirming the deletion of the game.

    Raises:
        HTTPException: If the game is not found or the deletion fails.
    """
    return delete_game_service(db, game_id)

