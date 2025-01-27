from sqlalchemy.orm import Session
from models import Games
from schemas import GameCreate, GameUpdate
from uuid import UUID
from fastapi import HTTPException


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
    new_game = Games(**game.dict())
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game



def get_all_games_service(db: Session):
    """
    Retrieves all game records from the database.

    Args:
        db (Session): Database session for querying game records.

    Returns:
        List[Games]: A list of all game records in the database.
    """
    return db.query(Games).all()


def get_game_by_id_service(db: Session, game_id: UUID):
    """
    Retrieves a specific game by its unique ID.

    Args:
        db (Session): Database session for querying game records.
        game_id (UUID): The unique identifier of the game to retrieve.

    Returns:
        Games: The game corresponding to the provided ID.

    Raises:
        HTTPException: If the game with the given ID is not found (404 status code).
    """
    game = db.query(Games).filter(Games.id == game_id).first()
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
    game = db.query(Games).filter(Games.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Update the game fields with the new data
    for key, value in game_update.dict(exclude_unset=True).items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)
    return game


def delete_game_service(db: Session, game_id: UUID):
    """
    Deletes a game record from the database.

    Args:
        db (Session): Database session for interacting with the database.
        game_id (UUID): The unique identifier of the game to delete.

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the game with the given ID is not found (404 status code).
    """
    game = db.query(Games).filter(Games.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(game)
    db.commit()
    return {"message": "Game deleted successfully"}

