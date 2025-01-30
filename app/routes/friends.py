from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.data_base import get_db
from app.schemas import FriendsCreate, FriendsResponse, FriendsUpdate
from app.services.friends import (
    create_friend_service,
    get_friend_by_id_service,
    update_friend_service,
    delete_friend_service,
    get_all_friends_service
)

router = APIRouter()


@router.post("/", response_model=FriendsResponse, tags=["Friends"], name="Create Friend")
def create_friend(friend_data: FriendsCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new friendship.

    Args:
        friend_data (FriendsCreate): The data required to create a new friendship, provided in the request body.
        db (Session): Database session dependency.

    Returns:
        FriendsResponse: The newly created friendship information.

    Raises:
        HTTPException:
            - 400 status code if the friendship already exists between the two users.
    """
    return create_friend_service(db, friend_data)


@router.get("/", response_model=list[FriendsResponse])  # Nouveau endpoint
def get_all_friends(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all friendships.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[FriendsResponse]: A list of all friendships.

    Raises:
        HTTPException: If an error occurs while fetching the friendships (optional, if implemented).
    """
    return get_all_friends_service(db)


@router.get("/{friend_id}", response_model=FriendsResponse, tags=["Friends"], name="Get Friend by id")
def get_friend_by_id(friend_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a specific friendship by its unique ID.

    Args:
        friend_id (UUID): The unique identifier of the friendship to retrieve.
        db (Session): Database session dependency.

    Returns:
        FriendsResponse: The retrieved friendship information.

    Raises:
        HTTPException:
            - 404 status code if the friendship is not found.
    """
    return get_friend_service(db, friend_id)



@router.put("/{friend_id}", response_model=FriendsResponse, tags=["Friends"], name="Update Friend")
def update_friend(friend_id: UUID, update_data: FriendsUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing friendship.

    Args:
        friend_id (UUID): The unique identifier of the friendship to be updated.
        update_data (FriendsUpdate): The updated friendship data provided in the request body.
        db (Session): Database session dependency.

    Returns:
        FriendsResponse: The updated friendship information.

    Raises:
        HTTPException:
            - 404 status code if the friendship is not found.
            - 400 status code if the update data is invalid.
    """
    return update_friend_service(db, friend_id, update_data)



@router.delete("/{friend_id}", response_model=FriendsResponse, tags=["Friends"], name="Delete Friend")
def delete_friend(friend_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to delete a friendship.

    Args:
        friend_id (UUID): The unique identifier of the friendship to be deleted.
        db (Session): Database session dependency.

    Returns:
        FriendsResponse: The deleted friendship information.

    Raises:
        HTTPException:
            - 404 status code if the friendship is not found.
    """
    return delete_friend_service(db, friend_id)

