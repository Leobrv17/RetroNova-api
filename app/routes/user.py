from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.data_base import get_db
from app.schemas import UserResponse, UserCreate
from app.services.user import create_user_service, get_users_service, get_user_by_id_service, update_user_service, \
    delete_user_service
from app.models import Users
from typing import List
from uuid import UUID
from app.utils.db_utils import filter_deleted

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
def get_all_users(
        include_deleted: bool = Query(False, description="Inclure les utilisateurs supprimés"),
        db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve all users.

    Args:
        include_deleted (bool): If True, include soft-deleted users in the response
        db (Session): Database session dependency.

    Returns:
        List[UserResponse]: A list of all users.

    Raises:
        HTTPException: If an error occurs while fetching the users (optional, if implemented).
    """
    users = get_users_service(db, include_deleted)
    return users


@router.get("/{user_id}", response_model=UserResponse, tags=["Users"], name="Get User by id")
def get_user_by_id(
        user_id: UUID,
        include_deleted: bool = Query(False, description="Inclure les utilisateurs supprimés"),
        db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve a user by their unique ID.

    Args:
        user_id (UUID): The unique identifier of the user to retrieve.
        include_deleted (bool): If True, retrieve even if the user is soft-deleted
        db (Session): Database session dependency.

    Returns:
        UserResponse: The retrieved user information.

    Raises:
        HTTPException: If the user is not found (404 status).
    """
    user = get_user_by_id_service(db, user_id, include_deleted)
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
def delete_user(
        user_id: UUID,
        hard_delete: bool = Query(False, description="Supprimer définitivement l'utilisateur"),
        db: Session = Depends(get_db)
):
    """
    Endpoint to delete an existing user.

    Args:
        user_id (UUID): The unique identifier of the user to be deleted.
        hard_delete (bool): If True, physically delete the user from the database. If False (default), perform a soft delete.
        db (Session): Database session dependency.

    Returns:
        UserResponse: The deleted user information.

    Raises:
        HTTPException: If the user is not found or the deletion fails.
    """
    return delete_user_service(user_id=user_id, db=db, hard_delete=hard_delete)


@router.post("/{user_id}/restore", response_model=UserResponse, tags=["Users"], name="Restore Deleted User")
def restore_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to restore a soft-deleted user.

    Args:
        user_id (UUID): The unique identifier of the user to be restored.
        db (Session): Database session dependency.

    Returns:
        UserResponse: The restored user information.

    Raises:
        HTTPException:
            - 404: If the user is not found.
            - 400: If the user is not deleted.
    """
    # Récupérer l'utilisateur, y compris s'il est supprimé
    user = get_user_by_id_service(db, user_id, include_deleted=True)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_deleted:
        raise HTTPException(status_code=400, detail="User is not deleted")

    # Restaurer l'utilisateur
    user.is_deleted = False
    user.deleted_at = None
    db.commit()
    db.refresh(user)

    return user


@router.get("/firebase/{firebase_id}", response_model=UserResponse, tags=["Users"])
def get_user_by_firebase_id(
        firebase_id: str,
        include_deleted: bool = Query(False, description="Inclure les utilisateurs supprimés"),
        db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve a user by their Firebase ID.

    Args:
        firebase_id (str): The Firebase ID of the user to retrieve.
        include_deleted (bool): If True, include soft-deleted users in the response
        db (Session): Database session dependency.

    Returns:
        UserResponse: The retrieved user information.

    Raises:
        HTTPException: If the user is not found (404 status).
    """
    query = db.query(Users).filter(Users.firebase_id == firebase_id)
    query = filter_deleted(query, include_deleted)
    user = query.first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/public/{public_id}", response_model=UserResponse, tags=["Users"], name="Get User by Public ID")
def get_user_by_public_id(
        public_id: str,
        db: Session = Depends(get_db)
):
    """
    Endpoint pour récupérer un utilisateur par son ID public.

    Args:
        public_id (str): L'ID public de l'utilisateur à récupérer.
        db (Session): Dépendance de session de base de données.

    Returns:
        UserResponse: Les informations de l'utilisateur trouvé.

    Raises:
        HTTPException: Si l'utilisateur n'est pas trouvé (404 status).
    """
    user = db.query(Users).filter(Users.publique_id == public_id, Users.is_deleted == False).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé avec cet ID public")
    return user