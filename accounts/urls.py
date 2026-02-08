# ============================================
# NOUVEAU FICHIER : accounts/urls.py
# Routes pour l'authentification
# ============================================

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentification de base
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profil utilisateur
    path('profil/', views.profil_view, name='profil'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('profil/changer-mot-de-passe/', views.changer_mot_de_passe, name='changer_mot_de_passe'),
    
    # Mot de passe oublié
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie, name='mot_de_passe_oublie'),
    path('reinitialiser-mot-de-passe/<str:token>/', views.reinitialiser_mot_de_passe, name='reinitialiser_mot_de_passe'),
    
    # Vérification email
    path('verifier-email/<str:token>/', views.verifier_email, name='verifier_email'),
    
    # Gestion des utilisateurs (Admin)
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateurs/<int:user_id>/modifier/', views.modifier_utilisateur, name='modifier_utilisateur'),
]