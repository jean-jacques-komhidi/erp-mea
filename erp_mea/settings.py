"""
Django settings for erp_mea project.

Configuration optimisée pour développement LOCAL
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zk7&qnqf5g9uc0+9zdn+6l1&!ckv4_sel5rkae7tbr&47^muzj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

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

# Database - SQLite pour développement local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
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

STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration - Console pour développement
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Pour tester les emails en local, décommente ces lignes et mets tes identifiants Gmail
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'ton-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'ton-mot-de-passe-application'
# DEFAULT_FROM_EMAIL = 'ton-email@gmail.com'

# ========== CONFIGURATION AUTHENTIFICATION ==========

# Redirection après login/logout
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Configuration des sessions
SESSION_COOKIE_AGE = 1209600  # 2 semaines en secondes
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_NAME = 'erp_mea_sessionid'

# ========== SÉCURITÉ - DÉSACTIVÉE EN DÉVELOPPEMENT ==========
# Ces paramètres sont pour la PRODUCTION uniquement
# En développement local, on n'utilise PAS HTTPS

SECURE_SSL_REDIRECT = False  # Pas de redirection HTTPS en local
SESSION_COOKIE_SECURE = False  # Cookies fonctionnent en HTTP
CSRF_COOKIE_SECURE = False  # CSRF fonctionne en HTTP
SECURE_HSTS_SECONDS = 0  # Pas de HSTS en local

# Message de confirmation au démarrage
print("=" * 60)
print("🚀 MODE DÉVELOPPEMENT LOCAL ACTIVÉ")
print("🌐 Serveur accessible sur : http://localhost:8000")
print("⚠️  HTTPS désactivé (normal en développement)")
print("=" * 60)