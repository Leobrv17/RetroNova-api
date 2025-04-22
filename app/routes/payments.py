from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.data_base import get_db
from app.schemas import PaymentCreate, PaymentResponse, PaymentUpdate
from app.services.payments import (
    create_payment_service,
    get_all_payments_service,
    get_payment_by_id_service,
    update_payment_service,
    delete_payment_service,
    restore_payment_service
)
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=PaymentResponse, tags=["Payments"], name="Create Payments")
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new payment.

    Args:
        payment (PaymentCreate): The data required to create a new payment, provided in the request body.
        db (Session): Database session dependency.

    Returns:
        PaymentResponse: The newly created payment's information.

    Raises:
        HTTPException:
            - 400 status code if the payment creation fails due to invalid input or other validation errors.
    """
    return create_payment_service(db, payment)


@router.get("/", response_model=list[PaymentResponse], tags=["Payments"], name="Get Payments")
def get_all_payments(
    include_deleted: bool = Query(False, description="Include soft-deleted payments"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve all payments.

    Args:
        include_deleted (bool, optional): If True, include soft-deleted payments. Defaults to False.
        db (Session): Database session dependency.

    Returns:
        List[PaymentResponse]: A list of all payments.

    Raises:
        HTTPException: If an error occurs while fetching the payments (optional, if implemented).
    """
    return get_all_payments_service(db, include_deleted)


@router.get("/{payment_id}", response_model=PaymentResponse, tags=["Payments"], name="Get Payments by id")
def get_payment_by_id(
    payment_id: UUID,
    include_deleted: bool = Query(False, description="Include soft-deleted payments"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve a payment by its unique ID.

    Args:
        payment_id (UUID): The unique identifier of the payment to retrieve.
        include_deleted (bool, optional): If True, include soft-deleted payments. Defaults to False.
        db (Session): Database session dependency.

    Returns:
        PaymentResponse: The retrieved payment's information.

    Raises:
        HTTPException:
            - 404 status code if the payment is not found.
    """
    return get_payment_by_id_service(db, payment_id, include_deleted)


@router.put("/{payment_id}", response_model=PaymentResponse, tags=["Payments"], name="Update Payments")
def update_payment(payment_id: UUID, payment: PaymentUpdate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing payment.

    Args:
        payment_id (UUID): The unique identifier of the payment to be updated.
        payment (PaymentUpdate): The updated payment data provided in the request body.
        db (Session): Database session dependency.

    Returns:
        PaymentResponse: The updated payment's information.

    Raises:
        HTTPException: If the payment is not found or the update fails.
    """
    return update_payment_service(db, payment_id, payment)


@router.delete("/{payment_id}", tags=["Payments"], name="Delete Payments")
def delete_payment(
    payment_id: UUID,
    hard_delete: bool = Query(False, description="Perform hard delete instead of soft delete"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to delete an existing payment.

    Args:
        payment_id (UUID): The unique identifier of the payment to be deleted.
        hard_delete (bool, optional): If True, permanently delete the payment. Defaults to False (soft delete).
        db (Session): Database session dependency.

    Returns:
        dict: A message confirming the deletion of the payment.

    Raises:
        HTTPException: If the payment is not found or the deletion fails.
    """
    return delete_payment_service(db, payment_id, hard_delete)


@router.post("/{payment_id}/restore", response_model=PaymentResponse, tags=["Payments"], name="Restore Deleted Payment")
def restore_payment(payment_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to restore a soft-deleted payment.

    Args:
        payment_id (UUID): The unique identifier of the payment to be restored.
        db (Session): Database session dependency.

    Returns:
        PaymentResponse: The restored payment's information.

    Raises:
        HTTPException:
            - 404 status code if the payment is not found.
            - 400 status code if the payment is not deleted.
    """
    return restore_payment_service(db, payment_id)