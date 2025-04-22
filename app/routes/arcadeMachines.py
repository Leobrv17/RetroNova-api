from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.data_base import get_db
from app.schemas import ArcadeMachineCreate, ArcadeMachineResponse, ArcadeMachineUpdate
from app.services.arcadeMachines import (
    create_arcade_machine_service,
    get_all_arcade_machines_service,
    get_arcade_machine_by_id_service,
    update_arcade_machine_service,
    delete_arcade_machine_service,
)
from app.models import ArcadeMachines
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=ArcadeMachineResponse, tags=["Arcade_Machines"], name="Create Arcade Machines")
def create_arcade_machine(machine: ArcadeMachineCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new arcade machine.

    Args:
        machine (ArcadeMachineCreate): The data required to create a new arcade machine, provided in the request body.
        db (Session): Database session dependency.

    Returns:
        ArcadeMachineResponse: The newly created arcade machine's information.

    Raises:
        HTTPException:
            - 400 status code if a machine with the same specifications already exists.
    """
    return create_arcade_machine_service(db, machine)


@router.get("/", response_model=list[ArcadeMachineResponse], tags=["Arcade_Machines"], name="Get Arcade Machines")
def get_all_arcade_machines(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all arcade machines.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[ArcadeMachineResponse]: A list of all arcade machines.

    Raises:
        HTTPException: If an error occurs while fetching the arcade machines (optional, if implemented).
    """
    return get_all_arcade_machines_service(db)


@router.get("/{machine_id}", response_model=ArcadeMachineResponse, tags=["Arcade_Machines"], name="Get Arcade Machines by id")
def get_arcade_machine_by_id(machine_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a specific arcade machine by its unique ID.

    Args:
        machine_id (UUID): The unique identifier of the arcade machine to retrieve.
        db (Session): Database session dependency.

    Returns:
        ArcadeMachineResponse: The retrieved arcade machine information.

    Raises:
        HTTPException:
            - 404 status code if the arcade machine is not found.
    """
    return get_arcade_machine_by_id_service(db, machine_id)


@router.put("/{machine_id}", response_model=ArcadeMachineResponse, tags=["Arcade_Machines"], name="Update Arcade Machines")
def update_arcade_machine(machine_id: UUID, machine: ArcadeMachineUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing arcade machine.

    Args:
        machine_id (UUID): The unique identifier of the arcade machine to be updated.
        machine (ArcadeMachineUpdate): The updated arcade machine data provided in the request body.
        db (Session): Database session dependency.

    Returns:
        ArcadeMachineResponse: The updated arcade machine information.

    Raises:
        HTTPException:
            - 404 status code if the arcade machine is not found.
            - 400 status code if the update data is invalid.
    """
    return update_arcade_machine_service(db, machine_id, machine)


@router.delete("/{machine_id}", tags=["Arcade_Machines"], name="Delete Arcade Machines")
def delete_arcade_machine(machine_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to delete an existing arcade machine.

    Args:
        machine_id (UUID): The unique identifier of the arcade machine to be deleted.
        db (Session): Database session dependency.

    Returns:
        dict: A confirmation message that the arcade machine has been deleted.

    Raises:
        HTTPException:
            - 404 status code if the arcade machine is not found.
    """
    return delete_arcade_machine_service(db, machine_id)


@router.get("/{machine_id}/games", tags=["Arcade_Machines"], name="Get Games by Arcade Machine ID")
def get_games_by_arcade_id(machine_id: UUID, db: Session = Depends(get_db)):
    arcade = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id).first()

    if not arcade:
        raise HTTPException(status_code=404, detail="Arcade machine not found")

    return {
        "name" : arcade.name if arcade.name else None,
        "game1": arcade.game1.name if arcade.game1 else None,
        "game2": arcade.game2.name if arcade.game2 else None
    }