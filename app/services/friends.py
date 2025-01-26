from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from models import Friends
from schemas import FriendsCreate, FriendsUpdate

def create_friend_service(db: Session, friend_data: FriendsCreate):
    # Vérifier si la relation existe déjà
    existing_friend = db.query(Friends).filter(
        Friends.friend_from_id == friend_data.friend_from_id,
        Friends.friend_to_id == friend_data.friend_to_id
    ).first()

    if existing_friend:
        raise HTTPException(status_code=400, detail="Friendship already exists")

    # Créer la relation
    new_friend = Friends(**friend_data.dict())
    db.add(new_friend)
    db.commit()
    db.refresh(new_friend)
    return new_friend

def get_friend_service(db: Session, friend_id: UUID):
    friend = db.query(Friends).filter(Friends.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")
    return friend

def get_all_friends_service(db: Session):
    """
    Récupère toutes les entrées de la table Friends.
    """
    return db.query(Friends).all()

def update_friend_service(db: Session, friend_id: UUID, update_data: FriendsUpdate):
    friend = db.query(Friends).filter(Friends.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    # Mise à jour des champs
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(friend, key, value)

    db.commit()
    db.refresh(friend)
    return friend

def delete_friend_service(db: Session, friend_id: UUID):
    friend = db.query(Friends).filter(Friends.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    db.delete(friend)
    db.commit()
    return friend
