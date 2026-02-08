from django.urls import path
from . import views


app_name = 'stock'

urlpatterns = [
    # URLs pour les produits
    path('produits/', views.liste_produits, name='liste_produits'),
    path('produits/nouveau/', views.creer_produit, name='creer_produit'),
    path('produits/<int:pk>/', views.details_produit, name='details_produit'),
    path('produits/<int:pk>/modifier/', views.modifier_produit, name='modifier_produit'),
    path('produits/<int:pk>/supprimer/', views.supprimer_produit, name='supprimer_produit'),
    
    # URLs pour les catégories
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/nouvelle/', views.creer_categorie, name='creer_categorie'),
    path('categories/<int:pk>/modifier/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/<int:pk>/supprimer/', views.supprimer_categorie, name='supprimer_categorie'),
    path('categories/<int:pk>/details/', views.details_categorie, name='details_categorie'),
    
    # URLs pour les mouvements de stock
    path('mouvements/', views.liste_mouvements, name='liste_mouvements'),
    path('mouvements/nouveau/', views.creer_mouvement_stock, name='creer_mouvement_stock'),
    path('mouvements/<int:pk>/', views.details_mouvement, name='details_mouvement'),
    path('mouvements/<int:pk>/modifier/', views.modifier_mouvement, name='modifier_mouvement'),
    path('mouvements/<int:pk>/supprimer/', views.supprimer_mouvement, name='supprimer_mouvement'),
    
    # URLs pour les entrepôts
    path('entrepots/', views.liste_entrepots, name='liste_entrepots'),
    path('entrepots/nouveau/', views.creer_entrepot, name='creer_entrepot'),
    path('entrepots/<int:pk>/', views.details_entrepot, name='details_entrepot'),
    path('entrepots/<int:pk>/modifier/', views.modifier_entrepot, name='modifier_entrepot'),
    path('entrepots/<int:pk>/supprimer/', views.supprimer_entrepot, name='supprimer_entrepot'),
    

    # URLs pour les rapports
    path('rapport/', views.rapport_stock, name='rapport_stock'),
]