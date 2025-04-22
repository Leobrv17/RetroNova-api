from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, credentials
import firebase_admin
# Firebase Admin Setup
cred = credentials.Certificate("./retronova-df56b-firebase-adminsdk-8qab9-2a10e2588c.json")
firebase_admin.initialize_app(cred)

security = HTTPBearer()

def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# @app.get("/protected")
# def protected_route(user_data: dict = Depends(verify_firebase_token)):
#     firebase_uuid = user_data.get("uid")  # Récupération de l'UID Firebase
#     return {"message": "Access granted", "firebase_uuid": firebase_uuid}