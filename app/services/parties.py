from sqlalchemy.orm import Session
from app.models import Parties
from app.schemas import PartyCreate, PartyUpdate
from uuid import UUID
from fastapi import HTTPException
from app.utils.db_utils import filter_deleted, soft_delete


def create_party_service(db: Session, party: PartyCreate):
    """
    Creates a new party record in the database.

    Args:
        db (Session): Database session to interact with the database.
        party (PartyCreate): The party data to create a new party.

    Returns:
        Parties: The newly created party record.

    Notes:
        This function adds a new party to the database and commits the transaction.
    """
    new_party = Parties(**party.model_dump())
    db.add(new_party)
    db.commit()
    db.refresh(new_party)
    return new_party


def get_all_parties_service(db: Session, include_deleted: bool = False):
    """
    Retrieves all party records from the database.

    Args:
        db (Session): Database session for querying party records.
        include_deleted (bool, optional): If True, include soft-deleted parties. Defaults to False.

    Returns:
        List[Parties]: A list of all party records in the database.
    """
    query = db.query(Parties)
    query = filter_deleted(query, include_deleted)
    return query.all()


def get_party_by_id_service(db: Session, party_id: UUID, include_deleted: bool = False):
    """
    Retrieves a specific party by its unique ID.

    Args:
        db (Session): Database session for querying party records.
        party_id (UUID): The unique identifier of the party to retrieve.
        include_deleted (bool, optional): If True, include soft-deleted parties. Defaults to False.

    Returns:
        Parties: The party corresponding to the provided ID.

    Raises:
        HTTPException: If the party with the given ID is not found (404 status code).
    """
    query = db.query(Parties).filter(Parties.id == party_id)
    query = filter_deleted(query, include_deleted)
    party = query.first()

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party


def update_party_service(db: Session, party_id: UUID, party_update: PartyUpdate):
    """
    Updates the details of an existing party record.

    Args:
        db (Session): Database session for interacting with the database.
        party_id (UUID): The unique identifier of the party to update.
        party_update (PartyUpdate): The new data to update the party record with.

    Returns:
        Parties: The updated party record.

    Raises:
        HTTPException: If the party with the given ID is not found (404 status code).
    """
    query = db.query(Parties).filter(Parties.id == party_id)
    query = filter_deleted(query, False)
    party = query.first()

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    # Update the party fields with the new data
    for key, value in party_update.dict(exclude_unset=True).items():
        setattr(party, key, value)

    db.commit()
    db.refresh(party)
    return party


def delete_party_service(db: Session, party_id: UUID, hard_delete: bool = False):
    """
    Deletes a party record from the database.

    Args:
        db (Session): Database session for interacting with the database.
        party_id (UUID): The unique identifier of the party to delete.
        hard_delete (bool, optional): If True, physically delete the record. Defaults to False.

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the party with the given ID is not found (404 status code).
    """
    query = db.query(Parties).filter(Parties.id == party_id)
    query = filter_deleted(query, False)
    party = query.first()

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if hard_delete:
        db.delete(party)
        db.commit()
    else:
        soft_delete(party, db)

    return {"message": "Party deleted successfully"}


def restore_party_service(db: Session, party_id: UUID):
    """
    Restores a soft-deleted party.

    Args:
        db (Session): Database session for interacting with the database.
        party_id (UUID): The unique identifier of the party to restore.

    Returns:
        Parties: The restored party record.

    Raises:
        HTTPException:
            - 404: If the party is not found.
            - 400: If the party is not deleted.
    """
    party = db.query(Parties).filter(Parties.id == party_id).first()

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if not party.is_deleted:
        raise HTTPException(status_code=400, detail="Party is not deleted")

    party.is_deleted = False
    party.deleted_at = None
    db.commit()
    db.refresh(party)

    return party