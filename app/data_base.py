from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

def get_database_url():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL is not set in the environment variables")  # ← Ligne 11 qui pose problème
    return db_url

DATABASE_URL = get_database_url()

def create_engine_and_session(db_url=None):
    """
    Initialise le moteur et la session SQLAlchemy.
    Permet d'injecter une URL spécifique pour les tests.
    """
    engine = create_engine(db_url or get_database_url())
    return engine, sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialisation de la BDD
engine, SessionLocal = create_engine_and_session()

def get_db():
    """Dépendance pour récupérer une session de la base de données."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
