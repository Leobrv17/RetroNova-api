from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from uuid import UUID
from app.data_base import get_db
from app.depends.firebase_auth import verify_firebase_token
from app.schemas import FriendsCreate, FriendsResponse, FriendsUpdate
from app.services.friends import (
    create_friend_service,
    get_friend_by_id_service,
    update_friend_service,
    delete_friend_service,
    get_all_friends_service,
    restore_friend_service
)
from app.models import Friends, Users
from app.utils.db_utils import filter_deleted

router = APIRouter()


@router.post("/", response_model=FriendsResponse, tags=["Friends"], name="Create Friend")
def create_friend(
    friend_data: FriendsCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_firebase_token)
):
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
    firebase_uid = current_user.get("uid")
    return create_friend_service(db, friend_data, firebase_uid)


@router.get("/", response_model=list[FriendsResponse], tags=["Friends"], name="Get All Friends")
def get_all_friends(
        include_deleted: bool = Query(False, description="Include soft-deleted friendships"),
        db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve all friendships.

    Args:
        include_deleted (bool, optional): If True, include soft-deleted friendships. Defaults to False.
        db (Session): Database session dependency.

    Returns:
        List[FriendsResponse]: A list of all friendships.

    Raises:
        HTTPException: If an error occurs while fetching the friendships (optional, if implemented).
    """
    return get_all_friends_service(db, include_deleted)


@router.get("/{friend_id}", response_model=FriendsResponse, tags=["Friends"], name="Get Friend by id")
def get_friend_by_id(
        friend_id: UUID,
        include_deleted: bool = Query(False, description="Include soft-deleted friendships"),
        db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve a specific friendship by its unique ID.

    Args:
        friend_id (UUID): The unique identifier of the friendship to retrieve.
        include_deleted (bool, optional): If True, include soft-deleted friendships. Defaults to False.
        db (Session): Database session dependency.

    Returns:
        FriendsResponse: The retrieved friendship information.

    Raises:
        HTTPException:
            - 404 status code if the friendship is not found.
    """
    return get_friend_by_id_service(db, friend_id, include_deleted)


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
def delete_friend(
        friend_id: UUID,
        hard_delete: bool = Query(False, description="Perform hard delete instead of soft delete"),
        db: Session = Depends(get_db)
):
    """
    Endpoint to delete a friendship.

    Args:
        friend_id (UUID): The unique identifier of the friendship to be deleted.
        hard_delete (bool, optional): If True, permanently delete the friendship. Defaults to False (soft delete).
        db (Session): Database session dependency.

    Returns:
        FriendsResponse: The deleted friendship information.

    Raises:
        HTTPException:
            - 404 status code if the friendship is not found.
    """
    return delete_friend_service(db, friend_id, hard_delete)


@router.post("/{friend_id}/restore", response_model=FriendsResponse, tags=["Friends"], name="Restore Deleted Friend")
def restore_friend(friend_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to restore a soft-deleted friendship.

    Args:
        friend_id (UUID): The unique identifier of the friendship to be restored.
        db (Session): Database session dependency.

    Returns:
        FriendsResponse: The restored friendship information.

    Raises:
        HTTPException:
            - 404 status code if the friendship is not found.
            - 400 status code if the friendship is not deleted.
    """
    return restore_friend_service(db, friend_id)


@router.get("/user", response_model=list[FriendsResponse], tags=["Friends"])
def get_user_friends(
        db: Session = Depends(get_db),
        current_user: dict = Depends(verify_firebase_token)
):
    firebase_uid = current_user.get("uid")
    user = db.query(Users).filter(Users.firebase_id == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupérer les amitiés acceptées où l'utilisateur est impliqué
    query = db.query(Friends).filter(
        or_(
            and_(Friends.friend_from_id == user.id, Friends.accept == True),
            and_(Friends.friend_to_id == user.id, Friends.accept == True)
        )
    )
    query = filter_deleted(query, False)
    friendships = query.all()

    if not friendships:
        raise HTTPException(status_code=404, detail="Aucun ami trouvé")

    return friendships


@router.get("/requests/received", response_model=list[FriendsResponse], tags=["Friends"],
            name="Get Received Friend Requests")
def get_received_friend_requests(db: Session = Depends(get_db), user_data: dict = Depends(verify_firebase_token)):
    """
    Endpoint pour récupérer les demandes d'amitié reçues par l'utilisateur connecté.
    """
    firebase_uid = user_data.get("uid")
    user = db.query(Users).filter(Users.firebase_id == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupérer les amitiés où l'utilisateur est le destinataire et qui ne sont pas encore acceptées ou refusées
    query = db.query(Friends).filter(
        and_(
            Friends.friend_to_id == user.id,
            Friends.accept == False,
            Friends.decline == False
        )
    )

    requests = query.all()
    if not requests:
        raise HTTPException(status_code=404, detail="Aucune demande reçue")

    return requests


@router.get("/requests/sent", response_model=list[FriendsResponse], tags=["Friends"])
def get_sent_friend_requests(
        db: Session = Depends(get_db),
        current_user: dict = Depends(verify_firebase_token)
):
    firebase_uid = current_user.get("uid")
    user = db.query(Users).filter(Users.firebase_id == firebase_uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Récupérer les demandes envoyées non acceptées/refusées
    query = db.query(Friends).filter(
        and_(
            Friends.friend_from_id == user.id,
            Friends.accept == False,
            Friends.decline == False
        )
    )
    query = filter_deleted(query, False)
    requests = query.all()

    if not requests:
        raise HTTPException(status_code=404, detail="Aucune demande envoyée")

    return requests
