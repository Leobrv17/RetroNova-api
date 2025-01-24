from uuid import UUID
import uuid
from sqlalchemy.orm import Session
from typing import List
from models import Users
from schemas import  UserCreate
from fastapi import HTTPException



def generate_unique_id(db: Session):
    while True:
        new_id = str(uuid.uuid4().int)[:12]

        existing_user = db.query(Users).filter_by(publique_id=new_id).first()
        if not existing_user:
            return new_id

def create_user(db: Session, user : UserCreate):
    unique_pub_id = generate_unique_id(db)
    db_user = Users(**user.dict(), publique_id=unique_pub_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session) -> List[Users]:
    """Retourne la liste de tous les utilisateurs"""
    return db.query(Users).all()

def get_user_by_id(db: Session, user_id: UUID) -> Users:
    """Retourne un utilisateur spécifique par son ID"""
    db_user = db.query(Users).filter(Users.id == user_id).first()
    return db_user


def update_user_service(user_id: UUID, user_data: UserCreate, db: Session):
    # Rechercher l'utilisateur
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Mettre à jour les champs
    db_user.first_name = user_data.first_name
    db_user.last_name = user_data.last_name
    db_user.nb_ticket = user_data.nb_ticket
    db_user.bar = user_data.bar
    db_user.firebase_id = user_data.firebase_id

    # Sauvegarder les modifications
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_service(user_id: UUID, db: Session):
    """
    Supprime un utilisateur par son ID.
    """
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user