# achats/urls.py - Routes du module achats

from django.urls import path
from . import views

app_name = 'achats'

urlpatterns = [
    # ========== LISTE ET TABLEAU DE BORD ==========
    path('', views.liste_commandes_achat, name='liste_commandes_achat'),
    path('historique/', views.historique_achats, name='historique_achats'),

    # ⭐ NOUVELLE ROUTE D'EXPORTATION (DOIT ÊTRE AVANT nouvelle/ et <int:pk>/) ⭐
    path('historique/imprimer/', views.imprimer_historique_achats, name='imprimer_historique_achats'),
    path('historique/telecharger-pdf/', views.telecharger_historique_pdf, name='telecharger_historique_pdf'),
    path('commandes/exporter/', views.exporter_commandes_achat, name='exporter_commandes_achat'),
    
    # ========== CRUD COMMANDES D'ACHAT ==========
    path('nouvelle/', views.creer_commande_achat, name='creer_commande_achat'),
    path('<int:pk>/', views.details_commande_achat, name='details_commande_achat'),
    path('<int:pk>/modifier/', views.modifier_commande_achat, name='modifier_commande_achat'),
    path('<int:pk>/supprimer/', views.supprimer_commande_achat, name='supprimer_commande_achat'),
    
    # ========== ACTIONS SUR LES COMMANDES ==========
    path('<int:pk>/confirmer/', views.confirmer_commande_achat, name='confirmer_commande_achat'),
    path('<int:pk>/envoyer/', views.envoyer_commande_achat, name='envoyer_commande_achat'),
    path('<int:pk>/recevoir/', views.recevoir_commande_achat, name='recevoir_commande_achat'),
    path('<int:pk>/annuler/', views.annuler_commande_achat, name='annuler_commande_achat'),
    
    # ========== API AJAX ==========
    path('api/produit/<int:pk>/prix/', views.obtenir_prix_produit, name='obtenir_prix_produit'),
]