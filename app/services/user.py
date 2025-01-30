from uuid import UUID
import uuid
from sqlalchemy.orm import Session
from typing import List
from app.models import Users
from app.schemas import  UserCreate
from fastapi import HTTPException



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
    db_user = Users(**user.dict(), publique_id=unique_pub_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users_service(db: Session) -> List[Users]:
    """
    Returns a list of all users in the database.

    Args:
        db (Session): Database session for querying users.

    Returns:
        List[Users]: A list of all user records from the database.
    """
    return db.query(Users).all()


def get_user_by_id_service(db: Session, user_id: UUID) -> Users:
    """
    Returns a specific user by their unique ID.

    Args:
        db (Session): Database session for querying users.
        user_id (UUID): The unique identifier of the user to retrieve.

    Returns:
        Users: The user corresponding to the provided ID, or None if not found.
    """
    db_user = db.query(Users).filter(Users.id == user_id).first()
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
    db_user = db.query(Users).filter(Users.id == user_id).first()
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

def delete_user_service(user_id: UUID, db: Session):
    """
    Service to delete a user by their unique ID.

    Args:
        user_id (UUID): The unique identifier of the user to delete.
        db (Session): Database session for interacting with the database.

    Returns:
        Users: The deleted user's information.

    Raises:
        HTTPException:
            - 404 status code if the user is not found in the database.
    """
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user