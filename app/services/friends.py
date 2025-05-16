from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from app.models import Friends
from app.schemas import FriendsCreate, FriendsUpdate
from app.utils.db_utils import filter_deleted, soft_delete


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
    # Check if the friendship already exists (same direction)
    query = db.query(Friends).filter(
        Friends.friend_from_id == friend_data.friend_from_id,
        Friends.friend_to_id == friend_data.friend_to_id
    )
    query = filter_deleted(query, True)  # Inclure même les amitiés supprimées pour détecter les doublons
    existing_friend = query.first()

    if existing_friend:
        if existing_friend.is_deleted:
            # Si l'amitié existe mais est supprimée, on la restaure
            existing_friend.is_deleted = False
            existing_friend.deleted_at = None
            db.commit()
            db.refresh(existing_friend)
            return existing_friend
        else:
            raise HTTPException(status_code=400, detail="Friendship already exists")

    # Check if a reverse friendship already exists (opposite direction)
    reverse_query = db.query(Friends).filter(
        Friends.friend_from_id == friend_data.friend_to_id,
        Friends.friend_to_id == friend_data.friend_from_id
    )
    reverse_query = filter_deleted(reverse_query, True)  # Inclure même les amitiés supprimées
    reverse_friendship = reverse_query.first()

    if reverse_friendship:
        # Une amitié dans le sens inverse existe déjà
        if reverse_friendship.is_deleted:
            # Si l'amitié inverse est supprimée, on pourrait la restaurer ou refuser
            # Ici on choisit de refuser pour des raisons de cohérence
            raise HTTPException(
                status_code=400,
                detail="A friendship request already exists in the opposite direction"
            )
        else:
            # L'amitié inverse existe et n'est pas supprimée
            raise HTTPException(
                status_code=400,
                detail="A friendship request already exists from the other user"
            )

    # Create the new friendship relationship
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

def get_friends_from_service(db: Session, user_id: UUID, include_deleted: bool = False):
    """
    Récupère toutes les amitiés initiées par un utilisateur spécifique.

    Args:
        db (Session): Session de base de données pour les requêtes.
        user_id (UUID): L'identifiant unique de l'utilisateur qui a initié les demandes d'amitié.
        include_deleted (bool, optional): Si True, inclut les amitiés supprimées logiquement.
                                          Defaults to False.

    Returns:
        List[Friends]: Une liste de toutes les amitiés initiées par l'utilisateur.
    """
    query = db.query(Friends).filter(Friends.friend_from_id == user_id)
    query = filter_deleted(query, include_deleted)
    return query.all()


def get_friends_to_service(db: Session, user_id: UUID, include_deleted: bool = False):
    """
    Récupère toutes les amitiés reçues par un utilisateur spécifique.

    Args:
        db (Session): Session de base de données pour les requêtes.
        user_id (UUID): L'identifiant unique de l'utilisateur qui a reçu les demandes d'amitié.
        include_deleted (bool, optional): Si True, inclut les amitiés supprimées logiquement.
                                          Defaults to False.

    Returns:
        List[Friends]: Une liste de toutes les amitiés reçues par l'utilisateur.
    """
    query = db.query(Friends).filter(Friends.friend_to_id == user_id)
    query = filter_deleted(query, include_deleted)
    return query.all()


def get_all_user_friends_service(db: Session, user_id: UUID, include_deleted: bool = False):
    """
    Récupère toutes les amitiés d'un utilisateur (initiées ET reçues).

    Args:
        db (Session): Session de base de données pour les requêtes.
        user_id (UUID): L'identifiant unique de l'utilisateur.
        include_deleted (bool, optional): Si True, inclut les amitiés supprimées logiquement.
                                          Defaults to False.

    Returns:
        List[Friends]: Une liste de toutes les amitiés de l'utilisateur.
    """
    query = db.query(Friends).filter(
        (Friends.friend_from_id == user_id) | (Friends.friend_to_id == user_id)
    )
    query = filter_deleted(query, include_deleted)
    return query.all()


def get_friends_by_status_service(
        db: Session,
        user_id: UUID,
        accepted: bool = None,
        declined: bool = None,
        include_deleted: bool = False
):
    """
    Récupère les amitiés d'un utilisateur filtrées par statut.

    Args:
        db (Session): Session de base de données pour les requêtes.
        user_id (UUID): L'identifiant unique de l'utilisateur.
        accepted (bool, optional): Filtrer par demandes acceptées.
                                   None = pas de filtre sur ce champ.
        declined (bool, optional): Filtrer par demandes refusées.
                                   None = pas de filtre sur ce champ.
        include_deleted (bool, optional): Si True, inclut les amitiés supprimées logiquement.
                                          Defaults to False.

    Returns:
        List[Friends]: Une liste des amitiés filtrées.
    """
    # Requête de base pour toutes les amitiés impliquant cet utilisateur
    query = db.query(Friends).filter(
        (Friends.friend_from_id == user_id) | (Friends.friend_to_id == user_id)
    )

    # Filtrer par statut accepté
    if accepted is not None:
        query = query.filter(Friends.accept == accepted)

    # Filtrer par statut refusé
    if declined is not None:
        query = query.filter(Friends.decline == declined)

    # Filtre de suppression logique
    query = filter_deleted(query, include_deleted)

    return query.all()


def get_pending_friends_service(db: Session, user_id: UUID, include_deleted: bool = False):
    """
    Récupère les demandes d'amitié en attente pour un utilisateur.

    Args:
        db (Session): Session de base de données pour les requêtes.
        user_id (UUID): L'identifiant unique de l'utilisateur.
        include_deleted (bool, optional): Si True, inclut les amitiés supprimées logiquement.
                                          Defaults to False.

    Returns:
        List[Friends]: Une liste des demandes d'amitié en attente.
    """
    query = db.query(Friends).filter(
        (Friends.friend_to_id == user_id) &  # Demandes reçues
        (Friends.accept == False) &  # Non acceptées
        (Friends.decline == False)  # Non refusées
    )

    query = filter_deleted(query, include_deleted)
    return query.all()