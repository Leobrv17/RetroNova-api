import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from unittest.mock import patch
from app.depends.firebase_auth import verify_firebase_token


# ✅ Test : Token Firebase valide
@patch("firebase_admin.auth.verify_id_token")
def test_verify_firebase_token_valid(mock_verify):
    """ Vérifie qu'un token valide est bien authentifié """
    mock_verify.return_value = {"uid": "12345"}  # Simule une réponse Firebase

    fake_credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_token")

    result = verify_firebase_token(fake_credentials)

    assert result == {"uid": "12345"}  # Vérifie que l'UID est retourné


# ❌ Test : Token Firebase invalide
@patch("firebase_admin.auth.verify_id_token", side_effect=Exception("Token non valide"))
def test_verify_firebase_token_invalid(mock_verify):
    """ Vérifie qu'un token invalide déclenche une erreur 401 """
    fake_credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")

    with pytest.raises(HTTPException) as exc_info:
        verify_firebase_token(fake_credentials)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid or expired token"
