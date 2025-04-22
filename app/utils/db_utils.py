from datetime import datetime
from sqlalchemy import or_, and_
from sqlalchemy.orm import Query


def filter_deleted(query: Query, include_deleted: bool = False) -> Query:
    """
    Filtre les éléments supprimés logiquement d'une requête SQLAlchemy.

    Args:
        query (Query): La requête SQLAlchemy à filtrer.
        include_deleted (bool, optional): Si True, inclut également les éléments supprimés logiquement.
            Par défaut à False.

    Returns:
        Query: La requête filtrée.
    """
    if not include_deleted:
        return query.filter(or_(query.column_descriptions[0]['type'].is_deleted.is_(False),
                                query.column_descriptions[0]['type'].is_deleted.is_(None)))
    return query


def soft_delete(db_obj, db):
    """
    Marque un objet comme supprimé logiquement.

    Args:
        db_obj: L'objet de base de données à supprimer logiquement.
        db: La session de base de données.
    """
    db_obj.is_deleted = True
    db_obj.deleted_at = datetime.utcnow()
    db.add(db_obj)
    db.commit()
    return db_obj