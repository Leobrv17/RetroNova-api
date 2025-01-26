import uvicorn
from fastapi import FastAPI
from data_base import Base, engine
from routes import user, friends, payments, games, arcadeMachines, parties

# Créer toutes les tables (à utiliser uniquement pendant le développement)
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI()



app.include_router(user.router, prefix="/users", tags=["Users"])

app.include_router(friends.router, prefix="/friends", tags=["Friends"])

app.include_router(payments.router, prefix="/payments", tags=["Payments"])

app.include_router(games.router, prefix="/games", tags=["Games"])

app.include_router(arcadeMachines.router, prefix="/arcade_machines", tags=["Arcade_Machines"])

app.include_router(parties.router, prefix="/parties", tags=["Parties"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)