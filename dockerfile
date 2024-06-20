# Utilisel'image de base Python
FROM python:3.9-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste des fichiers de l'application dans le conteneur
COPY . .


