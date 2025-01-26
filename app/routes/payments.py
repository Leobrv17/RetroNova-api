from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data_base import get_db
from schemas import PaymentCreate, PaymentResponse, PaymentUpdate
from services.payments import (
    create_payment_service,
    get_all_payments_service,
    get_payment_by_id_service,
    update_payment_service,
    delete_payment_service,
)
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return create_payment_service(db, payment)

@router.get("/", response_model=list[PaymentResponse])
def get_all_payments(db: Session = Depends(get_db)):
    return get_all_payments_service(db)

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment_by_id(payment_id: UUID, db: Session = Depends(get_db)):
    return get_payment_by_id_service(db, payment_id)

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: UUID, payment: PaymentUpdate, db: Session = Depends(get_db)):
    return update_payment_service(db, payment_id, payment)

@router.delete("/{payment_id}")
def delete_payment(payment_id: UUID, db: Session = Depends(get_db)):
    return delete_payment_service(db, payment_id)
