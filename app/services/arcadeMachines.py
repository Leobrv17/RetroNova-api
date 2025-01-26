from sqlalchemy.orm import Session
from models import ArcadeMachines
from schemas import ArcadeMachineCreate, ArcadeMachineUpdate
from uuid import UUID
from fastapi import HTTPException


def create_arcade_machine_service(db: Session, machine: ArcadeMachineCreate):
    new_machine = ArcadeMachines(**machine.dict())
    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)
    return new_machine


def get_all_arcade_machines_service(db: Session):
    return db.query(ArcadeMachines).all()


def get_arcade_machine_by_id_service(db: Session, machine_id: UUID):
    machine = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Arcade machine not found")
    return machine


def update_arcade_machine_service(db: Session, machine_id: UUID, machine_update: ArcadeMachineUpdate):
    machine = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Arcade machine not found")

    for key, value in machine_update.dict(exclude_unset=True).items():
        setattr(machine, key, value)

    db.commit()
    db.refresh(machine)
    return machine


def delete_arcade_machine_service(db: Session, machine_id: UUID):
    machine = db.query(ArcadeMachines).filter(ArcadeMachines.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Arcade machine not found")
    db.delete(machine)
    db.commit()
    return {"message": "Arcade machine deleted successfully"}
