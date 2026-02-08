# erp_mea/settings.py - PRODUCTION RAILWAY AVEC CSRF_TRUSTED_ORIGINS
"""
Configuration Django pour ERP MEA - Production Railway
Ce fichier gère automatiquement la connexion PostgreSQL de Railway
"""

import os
from pathlib import Path
import dj_database_url # type: ignore

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY - SECRET KEY
# Railway injecte automatiquement les variables d'environnement
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# DEBUG - False en production
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED HOSTS
# Railway injecte automatiquement RAILWAY_STATIC_URL et RAILWAY_PUBLIC_DOMAIN
railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
railway_static_url = os.environ.get('RAILWAY_STATIC_URL', '')
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '').split(',')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',  # Tous les domaines Railway
    '.up.railway.app',  # Tous les sous-domaines Railway
]

# Ajouter le domaine Railway automatiquement
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)
if railway_static_url:
    ALLOWED_HOSTS.append(railway_static_url.replace('https://', '').replace('http://', ''))

# Ajouter les hosts de la variable d'environnement
ALLOWED_HOSTS.extend([host.strip() for host in allowed_hosts_env if host.strip()])

# Nettoyer les doublons
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

print(f"🌐 ALLOWED_HOSTS configurés : {ALLOWED_HOSTS}")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'django_jinja',
    'rest_framework',
    
    # Apps locales
    'base',
    'stock',
    'ventes',
    'achats',
    'comptabilite',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Servir fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'erp_mea.urls'

# Templates avec Jinja2
TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.jinja',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'erp_mea.wsgi.application'

# Database - Railway injecte automatiquement DATABASE_URL
if os.environ.get('DATABASE_URL'):
    # Production avec PostgreSQL de Railway
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Développement local avec SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Dakar'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Créer le dossier static s'il n'existe pas
if not (BASE_DIR / 'static').exists():
    (BASE_DIR / 'static').mkdir(exist_ok=True)

STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# WhiteNoise pour servir les fichiers statiques efficacement
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings pour production
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False') == 'True'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# ========== CSRF TRUSTED ORIGINS - CRITICAL POUR RAILWAY ==========
# IMPORTANT: Sans ceci, tu auras l'erreur "CSRF verification failed"
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
    'https://erp-mea-production.up.railway.app',
]

# Ajouter les origines de la variable d'environnement si elle existe
csrf_origins_env = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if csrf_origins_env:
    CSRF_TRUSTED_ORIGINS.extend([origin.strip() for origin in csrf_origins_env.split(',') if origin.strip()])

print(f"🔒 CSRF_TRUSTED_ORIGINS configurés : {CSRF_TRUSTED_ORIGINS}")

# Email configuration (optionnel)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Site configuration
SITE_NAME = os.environ.get('SITE_NAME', 'ERP MEA')

# ========== CONFIGURATION AUTHENTIFICATION ==========
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Configuration des sessions
SESSION_COOKIE_AGE = 1209600  # 2 semaines en secondes
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_NAME = 'erp_mea_sessionid'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Message de confirmation au démarrage
print("=" * 60)
print("🚀 ERP MEA - PRODUCTION MODE")
print(f"🗄️  Database: {'PostgreSQL (Railway)' if os.environ.get('DATABASE_URL') else 'SQLite (Local)'}")
print(f"🐛 DEBUG: {DEBUG}")
print(f"🌐 Allowed Hosts: {len(ALLOWED_HOSTS)} configurés")
print(f"🔒 CSRF Origins: {len(CSRF_TRUSTED_ORIGINS)} configurés")
print("=" * 60)