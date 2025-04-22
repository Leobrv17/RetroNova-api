from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.data_base import get_db
from app.schemas import GameCreate, GameResponse, GameUpdate
from app.services.games import (
    create_game_service,
    get_all_games_service,
    get_game_by_id_service,
    update_game_service,
    delete_game_service,
    restore_game_service
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
def get_all_games(
    include_deleted: bool = Query(False, description="Include soft-deleted games"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve all games.

    Args:
        include_deleted (bool, optional): If True, include soft-deleted games. Defaults to False.
        db (Session): Database session dependency.

    Returns:
        List[GameResponse]: A list of all games.

    Raises:
        HTTPException: If an error occurs while fetching the games (optional, if implemented).
    """
    return get_all_games_service(db, include_deleted)


@router.get("/{game_id}", response_model=GameResponse, tags=["Games"], name="Get Games by id")
def get_game_by_id(
    game_id: UUID,
    include_deleted: bool = Query(False, description="Include soft-deleted games"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve a game by its unique ID.

    Args:
        game_id (UUID): The unique identifier of the game to retrieve.
        include_deleted (bool, optional): If True, include soft-deleted games. Defaults to False.
        db (Session): Database session dependency.

    Returns:
        GameResponse: The retrieved game's information.

    Raises:
        HTTPException:
            - 404 status code if the game is not found.
    """
    return get_game_by_id_service(db, game_id, include_deleted)


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
def delete_game(
    game_id: UUID,
    hard_delete: bool = Query(False, description="Perform hard delete instead of soft delete"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to delete an existing game.

    Args:
        game_id (UUID): The unique identifier of the game to be deleted.
        hard_delete (bool, optional): If True, permanently delete the game. Defaults to False (soft delete).
        db (Session): Database session dependency.

    Returns:
        dict: A message confirming the deletion of the game.

    Raises:
        HTTPException: If the game is not found or the deletion fails.
    """
    return delete_game_service(db, game_id, hard_delete)


@router.post("/{game_id}/restore", response_model=GameResponse, tags=["Games"], name="Restore Deleted Game")
def restore_game(game_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to restore a soft-deleted game.

    Args:
        game_id (UUID): The unique identifier of the game to be restored.
        db (Session): Database session dependency.

    Returns:
        GameResponse: The restored game's information.

    Raises:
        HTTPException:
            - 404 status code if the game is not found.
            - 400 status code if the game is not deleted.
    """
    return restore_game_service(db, game_id)