# Utiliser une image Python de base
FROM python:3.9-slim

# Installer les dépendances
WORKDIR /application

# Assurez-vous que Python inclut /app dans le PYTHONPATH
#ENV PYTHONPATH=/app

# Copier l'ensemble de l'application dans le conteneur
COPY . /application/

# Installer les dépendances depuis requirements.txt
RUN pip install -r requirements.txt

# Définir PYTHONPATH pour que Python reconnaisse le module 'app'
# ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8000
# Commande d'exécution par défaut
CMD ["python", "prod.py"]

