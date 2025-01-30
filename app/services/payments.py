from sqlalchemy.orm import Session
from app.models import Payments
from app.schemas import PaymentCreate, PaymentUpdate
from uuid import UUID
from fastapi import HTTPException


def create_payment_service(db: Session, payment: PaymentCreate):
    """
    Creates a new payment record in the database.

    Args:
        db (Session): Database session to interact with the database.
        payment (PaymentCreate): The payment data to create a new payment.

    Returns:
        Payments: The newly created payment record.

    Notes:
        This function adds a new payment to the database and commits the transaction.
    """
    new_payment = Payments(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment



def get_all_payments_service(db: Session):
    """
    Retrieves all payment records from the database.

    Args:
        db (Session): Database session for querying payment records.

    Returns:
        List[Payments]: A list of all payment records in the database.
    """
    return db.query(Payments).all()



def get_payment_by_id_service(db: Session, payment_id: UUID):
    """
    Retrieves a specific payment by its unique ID.

    Args:
        db (Session): Database session for querying payment records.
        payment_id (UUID): The unique identifier of the payment to retrieve.

    Returns:
        Payments: The payment corresponding to the provided ID.

    Raises:
        HTTPException: If the payment with the given ID is not found (404 status code).
    """
    payment = db.query(Payments).filter(Payments.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment



def update_payment_service(db: Session, payment_id: UUID, payment_update: PaymentUpdate):
    """
    Updates the details of an existing payment record.

    Args:
        db (Session): Database session for interacting with the database.
        payment_id (UUID): The unique identifier of the payment to update.
        payment_update (PaymentUpdate): The new data to update the payment record with.

    Returns:
        Payments: The updated payment record.

    Raises:
        HTTPException: If the payment with the given ID is not found (404 status code).
    """
    payment = db.query(Payments).filter(Payments.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    # Update the payment fields with the new data
    for key, value in payment_update.dict(exclude_unset=True).items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


def delete_payment_service(db: Session, payment_id: UUID):
    """
    Deletes a payment record from the database.

    Args:
        db (Session): Database session for interacting with the database.
        payment_id (UUID): The unique identifier of the payment to delete.

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the payment with the given ID is not found (404 status code).
    """
    payment = db.query(Payments).filter(Payments.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}

