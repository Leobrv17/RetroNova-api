from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data_base import get_db
from schemas import ArcadeMachineCreate, ArcadeMachineResponse, ArcadeMachineUpdate
from services.arcadeMachines import (
    create_arcade_machine_service,
    get_all_arcade_machines_service,
    get_arcade_machine_by_id_service,
    update_arcade_machine_service,
    delete_arcade_machine_service,
)
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=ArcadeMachineResponse)
def create_arcade_machine(machine: ArcadeMachineCreate, db: Session = Depends(get_db)):
    return create_arcade_machine_service(db, machine)

@router.get("/", response_model=list[ArcadeMachineResponse])
def get_all_arcade_machines(db: Session = Depends(get_db)):
    return get_all_arcade_machines_service(db)

@router.get("/{machine_id}", response_model=ArcadeMachineResponse)
def get_arcade_machine_by_id(machine_id: UUID, db: Session = Depends(get_db)):
    return get_arcade_machine_by_id_service(db, machine_id)

@router.put("/{machine_id}", response_model=ArcadeMachineResponse)
def update_arcade_machine(machine_id: UUID, machine: ArcadeMachineUpdate, db: Session = Depends(get_db)):
    return update_arcade_machine_service(db, machine_id, machine)

@router.delete("/{machine_id}")
def delete_arcade_machine(machine_id: UUID, db: Session = Depends(get_db)):
    return delete_arcade_machine_service(db, machine_id)
