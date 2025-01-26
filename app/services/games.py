from sqlalchemy.orm import Session
from models import Games
from schemas import GameCreate, GameUpdate
from uuid import UUID
from fastapi import HTTPException


def create_game_service(db: Session, game: GameCreate):
    new_game = Games(**game.dict())
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


def get_all_games_service(db: Session):
    return db.query(Games).all()


def get_game_by_id_service(db: Session, game_id: UUID):
    game = db.query(Games).filter(Games.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


def update_game_service(db: Session, game_id: UUID, game_update: GameUpdate):
    game = db.query(Games).filter(Games.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    for key, value in game_update.dict(exclude_unset=True).items():
        setattr(game, key, value)

    db.commit()
    db.refresh(game)
    return game


def delete_game_service(db: Session, game_id: UUID):
    game = db.query(Games).filter(Games.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    db.delete(game)
    db.commit()
    return {"message": "Game deleted successfully"}
