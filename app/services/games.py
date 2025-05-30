from sqlalchemy.orm import Session
from app.models import Games
from app.schemas import GameCreate, GameUpdate
from uuid import UUID
from fastapi import HTTPException
from app.utils.db_utils import filter_deleted, soft_delete


def create_game_service(db: Session, game: GameCreate):
    """
    Creates a new game record in the database.

    Args:
        db (Session): Database session to interact with the database.
        game (GameCreate): The game data to create a new game.

    Returns:
        Games: The newly created game record.

    Notes:
        This function adds a new game to the database and commits the transaction.
    """
    new_game = Games(**game.model_dump())
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


def get_all_games_service(db: Session, include_deleted: bool = False):
    """
    Retrieves all game records from the database.

    Args:
        db (Session): Database session for querying game records.
        include_deleted (bool, optional): If True, include soft-deleted games. Defaults to False.

    Returns:
        List[Games]: A list of all game records in the database.
    """
    query = db.query(Games)
    query = filter_deleted(query, include_deleted)
    return query.all()


def get_game_by_id_service(db: Session, game_id: UUID, include_deleted: bool = False):
    """
    Retrieves a specific game by its unique ID.

    Args:
        db (Session): Database session for querying game records.
        game_id (UUID): The unique identifier of the game to retrieve.
        include_deleted (bool, optional): If True, include soft-deleted games. Defaults to False.

    Returns:
        Games: The game corresponding to the provided ID.

    Raises:
        HTTPException: If the game with the given ID is not found (404 status code).
    """
    query = db.query(Games).filter(Games.id == game_id)
    query = filter_deleted(query, include_deleted)
    game = query.first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


def update_game_service(db: Session, game_id: UUID, game_update: GameUpdate):
    """
    Updates the details of an existing game record.

    Args:
        db (Session): Database session for interacting with the database.
        game_id (UUID): The unique identifier of the game to update.
        game_update (GameUpdate): The new data to update the game record with.

    Returns:
        Games: The updated game record.

    Raises:
        HTTPException: If the game with the given ID is not found (404 status code).
    """
    query = db.query(Games).filter(Games.id == game_id)
    query = filter_deleted(query, False)  # Ne pas inclure les jeux supprimés
    game = query.first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Update the game fields with the new data
    for key, value in game_update.dict(exclude_unset=True).items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)
    return game


def delete_game_service(db: Session, game_id: UUID, hard_delete: bool = False):
    """
    Deletes a game record from the database.

    Args:
        db (Session): Database session for interacting with the database.
        game_id (UUID): The unique identifier of the game to delete.
        hard_delete (bool, optional): If True, physically delete the record. Defaults to False.

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the game with the given ID is not found (404 status code).
    """
    query = db.query(Games).filter(Games.id == game_id)
    query = filter_deleted(query, False)
    game = query.first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if hard_delete:
        db.delete(game)
        db.commit()
    else:
        soft_delete(game, db)

    return {"message": "Game deleted successfully"}


def restore_game_service(db: Session, game_id: UUID):
    """
    Restores a soft-deleted game.

    Args:
        db (Session): Database session for interacting with the database.
        game_id (UUID): The unique identifier of the game to restore.

    Returns:
        Games: The restored game record.

    Raises:
        HTTPException:
            - 404: If the game is not found.
            - 400: If the game is not deleted.
    """
    game = db.query(Games).filter(Games.id == game_id).first()

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if not game.is_deleted:
        raise HTTPException(status_code=400, detail="Game is not deleted")

    game.is_deleted = False
    game.deleted_at = None
    db.commit()
    db.refresh(game)

    return game