from sqlalchemy.orm import Session
from models import Parties
from schemas import PartyCreate, PartyUpdate
from uuid import UUID
from fastapi import HTTPException


def create_party_service(db: Session, party: PartyCreate):
    new_party = Parties(**party.dict())
    db.add(new_party)
    db.commit()
    db.refresh(new_party)
    return new_party


def get_all_parties_service(db: Session):
    return db.query(Parties).all()


def get_party_by_id_service(db: Session, party_id: UUID):
    party = db.query(Parties).filter(Parties.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party


def update_party_service(db: Session, party_id: UUID, party_update: PartyUpdate):
    party = db.query(Parties).filter(Parties.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    for key, value in party_update.dict(exclude_unset=True).items():
        setattr(party, key, value)

    db.commit()
    db.refresh(party)
    return party


def delete_party_service(db: Session, party_id: UUID):
    party = db.query(Parties).filter(Parties.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    db.delete(party)
    db.commit()
    return {"message": "Party deleted successfully"}
