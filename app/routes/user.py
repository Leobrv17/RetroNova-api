from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data_base  import get_db
from schemas import UserResponse, UserCreate
from services.user import create_user, get_users, get_user_by_id, update_user_service, delete_user_service
from models import Users
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=UserResponse, tags=["Users"],name="Create User")
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.firebase_id == user.firebase_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User with this Firebase ID already exists")

    db_user = create_user(db, user)  # Appelle la fonction d'insertion
    return db_user

@router.get("/", response_model=List[UserResponse], tags=["Users"], name="Get User")
def read_users(db: Session = Depends(get_db)):
    """Route pour récupérer tous les utilisateurs"""
    users = get_users(db)
    return users

@router.get("/{user_id}", response_model=UserResponse, tags=["Users"], name="Get User by id")
def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """Route pour récupérer un utilisateur par ID"""
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse, tags=["Users"], name="Update User")
def update_user(user_id: UUID, user: UserCreate, db: Session = Depends(get_db)):
    try:
        updated_user = update_user_service(user_id, user, db)
        return updated_user
    except HTTPException as e:
        raise e

@router.delete("/{user_id}", response_model=UserResponse, tags=["Users"], name="Delete User")
def delete_user_route(user_id: UUID, db: Session = Depends(get_db)):
    """
    Route pour supprimer un utilisateur.
    """
    return delete_user_service(user_id=user_id, db=db)