from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.data_base import get_db
from app.schemas import PaymentCreate, PaymentResponse, PaymentUpdate
from app.services.payments import (
    create_payment_service,
    get_all_payments_service,
    get_payment_by_id_service,
    update_payment_service,
    delete_payment_service,
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
def get_all_payments(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all payments.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[PaymentResponse]: A list of all payments.

    Raises:
        HTTPException: If an error occurs while fetching the payments (optional, if implemented).
    """
    return get_all_payments_service(db)


@router.get("/{payment_id}", response_model=PaymentResponse, tags=["Payments"], name="Get Payments by id")
def get_payment_by_id(payment_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a payment by its unique ID.

    Args:
        payment_id (UUID): The unique identifier of the payment to retrieve.
        db (Session): Database session dependency.

    Returns:
        PaymentResponse: The retrieved payment's information.

    Raises:
        HTTPException:
            - 404 status code if the payment is not found.
    """
    return get_payment_by_id_service(db, payment_id)


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
def delete_payment(payment_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint to delete an existing payment.

    Args:
        payment_id (UUID): The unique identifier of the payment to be deleted.
        db (Session): Database session dependency.

    Returns:
        dict: A message confirming the deletion of the payment.

    Raises:
        HTTPException: If the payment is not found or the deletion fails.
    """
    return delete_payment_service(db, payment_id)

