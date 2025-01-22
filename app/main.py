import uvicorn
from fastapi import FastAPI
from data_base import Base, engine
from routes import user

# Créer toutes les tables (à utiliser uniquement pendant le développement)
Base.metadata.create_all(bind=engine)

# Créer l'application FastAPI
app = FastAPI()



app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)