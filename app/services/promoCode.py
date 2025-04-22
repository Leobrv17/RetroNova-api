from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import PromoCodes, Users
from app.schemas import PromoCodeCreate, PromoCodeUpdate
from datetime import datetime
from uuid import UUID
import string
import random


def generate_promo_code(length=8):
    """Génère un code promo aléatoire alphanumérique."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def create_promo_code_service(db: Session, promo_code: PromoCodeCreate):
    """
    Crée un nouveau code promo dans la base de données.

    Args:
        db (Session): Session de base de données pour interagir avec la BDD.
        promo_code (PromoCodeCreate): Les données pour créer un nouveau code promo.

    Returns:
        PromoCodes: Le code promo nouvellement créé.

    Raises:
        HTTPException: Si un code promo avec le même code existe déjà.
    """
    # Vérifier si le code existe déjà
    db_code = db.query(PromoCodes).filter(PromoCodes.code == promo_code.code).first()
    if db_code:
        raise HTTPException(status_code=400, detail="Un code promo avec ce code existe déjà")

    new_promo_code = PromoCodes(**promo_code.model_dump())
    db.add(new_promo_code)
    db.commit()
    db.refresh(new_promo_code)
    return new_promo_code


def get_all_promo_codes_service(db: Session, include_inactive: bool = False):
    """
    Récupère tous les codes promo de la base de données.

    Args:
        db (Session): Session de base de données pour les requêtes.
        include_inactive (bool): Si True, inclut également les codes inactifs.

    Returns:
        List[PromoCodes]: Une liste de tous les codes promo.
    """
    query = db.query(PromoCodes)
    if not include_inactive:
        query = query.filter(PromoCodes.is_active == True)
    return query.all()


def get_promo_code_by_id_service(db: Session, promo_code_id: UUID):
    """
    Récupère un code promo spécifique par son ID.

    Args:
        db (Session): Session de base de données pour les requêtes.
        promo_code_id (UUID): L'identifiant unique du code promo à récupérer.

    Returns:
        PromoCodes: Le code promo correspondant à l'ID fourni.

    Raises:
        HTTPException: Si le code promo avec l'ID donné n'est pas trouvé.
    """
    promo_code = db.query(PromoCodes).filter(PromoCodes.id == promo_code_id).first()
    if not promo_code:
        raise HTTPException(status_code=404, detail="Code promo non trouvé")
    return promo_code


def get_promo_code_by_code_service(db: Session, code: str):
    """
    Récupère un code promo spécifique par son code.

    Args:
        db (Session): Session de base de données pour les requêtes.
        code (str): Le code à rechercher.

    Returns:
        PromoCodes: Le code promo correspondant au code fourni.

    Raises:
        HTTPException: Si le code promo n'est pas trouvé.
    """
    promo_code = db.query(PromoCodes).filter(PromoCodes.code == code.upper()).first()
    if not promo_code:
        raise HTTPException(status_code=404, detail="Code promo non trouvé")
    return promo_code


def update_promo_code_service(db: Session, promo_code_id: UUID, promo_code_update: PromoCodeUpdate):
    """
    Met à jour les détails d'un code promo existant.

    Args:
        db (Session): Session de base de données pour interagir avec la BDD.
        promo_code_id (UUID): L'identifiant unique du code promo à mettre à jour.
        promo_code_update (PromoCodeUpdate): Les nouvelles données pour mettre à jour le code promo.

    Returns:
        PromoCodes: Le code promo mis à jour.

    Raises:
        HTTPException: Si le code promo avec l'ID donné n'est pas trouvé ou si la mise à jour échoue.
    """
    promo_code = db.query(PromoCodes).filter(PromoCodes.id == promo_code_id).first()
    if not promo_code:
        raise HTTPException(status_code=404, detail="Code promo non trouvé")

    # Vérifier si le nouveau code est déjà utilisé par un autre code promo
    if promo_code_update.code is not None and promo_code_update.code != promo_code.code:
        existing_code = db.query(PromoCodes).filter(PromoCodes.code == promo_code_update.code).first()
        if existing_code:
            raise HTTPException(status_code=400, detail="Un code promo avec ce code existe déjà")

    # Mettre à jour les champs du code promo avec les nouvelles données
    update_data = promo_code_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(promo_code, key, value)

    db.commit()
    db.refresh(promo_code)
    return promo_code


def delete_promo_code_service(db: Session, promo_code_id: UUID):
    """
    Supprime un code promo de la base de données.

    Args:
        db (Session): Session de base de données pour interagir avec la BDD.
        promo_code_id (UUID): L'identifiant unique du code promo à supprimer.

    Returns:
        dict: Un message de confirmation après suppression réussie.

    Raises:
        HTTPException: Si le code promo avec l'ID donné n'est pas trouvé.
    """
    promo_code = db.query(PromoCodes).filter(PromoCodes.id == promo_code_id).first()
    if not promo_code:
        raise HTTPException(status_code=404, detail="Code promo non trouvé")

    db.delete(promo_code)
    db.commit()
    return {"message": "Code promo supprimé avec succès"}


def use_promo_code_service(db: Session, code: str, user_id: UUID):
    """
    Utilise un code promo pour un utilisateur spécifique.

    Args:
        db (Session): Session de base de données pour interagir avec la BDD.
        code (str): Le code promo à utiliser.
        user_id (UUID): L'ID de l'utilisateur qui utilise le code.

    Returns:
        dict: Résultat de l'utilisation du code promo.

    Raises:
        HTTPException: Si le code est invalide, expiré, ou déjà utilisé trop de fois.
    """
    # Récupérer le code promo
    promo_code = db.query(PromoCodes).filter(PromoCodes.code == code.upper()).first()
    if not promo_code:
        raise HTTPException(status_code=404, detail="Code promo invalide")

    # Vérifier si le code est actif
    if not promo_code.is_active:
        raise HTTPException(status_code=400, detail="Ce code promo n'est plus actif")

    # Vérifier si le code a expiré
    if promo_code.expires_at and promo_code.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Ce code promo a expiré")

    # Vérifier le nombre d'utilisations maximal
    if promo_code.max_uses and promo_code.used_count >= promo_code.max_uses:
        raise HTTPException(status_code=400, detail="Ce code promo a atteint son nombre maximal d'utilisations")

    # Récupérer l'utilisateur
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Ajouter les tickets à l'utilisateur
    user.nb_ticket += promo_code.nb_parties

    # Incrémenter le compteur d'utilisation du code
    promo_code.used_count += 1

    # Mettre à jour la base de données
    db.commit()

    return {
        "success": True,
        "message": f"Code promo utilisé avec succès! {promo_code.nb_parties} tickets ajoutés à votre compte.",
        "nb_parties": promo_code.nb_parties
    }