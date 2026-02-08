# achats/admin.py - Administration basique du module achats

from django.contrib import admin
from .models import CommandeAchat, LigneCommandeAchat, PaiementFournisseur


class LigneCommandeAchatInline(admin.TabularInline):
    """Inline pour les lignes de commande"""
    model = LigneCommandeAchat
    extra = 1
    fields = ['produit', 'quantite', 'quantite_recue', 'prix_unitaire', 'taux_tva']


@admin.register(CommandeAchat)
class CommandeAchatAdmin(admin.ModelAdmin):
    """Administration des commandes d'achat"""
    list_display = ['numero_commande', 'fournisseur', 'entrepot', 'statut', 'date_commande', 'total', 'cree_par']
    list_filter = ['statut', 'date_commande', 'fournisseur']
    search_fields = ['numero_commande', 'fournisseur__nom']
    readonly_fields = ['numero_commande', 'sous_total', 'montant_tva', 'total', 'cree_par', 'date_creation']
    inlines = [LigneCommandeAchatInline]
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('numero_commande', 'fournisseur', 'entrepot', 'statut')
        }),
        ('Dates', {
            'fields': ('date_commande', 'date_livraison_prevue', 'date_reception')
        }),
        ('Montants', {
            'fields': ('sous_total', 'montant_tva', 'total')
        }),
        ('Autres', {
            'fields': ('notes', 'raison_annulation', 'piece_comptable', 'cree_par', 'date_creation')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.cree_par = request.user
        super().save_model(request, obj, form, change)


@admin.register(LigneCommandeAchat)
class LigneCommandeAchatAdmin(admin.ModelAdmin):
    """Administration des lignes de commande"""
    list_display = ['commande', 'produit', 'quantite', 'quantite_recue', 'prix_unitaire', 'taux_tva']
    list_filter = ['commande__statut', 'commande__date_commande']
    search_fields = ['commande__numero_commande', 'produit__nom']


@admin.register(PaiementFournisseur)
class PaiementFournisseurAdmin(admin.ModelAdmin):
    """Administration des paiements fournisseurs"""
    list_display = ['numero_paiement', 'commande', 'fournisseur', 'montant', 'date_paiement', 'mode_paiement']
    list_filter = ['mode_paiement', 'date_paiement']
    search_fields = ['numero_paiement', 'commande__numero_commande', 'fournisseur__nom']
    readonly_fields = ['numero_paiement', 'utilisateur']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.utilisateur = request.user
        super().save_model(request, obj, form, change)