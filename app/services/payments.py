from sqlalchemy.orm import Session
from app.models import Payments
from app.schemas import PaymentCreate, PaymentUpdate
from uuid import UUID
from fastapi import HTTPException
from app.utils.db_utils import filter_deleted, soft_delete


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
    new_payment = Payments(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


def get_all_payments_service(db: Session, include_deleted: bool = False):
    """
    Retrieves all payment records from the database.

    Args:
        db (Session): Database session for querying payment records.
        include_deleted (bool, optional): If True, include soft-deleted payments. Defaults to False.

    Returns:
        List[Payments]: A list of all payment records in the database.
    """
    query = db.query(Payments)
    query = filter_deleted(query, include_deleted)
    return query.all()


def get_payment_by_id_service(db: Session, payment_id: UUID, include_deleted: bool = False):
    """
    Retrieves a specific payment by its unique ID.

    Args:
        db (Session): Database session for querying payment records.
        payment_id (UUID): The unique identifier of the payment to retrieve.
        include_deleted (bool, optional): If True, include soft-deleted payments. Defaults to False.

    Returns:
        Payments: The payment corresponding to the provided ID.

    Raises:
        HTTPException: If the payment with the given ID is not found (404 status code).
    """
    query = db.query(Payments).filter(Payments.id == payment_id)
    query = filter_deleted(query, include_deleted)
    payment = query.first()

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
    query = db.query(Payments).filter(Payments.id == payment_id)
    query = filter_deleted(query, False)
    payment = query.first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    # Update the payment fields with the new data
    for key, value in payment_update.dict(exclude_unset=True).items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


def delete_payment_service(db: Session, payment_id: UUID, hard_delete: bool = False):
    """
    Deletes a payment record from the database.

    Args:
        db (Session): Database session for interacting with the database.
        payment_id (UUID): The unique identifier of the payment to delete.
        hard_delete (bool, optional): If True, physically delete the record. Defaults to False.

    Returns:
        dict: A success message upon successful deletion.

    Raises:
        HTTPException: If the payment with the given ID is not found (404 status code).
    """
    query = db.query(Payments).filter(Payments.id == payment_id)
    query = filter_deleted(query, False)
    payment = query.first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if hard_delete:
        db.delete(payment)
        db.commit()
    else:
        soft_delete(payment, db)

    return {"message": "Payment deleted successfully"}


def restore_payment_service(db: Session, payment_id: UUID):
    """
    Restores a soft-deleted payment.

    Args:
        db (Session): Database session for interacting with the database.
        payment_id (UUID): The unique identifier of the payment to restore.

    Returns:
        Payments: The restored payment record.

    Raises:
        HTTPException:
            - 404: If the payment is not found.
            - 400: If the payment is not deleted.
    """
    payment = db.query(Payments).filter(Payments.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if not payment.is_deleted:
        raise HTTPException(status_code=400, detail="Payment is not deleted")

    payment.is_deleted = False
    payment.deleted_at = None
    db.commit()
    db.refresh(payment)

    return payment