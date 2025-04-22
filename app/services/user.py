from uuid import UUID
import uuid
from sqlalchemy.orm import Session
from typing import List
from app.models import Users
from app.schemas import UserCreate
from fastapi import HTTPException
from app.utils.db_utils import filter_deleted, soft_delete


def generate_unique_id(db: Session):
    """
    Generates a unique public ID for a new user.

    Args:
        db (Session): Database session for checking existing users.

    Returns:
        str: A unique 12-character string representing the public ID.

    Notes:
        This function generates a random ID and checks if it already exists in the database.
        If the ID exists, it retries until a unique ID is found.
    """
    while True:
        new_id = str(uuid.uuid4().int)[:12]

        existing_user = db.query(Users).filter_by(publique_id=new_id).first()
        if not existing_user:
            return new_id


def create_user_service(db: Session, user: UserCreate):
    """
    Creates a new user in the database with a unique public ID.

    Args:
        db (Session): Database session to interact with the database.
        user (UserCreate): The user data to create a new user.

    Returns:
        Users: The newly created user's information.

    Notes:
        This function generates a unique public ID and then inserts the new user into the database.
    """
    unique_pub_id = generate_unique_id(db)
    db_user = Users(**user.model_dump(), publique_id=unique_pub_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users_service(db: Session, include_deleted: bool = False) -> List[Users]:
    """
    Returns a list of all users in the database.

    Args:
        db (Session): Database session for querying users.
        include_deleted (bool, optional): Si True, inclut les utilisateurs supprimés. Par défaut à False.

    Returns:
        List[Users]: A list of all user records from the database.
    """
    query = db.query(Users)
    query = filter_deleted(query, include_deleted)
    return query.all()


def get_user_by_id_service(db: Session, user_id: UUID, include_deleted: bool = False) -> Users:
    """
    Returns a specific user by their unique ID.

    Args:
        db (Session): Database session for querying users.
        user_id (UUID): The unique identifier of the user to retrieve.
        include_deleted (bool, optional): Si True, inclut les utilisateurs supprimés. Par défaut à False.

    Returns:
        Users: The user corresponding to the provided ID, or None if not found.
    """
    query = db.query(Users).filter(Users.id == user_id)
    query = filter_deleted(query, include_deleted)
    db_user = query.first()
    return db_user


def update_user_service(user_id: UUID, user_data: UserCreate, db: Session):
    """
    Service to update an existing user's information.

    Args:
        user_id (UUID): The unique identifier of the user to update.
        user_data (UserCreate): The updated user data provided in the request.
        db (Session): Database session for interacting with the database.

    Returns:
        Users: The updated user's information.

    Raises:
        HTTPException:
            - 404 status code if the user is not found in the database.
    """
    query = db.query(Users).filter(Users.id == user_id)
    query = filter_deleted(query, False)  # Ne pas inclure les utilisateurs supprimés
    db_user = query.first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.first_name = user_data.first_name
    db_user.last_name = user_data.last_name
    db_user.nb_ticket = user_data.nb_ticket
    db_user.bar = user_data.bar
    db_user.firebase_id = user_data.firebase_id

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_service(user_id: UUID, db: Session, hard_delete: bool = False):
    """
    Service to delete a user by their unique ID.

    Args:
        user_id (UUID): The unique identifier of the user to delete.
        db (Session): Database session for interacting with the database.
        hard_delete (bool, optional): Si True, supprime définitivement l'enregistrement. Par défaut à False (soft delete).

    Returns:
        Users: The deleted user's information.

    Raises:
        HTTPException:
            - 404 status code if the user is not found in the database.
    """
    query = db.query(Users).filter(Users.id == user_id)
    query = filter_deleted(query, False)  # Ne pas inclure les utilisateurs déjà supprimés
    db_user = query.first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if hard_delete:
        # Suppression définitive
        db.delete(db_user)
        db.commit()
    else:
        # Suppression logique
        soft_delete(db_user, db)

    return db_user