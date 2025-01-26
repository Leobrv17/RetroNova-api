from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from data_base import get_db
from schemas import FriendsCreate, FriendsResponse, FriendsUpdate
from services.friends import (
    create_friend_service,
    get_friend_service,
    update_friend_service,
    delete_friend_service,
    get_all_friends_service
)

router = APIRouter()


@router.post("/", response_model=FriendsResponse, tags=["Friends"], name="Create Friend")
def create_friend(friend_data: FriendsCreate, db: Session = Depends(get_db)):
    return create_friend_service(db, friend_data)

@router.get("/", response_model=list[FriendsResponse])  # Nouveau endpoint
def get_all_friends(db: Session = Depends(get_db)):
    return get_all_friends_service(db)

@router.get("/{friend_id}", response_model=FriendsResponse, tags=["Friends"], name="Get Friend by id")
def get_friend(friend_id: UUID, db: Session = Depends(get_db)):
    return get_friend_service(db, friend_id)


@router.put("/{friend_id}", response_model=FriendsResponse, tags=["Friends"], name="Update Friend")
def update_friend(friend_id: UUID, update_data: FriendsUpdate, db: Session = Depends(get_db)):
    return update_friend_service(db, friend_id, update_data)


@router.delete("/{friend_id}", response_model=FriendsResponse, tags=["Friends"], name="Delete Friend")
def delete_friend(friend_id: UUID, db: Session = Depends(get_db)):
    return delete_friend_service(db, friend_id)
