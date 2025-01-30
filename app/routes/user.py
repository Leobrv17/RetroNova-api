from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.data_base import get_db
from app.schemas import UserResponse, UserCreate
from app.services.user import create_user_service, get_users_service, get_user_by_id_service, update_user_service, delete_user_service
from app.models import Users
from typing import List
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=UserResponse, tags=["Users"], name="Create User")
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
        Endpoint to create a new user.

        Args:
            user (UserCreate): The data required to create a new user, provided in the request body.
            db (Session): Database session dependency.

        Returns:
            UserResponse: The newly created user's information.

        Raises:
            HTTPException:
                - 400 status code if a user with the given Firebase ID already exists.
        """
    db_user = db.query(Users).filter(Users.firebase_id == user.firebase_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User with this Firebase ID already exists")

    db_user = create_user_service(db, user)  # Appelle la fonction d'insertion
    return db_user


@router.get("/", response_model=List[UserResponse], tags=["Users"], name="Get User")
def get_all_users(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all users.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[UserResponse]: A list of all users.

    Raises:
        HTTPException: If an error occurs while fetching the users (optional, if implemented).
    """
    users = get_users_service(db)
    return users


@router.get("/{user_id}", response_model=UserResponse, tags=["Users"], name="Get User by id")
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a user by their unique ID.

    Args:
        user_id (UUID): The unique identifier of the user to retrieve.
        db (Session): Database session dependency.

    Returns:
        UserResponse: The retrieved user information.

    Raises:
        HTTPException: If the user is not found (404 status).
    """
    user = get_user_by_id_service(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse, tags=["Users"], name="Update User")
def update_user(user_id: UUID, user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing user.

    Args:
        user_id (UUID): The unique identifier of the user to be updated.
        user (UserCreate): The updated user data provided in the request body.
        db (Session): Database session dependency.

    Returns:
        UserResponse: The updated user information.

    Raises:
        HTTPException: If the update fails or the user is not found.
    """
    try:
        updated_user = update_user_service(user_id, user, db)
        return updated_user
    except HTTPException as e:
        raise e


@router.delete("/{user_id}", response_model=UserResponse, tags=["Users"], name="Delete User")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to delete an existing user.

    Args:
        user_id (UUID): The unique identifier of the user to be deleted.
        db (Session): Database session dependency.

    Returns:
        UserResponse: The deleted user information.

    Raises:
        HTTPException: If the user is not found or the deletion fails.
    """
    return delete_user_service(user_id=user_id, db=db)
