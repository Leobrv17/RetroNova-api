from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from app.models import Friends
from app.schemas import FriendsCreate, FriendsUpdate

def create_friend_service(db: Session, friend_data: FriendsCreate):
    """
    Creates a new friendship record in the database.

    Args:
        db (Session): Database session to interact with the database.
        friend_data (FriendsCreate): The data to create a new friendship relationship.

    Returns:
        Friends: The newly created friendship record.

    Raises:
        HTTPException: If the friendship already exists (400 status code).
    """
    # Check if the friendship already exists
    existing_friend = db.query(Friends).filter(
        Friends.friend_from_id == friend_data.friend_from_id,
        Friends.friend_to_id == friend_data.friend_to_id
    ).first()

    if existing_friend:
        raise HTTPException(status_code=400, detail="Friendship already exists")

    # Create the new friendship relationship
    new_friend = Friends(**friend_data.model_dump())
    db.add(new_friend)
    db.commit()
    db.refresh(new_friend)
    return new_friend


def get_friend_by_id_service(db: Session, friend_id: UUID):
    """
    Retrieves a specific friendship by its unique ID.

    Args:
        db (Session): Database session for querying friendship records.
        friend_id (UUID): The unique identifier of the friendship to retrieve.

    Returns:
        Friends: The friendship corresponding to the provided ID.

    Raises:
        HTTPException: If the friendship with the given ID is not found (404 status code).
    """
    friend = db.query(Friends).filter(Friends.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")
    return friend


def get_all_friends_service(db: Session):
    """
    Retrieves all friendship records from the database.

    Args:
        db (Session): Database session for querying friendship records.

    Returns:
        List[Friends]: A list of all friendship records in the database.
    """
    return db.query(Friends).all()


def update_friend_service(db: Session, friend_id: UUID, update_data: FriendsUpdate):
    """
    Updates the details of an existing friendship record.

    Args:
        db (Session): Database session for interacting with the database.
        friend_id (UUID): The unique identifier of the friendship to update.
        update_data (FriendsUpdate): The new data to update the friendship record with.

    Returns:
        Friends: The updated friendship record.

    Raises:
        HTTPException: If the friendship with the given ID is not found (404 status code).
    """
    friend = db.query(Friends).filter(Friends.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    # Update the friendship fields with the new data
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(friend, key, value)

    db.commit()
    db.refresh(friend)
    return friend


def delete_friend_service(db: Session, friend_id: UUID):
    """
    Deletes a friendship record from the database.

    Args:
        db (Session): Database session for interacting with the database.
        friend_id (UUID): The unique identifier of the friendship to delete.

    Returns:
        Friends: The deleted friendship record.

    Raises:
        HTTPException: If the friendship with the given ID is not found (404 status code).
    """
    friend = db.query(Friends).filter(Friends.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    db.delete(friend)
    db.commit()
    return friend

