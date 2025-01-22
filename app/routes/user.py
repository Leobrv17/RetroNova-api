from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data_base  import get_db
from schemas import UserResponse, UserCreate
from services.user import create_user
from models import Users
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/users", response_model=UserResponse, tags=["Users"])
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.firebase_id == user.firebase_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User with this Firebase ID already exists")

    db_user = create_user(db, user)  # Appelle la fonction d'insertion
    return db_user

@router.get("/users", response_model=List[UserResponse], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user