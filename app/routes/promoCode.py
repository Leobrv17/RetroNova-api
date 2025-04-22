from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.data_base import get_db
from app.schemas import PromoCodeCreate, PromoCodeResponse, PromoCodeUpdate, PromoCodeUse, PromoCodeUsageResponse
from app.services.promoCode import (
    create_promo_code_service,
    get_all_promo_codes_service,
    get_promo_code_by_id_service,
    get_promo_code_by_code_service,
    update_promo_code_service,
    delete_promo_code_service,
    use_promo_code_service,
    generate_promo_code
)
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=PromoCodeResponse, tags=["Promo_Codes"], name="Create Promo Code")
def create_promo_code(promo_code: PromoCodeCreate, db: Session = Depends(get_db)):
    """
    Endpoint pour créer un nouveau code promo.

    Args:
        promo_code (PromoCodeCreate): Les données requises pour créer un nouveau code promo, fournies dans le corps de la requête.
        db (Session): Dépendance de session de base de données.

    Returns:
        PromoCodeResponse: Les informations du code promo nouvellement créé.

    Raises:
        HTTPException:
            - Code 400 si un code promo avec le même code existe déjà.
    """
    return create_promo_code_service(db, promo_code)


@router.post("/generate", response_model=PromoCodeResponse, tags=["Promo_Codes"], name="Generate Random Promo Code")
def generate_random_promo_code(
    nb_parties: int = Query(1, gt=0),
    length: int = Query(8, ge=6, le=12),
    db: Session = Depends(get_db)
):
    """
    Endpoint pour générer un code promo aléatoire.

    Args:
        nb_parties (int): Nombre de parties offertes par ce code promo.
        length (int): Longueur du code promo à générer (entre 6 et 12).
        db (Session): Dépendance de session de base de données.

    Returns:
        PromoCodeResponse: Les informations du code promo généré.
    """
    code = generate_promo_code(length)
    promo_data = PromoCodeCreate(code=code, nb_parties=nb_parties)
    return create_promo_code_service(db, promo_data)


@router.get("/", response_model=List[PromoCodeResponse], tags=["Promo_Codes"], name="Get All Promo Codes")
def get_all_promo_codes(
    include_inactive: bool = Query(False, description="Inclure les codes promo inactifs"),
    db: Session = Depends(get_db)
):
    """
    Endpoint pour récupérer tous les codes promo.

    Args:
        include_inactive (bool): Si True, inclut également les codes inactifs.
        db (Session): Dépendance de session de base de données.

    Returns:
        List[PromoCodeResponse]: Une liste de tous les codes promo.
    """
    return get_all_promo_codes_service(db, include_inactive)


@router.get("/{promo_code_id}", response_model=PromoCodeResponse, tags=["Promo_Codes"], name="Get Promo Code by ID")
def get_promo_code_by_id(promo_code_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint pour récupérer un code promo spécifique par son ID.

    Args:
        promo_code_id (UUID): L'identifiant unique du code promo à récupérer.
        db (Session): Dépendance de session de base de données.

    Returns:
        PromoCodeResponse: Les informations du code promo récupéré.

    Raises:
        HTTPException:
            - Code 404 si le code promo n'est pas trouvé.
    """
    return get_promo_code_by_id_service(db, promo_code_id)


@router.get("/code/{code}", response_model=PromoCodeResponse, tags=["Promo_Codes"], name="Get Promo Code by Code")
def get_promo_code_by_code(code: str, db: Session = Depends(get_db)):
    """
    Endpoint pour récupérer un code promo spécifique par son code.

    Args:
        code (str): Le code à rechercher.
        db (Session): Dépendance de session de base de données.

    Returns:
        PromoCodeResponse: Les informations du code promo récupéré.

    Raises:
        HTTPException:
            - Code 404 si le code promo n'est pas trouvé.
    """
    return get_promo_code_by_code_service(db, code)


@router.put("/{promo_code_id}", response_model=PromoCodeResponse, tags=["Promo_Codes"], name="Update Promo Code")
def update_promo_code(promo_code_id: UUID, promo_code: PromoCodeUpdate, db: Session = Depends(get_db)):
    """
    Endpoint pour mettre à jour un code promo existant.

    Args:
        promo_code_id (UUID): L'identifiant unique du code promo à mettre à jour.
        promo_code (PromoCodeUpdate): Les données de mise à jour du code promo fournies dans le corps de la requête.
        db (Session): Dépendance de session de base de données.

    Returns:
        PromoCodeResponse: Les informations du code promo mis à jour.

    Raises:
        HTTPException:
            - Code 404 si le code promo n'est pas trouvé.
            - Code 400 si les données de mise à jour sont invalides.
    """
    return update_promo_code_service(db, promo_code_id, promo_code)


@router.delete("/{promo_code_id}", tags=["Promo_Codes"], name="Delete Promo Code")
def delete_promo_code(promo_code_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint pour supprimer un code promo existant.

    Args:
        promo_code_id (UUID): L'identifiant unique du code promo à supprimer.
        db (Session): Dépendance de session de base de données.

    Returns:
        dict: Un message de confirmation que le code promo a été supprimé.

    Raises:
        HTTPException:
            - Code 404 si le code promo n'est pas trouvé.
    """
    return delete_promo_code_service(db, promo_code_id)


@router.post("/use", response_model=PromoCodeUsageResponse, tags=["Promo_Codes"], name="Use Promo Code")
def use_promo_code(promo_code_use: PromoCodeUse, db: Session = Depends(get_db)):
    """
    Endpoint pour utiliser un code promo et attribuer des tickets à un utilisateur.

    Args:
        promo_code_use (PromoCodeUse): Les données requises pour utiliser un code promo.
        db (Session): Dépendance de session de base de données.

    Returns:
        PromoCodeUsageResponse: Le résultat de l'utilisation du code promo.

    Raises:
        HTTPException:
            - Code 404 si le code promo ou l'utilisateur n'est pas trouvé.
            - Code 400 si le code est inactif, expiré ou a atteint son nombre maximal d'utilisations.
    """
    return use_promo_code_service(db, promo_code_use.code, promo_code_use.user_id)