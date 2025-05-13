from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from app.models import Friends
from app.schemas import FriendsCreate, FriendsUpdate
from app.utils.db_utils import filter_deleted, soft_delete
from app.models import Users


def create_friend_service(db: Session, friend_data: FriendsCreate, current_user_firebase_id: str = None):
    """
    Creates a new friendship record in the database.

    Args:
        db (Session): Database session to interact with the database.
        friend_data (FriendsCreate): The data to create a new friendship relationship.
        current_user_firebase_id (str, optional): Firebase ID of the current user.

    Returns:
        Friends: The newly created friendship record.

    Raises:
        HTTPException: If the friendship already exists (400 status code).
    """
    # Si l'ID Firebase est fourni, récupérer l'ID de l'utilisateur correspondant
    if current_user_firebase_id:
        user = db.query(Users).filter(Users.firebase_id == current_user_firebase_id).first()
        if user:
            friend_data.friend_from_id = user.id

    # Vérifier si l'amitié existe déjà
    query = db.query(Friends).filter(
        Friends.friend_from_id == friend_data.friend_from_id,
        Friends.friend_to_id == friend_data.friend_to_id
    )
    query = filter_deleted(query, True)
    existing_friend = query.first()

    if existing_friend:
        if existing_friend.is_deleted:
            existing_friend.is_deleted = False
            existing_friend.deleted_at = None
            db.commit()
            db.refresh(existing_friend)
            return existing_friend
        else:
            raise HTTPException(status_code=400, detail="Friendship already exists")

    new_friend = Friends(**friend_data.model_dump())
    db.add(new_friend)
    db.commit()
    db.refresh(new_friend)
    return new_friend


def get_friend_by_id_service(db: Session, friend_id: UUID, include_deleted: bool = False):
    """
    Retrieves a specific friendship by its unique ID.

    Args:
        db (Session): Database session for querying friendship records.
        friend_id (UUID): The unique identifier of the friendship to retrieve.
        include_deleted (bool, optional): If True, include soft-deleted friendships. Defaults to False.

    Returns:
        Friends: The friendship corresponding to the provided ID.

    Raises:
        HTTPException: If the friendship with the given ID is not found (404 status code).
    """
    query = db.query(Friends).filter(Friends.id == friend_id)
    query = filter_deleted(query, include_deleted)
    friend = query.first()

    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")
    return friend


def get_all_friends_service(db: Session, include_deleted: bool = False):
    """
    Retrieves all friendship records from the database.

    Args:
        db (Session): Database session for querying friendship records.
        include_deleted (bool, optional): If True, include soft-deleted friendships. Defaults to False.

    Returns:
        List[Friends]: A list of all friendship records in the database.
    """
    query = db.query(Friends)
    query = filter_deleted(query, include_deleted)
    return query.all()


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
    query = db.query(Friends).filter(Friends.id == friend_id)
    query = filter_deleted(query, False)
    friend = query.first()

    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    # Update the friendship fields with the new data
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(friend, key, value)

    db.commit()
    db.refresh(friend)
    return friend


def delete_friend_service(db: Session, friend_id: UUID, hard_delete: bool = False):
    """
    Deletes a friendship record from the database.

    Args:
        db (Session): Database session for interacting with the database.
        friend_id (UUID): The unique identifier of the friendship to delete.
        hard_delete (bool, optional): If True, physically delete the record. Defaults to False.

    Returns:
        Friends: The deleted friendship record or a success message.

    Raises:
        HTTPException: If the friendship with the given ID is not found (404 status code).
    """
    query = db.query(Friends).filter(Friends.id == friend_id)
    query = filter_deleted(query, False)
    friend = query.first()

    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    if hard_delete:
        db.delete(friend)
        db.commit()
    else:
        soft_delete(friend, db)

    return friend


def restore_friend_service(db: Session, friend_id: UUID):
    """
    Restores a soft-deleted friendship.

    Args:
        db (Session): Database session for interacting with the database.
        friend_id (UUID): The unique identifier of the friendship to restore.

    Returns:
        Friends: The restored friendship record.

    Raises:
        HTTPException:
            - 404: If the friendship is not found.
            - 400: If the friendship is not deleted.
    """
    friend = db.query(Friends).filter(Friends.id == friend_id).first()

    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    if not friend.is_deleted:
        raise HTTPException(status_code=400, detail="Friendship is not deleted")

    friend.is_deleted = False
    friend.deleted_at = None
    db.commit()
    db.refresh(friend)

    return friend