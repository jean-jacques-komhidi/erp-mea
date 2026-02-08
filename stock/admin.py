from django.contrib import admin
from .models import Categorie, Produit, Entrepot, MouvementStock

@admin.register(Categorie)
class AdminCategorie(admin.ModelAdmin):
    list_display = ['nom', 'parent', 'description']
    search_fields = ['nom']
    list_filter = ['parent']

@admin.register(Produit)
class AdminProduit(admin.ModelAdmin):
    list_display = ['code', 'nom', 'categorie', 'prix_achat', 'prix_vente', 'est_actif', 'date_creation']
    search_fields = ['code', 'nom', 'description']
    list_filter = ['est_actif', 'categorie', 'date_creation']
    ordering = ['nom']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'nom', 'description', 'categorie', 'unite', 'image', 'est_actif')
        }),
        ('Prix', {
            'fields': ('prix_achat', 'prix_vente', 'taux_tva')
        }),
        ('Gestion de stock', {
            'fields': ('stock_min', 'stock_max', 'seuil_reapprovisionnement')
        }),
    )

@admin.register(Entrepot)
class AdminEntrepot(admin.ModelAdmin):
    list_display = ['code', 'nom', 'responsable', 'est_actif']
    search_fields = ['code', 'nom']
    list_filter = ['est_actif']

@admin.register(MouvementStock)
class AdminMouvementStock(admin.ModelAdmin):
    list_display = ['date', 'produit', 'entrepot', 'type_mouvement', 'quantite', 'reference', 'utilisateur']
    search_fields = ['produit__nom', 'reference']
    list_filter = ['type_mouvement', 'entrepot', 'date']
    ordering = ['-date']
    readonly_fields = ['date', 'utilisateur']
    fieldsets = (
        ('Informations sur le mouvement', {
            'fields': ('produit', 'entrepot', 'type_mouvement', 'quantite', 'reference', 'notes', 'date', 'utilisateur')
        }),
    )   
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.utilisateur = request.user
        super().save_model(request, obj, form, change)
        
