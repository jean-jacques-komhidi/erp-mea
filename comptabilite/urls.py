from django.urls import path
from . import views

app_name = 'comptabilite'

urlpatterns = [
    # Tableau de bord
    path('', views.tableau_bord_comptabilite, name='tableau_bord'),
    
    # Plan comptable
    path('plan-comptable/', views.liste_plan_comptable, name='liste_plan_comptable'),
    path('plan-comptable/nouveau/', views.creer_compte, name='creer_compte'),
    path('plan-comptable/<int:pk>/', views.details_compte, name='details_compte'),
    
    # Exercices
    path('exercices/', views.liste_exercices, name='liste_exercices'),
    path('exercices/nouveau/', views.creer_exercice, name='creer_exercice'),
    
    # Journaux
    path('journaux/', views.liste_journaux, name='liste_journaux'),
    path('journaux/nouveau/', views.creer_journal, name='creer_journal'),
    
    # Pièces comptables
    path('pieces/', views.liste_pieces, name='liste_pieces'),
    path('pieces/nouvelle/', views.creer_piece, name='creer_piece'),
    path('pieces/<int:pk>/', views.details_piece, name='details_piece'),
    path('pieces/<int:pk>/valider/', views.valider_piece, name='valider_piece'),
    
    # Banques
    path('banques/', views.liste_banques, name='liste_banques'),
    path('banques/nouvelle/', views.creer_banque, name='creer_banque'),
    path('banques/<int:pk>/', views.details_banque, name='details_banque'),
    path('mouvements-bancaires/nouveau/', views.creer_mouvement_bancaire, name='creer_mouvement_bancaire'),
    
    # Budgets
    path('budgets/', views.liste_budgets, name='liste_budgets'),
    path('budgets/nouveau/', views.creer_budget, name='creer_budget'),
    
    # Rapports
    path('rapports/bilan/', views.bilan, name='bilan'),
    path('rapports/compte-resultat/', views.compte_resultat, name='compte_resultat'),
]

