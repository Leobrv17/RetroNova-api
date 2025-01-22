from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Configuration de la base de données
DATABASE_URL="postgresql://postgres:postgres@retronova-db:5432/postgres"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance pour récupérer une session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()