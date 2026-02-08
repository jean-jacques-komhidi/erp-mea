from django.urls import path
from . import views 

urlpatterns = [
    # URLs pour les clients
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/nouveau/', views.creer_client, name='creer_client'),
    path('clients/<int:pk>/', views.details_client, name='details_client'),
    path('clients/<int:pk>/modifier/', views.modifier_client, name='modifier_client'),
    path('clients/<int:pk>/supprimer/', views.supprimer_client, name='supprimer_client'),
    # Export et actions groupées pour les clients
    path('clients/exporter/', views.exporter_clients, name='exporter_clients'),
    path('clients/action-groupee/', views.action_groupee_clients, name='action_groupee_clients'),
    
    # URLs pour les fournisseurs
    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('fournisseurs/nouveau/', views.creer_fournisseur, name='creer_fournisseur'),
    path('fournisseurs/<int:pk>/', views.details_fournisseur, name='details_fournisseur'),
    path('fournisseurs/<int:pk>/modifier/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('fournisseurs/<int:pk>/supprimer/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
    path('fournisseurs/exporter/', views.exporter_fournisseurs, name='exporter_fournisseurs'),
    path('fournisseurs/action-groupee/', views.action_groupee_fournisseurs, name='action_groupee_fournisseurs'),
]

