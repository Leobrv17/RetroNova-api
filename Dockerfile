# Utiliser une image Python de base
FROM python:3.9-slim

# Installer les dépendances
WORKDIR /application

# Copier l'ensemble de l'application dans le conteneur
COPY . /application/

# Installer les dépendances depuis requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposer sur le port 8000
EXPOSE 8000

# Commande d'exécution par défaut
CMD ["python", "prod.py"]

