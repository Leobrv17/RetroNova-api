from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.data_base import get_db
from app.schemas import PartyCreate, PartyResponse, PartyUpdate
from app.services.parties import (
    create_party_service,
    get_all_parties_service,
    get_party_by_id_service,
    update_party_service,
    delete_party_service,
    restore_party_service
)
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=PartyResponse, tags=["Parties"], name="Create Parties")
def create_party(party: PartyCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new party.

    Args:
        party (PartyCreate): The data required to create a new party, provided in the request body.
        db (Session): Database session dependency.

    Returns:
        PartyResponse: The newly created party's information.

    Raises:
        HTTPException:
            - 400 status code if the party creation fails due to invalid input or other validation errors.
    """
    return create_party_service(db, party)


@router.get("/", response_model=list[PartyResponse], tags=["Parties"], name="Get all Parties")
def get_all_parties(
    include_deleted: bool = Query(False, description="Include soft-deleted parties"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve all parties.

    Args:
        include_deleted (bool, optional): If True, include soft-deleted parties. Defaults to False.
        db (Session): Database session dependency.

    Returns:
        List[PartyResponse]: A list of all parties.

    Raises:
        HTTPException: If an error occurs while fetching the parties (optional, if implemented).
    """
    return get_all_parties_service(db, include_deleted)


@router.get("/{party_id}", response_model=PartyResponse, tags=["Parties"], name="Get Parties By Id")
def get_party_by_id(
    party_id: UUID,
    include_deleted: bool = Query(False, description="Include soft-deleted parties"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve a party by its unique ID.

    Args:
        party_id (UUID): The unique identifier of the party to retrieve.
        include_deleted (bool, optional): If True, include soft-deleted parties. Defaults to False.
        db (Session): Database session dependency.

    Returns:
        PartyResponse: The retrieved party's information.

    Raises:
        HTTPException:
            - 404 status code if the party is not found.
    """
    return get_party_by_id_service(db, party_id, include_deleted)


@router.put("/{party_id}", response_model=PartyResponse, tags=["Parties"], name="Update Parties")
def update_party(party_id: UUID, party: PartyUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing party.

    Args:
        party_id (UUID): The unique identifier of the party to be updated.
        party (PartyUpdate): The updated party data provided in the request body.
        db (Session): Database session dependency.

    Returns:
        PartyResponse: The updated party's information.

    Raises:
        HTTPException: If the party is not found or the update fails.
    """
    return update_party_service(db, party_id, party)


@router.delete("/{party_id}", tags=["Parties"], name="Delete Parties")
def delete_party(
    party_id: UUID,
    hard_delete: bool = Query(False, description="Perform hard delete instead of soft delete"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to delete an existing party.

    Args:
        party_id (UUID): The unique identifier of the party to be deleted.
        hard_delete (bool, optional): If True, permanently delete the party. Defaults to False (soft delete).
        db (Session): Database session dependency.

    Returns:
        dict: A message confirming the deletion of the party.

    Raises:
        HTTPException: If the party is not found or the deletion fails.
    """
    return delete_party_service(db, party_id, hard_delete)


@router.post("/{party_id}/restore", response_model=PartyResponse, tags=["Parties"], name="Restore Deleted Party")
def restore_party(party_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to restore a soft-deleted party.

    Args:
        party_id (UUID): The unique identifier of the party to be restored.
        db (Session): Database session dependency.

    Returns:
        PartyResponse: The restored party's information.

    Raises:
        HTTPException:
            - 404 status code if the party is not found.
            - 400 status code if the party is not deleted.
    """
    return restore_party_service(db, party_id)