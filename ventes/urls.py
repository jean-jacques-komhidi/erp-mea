from django.urls import path
from . import views

app_name = 'ventes'

urlpatterns = [
    # URLs pour les commandes de vente
    path('commandes/', views.liste_commandes_vente, name='liste_commandes_vente'),
    path('commandes/nouvelle/', views.creer_commande_vente, name='creer_commande_vente'),
    path('commandes/<int:pk>/', views.details_commande_vente, name='details_commande_vente'),
    path('commandes/<int:pk>/modifier/', views.modifier_commande_vente, name='modifier_commande_vente'),
    path('commandes/<int:pk>/confirmer/', views.confirmer_commande_vente, name='confirmer_commande_vente'),
    path('commandes/<int:pk>/expedier/', views.expedier_commande_vente, name='expedier_commande_vente'),
    path('expeditions/', views.liste_expeditions, name='liste_expeditions'),
    path('commandes/<int:pk>/facturer/', views.facturer_commande_vente, name='facturer_commande_vente'),
    path('commandes/<int:pk>/supprimer/', views.supprimer_commande_vente, name='supprimer_commande_vente'),

    # NOUVELLE ROUTE D'EXPORTATION
    path('commandes/exporter/', views.exporter_commandes_vente, name='exporter_commandes_vente'),
    
    # URLs pour les factures
    path('factures/', views.liste_factures, name='liste_factures'),
    path('factures/<int:pk>/', views.details_facture, name='details_facture'),
    path('factures/<int:pk>/envoyer/', views.envoyer_facture, name='envoyer_facture'),
    path('factures/<int:pk>/paiement/', views.enregistrer_paiement, name='enregistrer_paiement'),
    path('factures/<int:pk>/pdf/', views.facture_pdf, name='facture_pdf'),
    
    # Actions rapides factures (NOUVELLES ROUTES)
    path('factures/<int:pk>/imprimer/', views.imprimer_facture, name='imprimer_facture'),
    path('factures/<int:pk>/pdf/', views.telecharger_facture_pdf, name='facture_pdf'),
    path('factures/<int:pk>/telecharger-pdf/', views.telecharger_facture_pdf, name='telecharger_facture_pdf'),
    path('factures/<int:pk>/envoyer-email/', views.envoyer_facture_email, name='envoyer_facture_email'),
    path('factures/<int:pk>/envoyer/', views.envoyer_facture_email, name='envoyer_facture'),

    # Dans ventes/urls.py
    path('commandes/<int:pk>/imprimer/', views.imprimer_commande, name='imprimer_commande'),
    path('commandes/<int:pk>/telecharger-pdf/', views.telecharger_commande_pdf, name='telecharger_commande_pdf'),
    path('commandes/<int:pk>/envoyer-email/', views.envoyer_commande_email, name='envoyer_commande_email'),
    
    # API pour AJAX
    path('api/produit/<int:pk>/prix/', views.obtenir_prix_produit, name='obtenir_prix_produit'),
]