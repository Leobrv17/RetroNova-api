from sqlalchemy.orm import Session
from models import Payments
from schemas import PaymentCreate, PaymentUpdate
from uuid import UUID
from fastapi import HTTPException


def create_payment_service(db: Session, payment: PaymentCreate):
    new_payment = Payments(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


def get_all_payments_service(db: Session):
    return db.query(Payments).all()


def get_payment_by_id_service(db: Session, payment_id: UUID):
    payment = db.query(Payments).filter(Payments.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


def update_payment_service(db: Session, payment_id: UUID, payment_update: PaymentUpdate):
    payment = db.query(Payments).filter(Payments.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    for key, value in payment_update.dict(exclude_unset=True).items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


def delete_payment_service(db: Session, payment_id: UUID):
    payment = db.query(Payments).filter(Payments.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}
