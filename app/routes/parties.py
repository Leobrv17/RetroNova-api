from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data_base import get_db
from schemas import PartyCreate, PartyResponse, PartyUpdate
from services.parties import (
    create_party_service,
    get_all_parties_service,
    get_party_by_id_service,
    update_party_service,
    delete_party_service,
)
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=PartyResponse)
def create_party(party: PartyCreate, db: Session = Depends(get_db)):
    return create_party_service(db, party)

@router.get("/", response_model=list[PartyResponse])
def get_all_parties(db: Session = Depends(get_db)):
    return get_all_parties_service(db)

@router.get("/{party_id}", response_model=PartyResponse)
def get_party_by_id(party_id: UUID, db: Session = Depends(get_db)):
    return get_party_by_id_service(db, party_id)

@router.put("/{party_id}", response_model=PartyResponse)
def update_party(party_id: UUID, party: PartyUpdate, db: Session = Depends(get_db)):
    return update_party_service(db, party_id, party)

@router.delete("/{party_id}")
def delete_party(party_id: UUID, db: Session = Depends(get_db)):
    return delete_party_service(db, party_id)
