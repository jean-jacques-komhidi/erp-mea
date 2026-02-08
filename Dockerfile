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

# Commande de démarrage avec création du superuser
CMD python manage.py migrate --noinput && \
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@erp-mea.com', 'Admin2026!ERP'); print('✅ Superuser ready')" && \
    gunicorn erp_mea.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120