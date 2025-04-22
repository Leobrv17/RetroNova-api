from sqlalchemy.orm import Session
from app.models import ArcadeMachines
from app.schemas import ArcadeMachineCreate, ArcadeMachineUpdate
from uuid import UUID
from fastapi import HTTPException
from app.utils.db_utils import filter_deleted, soft_delete


def create_arcade_machine_service(db: Session, machine: ArcadeMachineCreate):
    """
    Creates a new arcade machine record in the database.

    Args:
        db (Session): Database session to interact with the database.
        machine (ArcadeMachineCreate): The data to create a new arcade machine.

    Returns:
        ArcadeMachines: The newly created arcade machine record.
    """
    new_machine = ArcadeMachines(**machine.model_dump())
    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)
    return new_machine


def get_all_arcade_machines_service(db: Session, include_deleted: bool = False):
    """
    Retrieves all arcade machine records from the database.

    Args:
        db (Session): Database session for querying arcade machine records.
        include_deleted (bool, optional): If True, include soft-deleted machines. Defaults to False.

    Returns:
        List[ArcadeMachines]: A list of all arcade machine records in the database.
    """
    query = db.query(ArcadeMachines)
    query = filter_deleted(query, include_deleted)
    return query.all()


def get_arcade_machine_by_id_service(db: Session, machine_id: UUID, include_deleted: bool = False):
    """
    Retrieves a specific arcade machine by its unique ID.

    Args:
        db (Session): Database session for querying arcade machine records.
        machine_id (UUID): The unique identifier of the arcade machine to retrieve.
        include_deleted (bool, optional): If True, include soft-deleted machines. Defaults to False.

    Returns:
        ArcadeMachines: The arcade machine corresponding to the provided ID.

    Raises:
        HTTPException: If the arcade machine with the given ID is not found (404 status code).
    """
    query = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id)
    query = filter_deleted(query, include_deleted)
    machine = query.first()

    if not machine:
        raise HTTPException(status_code=404, detail="Arcade machine not found")
    return machine


def update_arcade_machine_service(db: Session, machine_id: UUID, machine_update: ArcadeMachineUpdate):
    """
    Updates the details of an existing arcade machine record.

    Args:
        db (Session): Database session for interacting with the database.
        machine_id (UUID): The unique identifier of the arcade machine to update.
        machine_update (ArcadeMachineUpdate): The new data to update the arcade machine record with.

    Returns:
        ArcadeMachines: The updated arcade machine record.

    Raises:
        HTTPException: If the arcade machine with the given ID is not found (404 status code).
    """
    query = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id)
    query = filter_deleted(query, False)
    machine = query.first()

    if not machine:
        raise HTTPException(status_code=404, detail="Arcade machine not found")

    # Update the arcade machine fields with the new data
    for key, value in machine_update.dict(exclude_unset=True).items():
        setattr(machine, key, value)

    db.commit()
    db.refresh(machine)
    return machine


def delete_arcade_machine_service(db: Session, machine_id: UUID, hard_delete: bool = False):
    """
    Deletes an arcade machine record from the database.

    Args:
        db (Session): Database session for interacting with the database.
        machine_id (UUID): The unique identifier of the arcade machine to delete.
        hard_delete (bool, optional): If True, physically delete the record. Defaults to False.

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the arcade machine with the given ID is not found (404 status code).
    """
    query = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id)
    query = filter_deleted(query, False)
    machine = query.first()

    if not machine:
        raise HTTPException(status_code=404, detail="Arcade machine not found")

    if hard_delete:
        db.delete(machine)
        db.commit()
    else:
        soft_delete(machine, db)

    return {"message": "Arcade machine deleted successfully"}


def restore_arcade_machine_service(db: Session, machine_id: UUID):
    """
    Restores a soft-deleted arcade machine.

    Args:
        db (Session): Database session for interacting with the database.
        machine_id (UUID): The unique identifier of the arcade machine to restore.

    Returns:
        ArcadeMachines: The restored arcade machine record.

    Raises:
        HTTPException:
            - 404: If the arcade machine is not found.
            - 400: If the arcade machine is not deleted.
    """
    machine = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id).first()

    if not machine:
        raise HTTPException(status_code=404, detail="Arcade machine not found")

    if not machine.is_deleted:
        raise HTTPException(status_code=400, detail="Arcade machine is not deleted")

    machine.is_deleted = False
    machine.deleted_at = None
    db.commit()
    db.refresh(machine)

    return machine