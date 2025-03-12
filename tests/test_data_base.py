import os
import pytest
from sqlalchemy.exc import OperationalError
from app.data_base import get_database_url, create_engine_and_session

def test_get_database_url_not_set(monkeypatch):
    """Vérifie que la fonction lève une erreur si DATABASE_URL est manquant."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValueError, match="DATABASE_URL is not set in the environment variables"):
        get_database_url()

def test_get_database_url_set(monkeypatch):
    """Vérifie que la fonction retourne correctement l'URL définie."""
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./test.db")
    assert get_database_url() == "sqlite:///./test.db"

def test_create_engine_with_valid_url():
    """Vérifie que le moteur et la session peuvent être créés avec une URL valide."""
    engine, Session = create_engine_and_session("sqlite:///./test.db")
    assert engine is not None
    assert Session is not None

def test_create_engine_with_invalid_url():
    """Vérifie que SQLAlchemy lève une erreur avec une URL invalide."""
    with pytest.raises(OperationalError):
        engine, Session = create_engine_and_session("postgresql://invalid:invalid@localhost/invalid_db")
        engine.connect()  # Déclenche l'erreur
