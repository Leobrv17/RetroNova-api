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

@router.post("/", response_model=GameResponse)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    return create_game_service(db, game)

@router.get("/", response_model=list[GameResponse])
def get_all_games(db: Session = Depends(get_db)):
    return get_all_games_service(db)

@router.get("/{game_id}", response_model=GameResponse)
def get_game_by_id(game_id: UUID, db: Session = Depends(get_db)):
    return get_game_by_id_service(db, game_id)

@router.put("/{game_id}", response_model=GameResponse)
def update_game(game_id: UUID, game: GameUpdate, db: Session = Depends(get_db)):
    return update_game_service(db, game_id, game)

@router.delete("/{game_id}")
def delete_game(game_id: UUID, db: Session = Depends(get_db)):
    return delete_game_service(db, game_id)
