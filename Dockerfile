# Dockerfile - ERP MEA pour Railway
FROM python:3.11-slim

# Variables d'environnement Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier tout le projet
COPY . .

# Créer les dossiers pour les fichiers statiques et media
RUN mkdir -p staticfiles media

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput || true

# Port exposé (Railway l'attribue automatiquement)
EXPOSE 8000

# Commande de démarrage
CMD python manage.py migrate && \
    gunicorn erp_mea.wsgi:application --bind 0.0.0.0:$PORT --workers 3