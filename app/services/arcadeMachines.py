from sqlalchemy.orm import Session
from models import ArcadeMachines
from schemas import ArcadeMachineCreate, ArcadeMachineUpdate
from uuid import UUID
from fastapi import HTTPException


def create_arcade_machine_service(db: Session, machine: ArcadeMachineCreate):
    """
    Creates a new arcade machine record in the database.

    Args:
        db (Session): Database session to interact with the database.
        machine (ArcadeMachineCreate): The data to create a new arcade machine.

    Returns:
        ArcadeMachines: The newly created arcade machine record.
    """
    new_machine = ArcadeMachines(**machine.dict())
    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)
    return new_machine



def get_all_arcade_machines_service(db: Session):
    """
    Retrieves all arcade machine records from the database.

    Args:
        db (Session): Database session for querying arcade machine records.

    Returns:
        List[ArcadeMachines]: A list of all arcade machine records in the database.
    """
    return db.query(ArcadeMachines).all()



def get_arcade_machine_by_id_service(db: Session, machine_id: UUID):
    """
    Retrieves a specific arcade machine by its unique ID.

    Args:
        db (Session): Database session for querying arcade machine records.
        machine_id (UUID): The unique identifier of the arcade machine to retrieve.

    Returns:
        ArcadeMachines: The arcade machine corresponding to the provided ID.

    Raises:
        HTTPException: If the arcade machine with the given ID is not found (404 status code).
    """
    machine = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id).first()
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
    machine = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Arcade machine not found")

    # Update the arcade machine fields with the new data
    for key, value in machine_update.dict(exclude_unset=True).items():
        setattr(machine, key, value)

    db.commit()
    db.refresh(machine)
    return machine


def delete_arcade_machine_service(db: Session, machine_id: UUID):
    """
    Deletes an arcade machine record from the database.

    Args:
        db (Session): Database session for interacting with the database.
        machine_id (UUID): The unique identifier of the arcade machine to delete.

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the arcade machine with the given ID is not found (404 status code).
    """
    machine = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Arcade machine not found")

    db.delete(machine)
    db.commit()
    return {"message": "Arcade machine deleted successfully"}
