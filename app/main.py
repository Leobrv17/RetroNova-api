
from fastapi import FastAPI
from app.data_base import Base, engine
from app.routes import user, friends, payments, games, arcadeMachines, parties, promoCode
from starlette.middleware.cors import CORSMiddleware

# Créer toutes les tables (à utiliser uniquement pendant le développement)
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI()

# Définir les origines autorisées pour le CORS
origins = [
    "http://localhost",  # Permet les requêtes depuis localhost
    "http://localhost:3000",  # Exemple pour une application frontend React qui tourne sur le port 3000
    "https://ton-domaine.com",  # Ajoute d'autres domaines si nécessaire
    "http://localhost:5173",
]

# Ajouter le middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autoriser ces origines
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les en-têtes HTTP
)

app.include_router(user.router, prefix="/users", tags=["Users"])

app.include_router(friends.router, prefix="/friends", tags=["Friends"])

app.include_router(payments.router, prefix="/payments", tags=["Payments"])

app.include_router(games.router, prefix="/games", tags=["Games"])

app.include_router(arcadeMachines.router, prefix="/arcade_machines", tags=["Arcade_Machines"])

app.include_router(parties.router, prefix="/parties", tags=["Parties"])

app.include_router(promoCode.router, prefix="/promo_codes", tags=["Promo_Codes"])