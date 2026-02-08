from django.contrib import admin
from .models import CommandeVente, LigneCommandeVente, Facture, LigneFacture

# ==================== COMMANDES DE VENTE ====================

class LigneCommandeVenteEnLigne(admin.TabularInline):
    model = LigneCommandeVente
    extra = 1
    fields = ['produit', 'quantite', 'prix_unitaire', 'remise', 'taux_tva']
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.statut in ['FACTURE', 'ANNULE']:
            return ['produit', 'quantite', 'prix_unitaire', 'remise', 'taux_tva']
        return []

@admin.register(CommandeVente)
class AdminCommandeVente(admin.ModelAdmin):
    list_display = ['numero_commande', 'client', 'date_commande', 'date_livraison', 'statut', 'total', 'cree_par']
    search_fields = ['numero_commande', 'client__nom']
    list_filter = ['statut', 'date_commande', 'date_creation', 'entrepot']
    ordering = ['-date_creation']
    inlines = [LigneCommandeVenteEnLigne]
    readonly_fields = ['numero_commande', 'sous_total', 'montant_tva', 'total', 'cree_par', 'date_creation']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('numero_commande', 'client', 'date_livraison', 'entrepot', 'statut')
        }),
        ('Montants', {
            'fields': ('sous_total', 'montant_tva', 'total'),
            'classes': ('collapse',)
        }),
        ('Notes et suivi', {
            'fields': ('notes', 'cree_par', 'date_creation'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une nouvelle commande
            obj.cree_par = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()
        # Recalculer les totaux après modification des lignes
        form.instance.calculer_totaux()

# ==================== FACTURES ====================

class LigneFactureEnLigne(admin.TabularInline):
    model = LigneFacture
    extra = 1
    fields = ['produit', 'quantite', 'prix_unitaire', 'remise', 'taux_tva']
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.statut in ['PAYEE', 'ANNULEE']:
            return ['produit', 'quantite', 'prix_unitaire', 'remise', 'taux_tva']
        return []

@admin.register(Facture)
class AdminFacture(admin.ModelAdmin):
    list_display = ['numero_facture', 'client', 'date_facture', 'date_echeance', 'total', 'montant_paye', 'solde_display', 'statut']
    search_fields = ['numero_facture', 'client__nom']
    list_filter = ['statut', 'date_facture', 'date_echeance']
    ordering = ['-date_creation']
    readonly_fields = ['numero_facture', 'sous_total', 'montant_tva', 'total', 'solde_display', 'date_creation']
    inlines = [LigneFactureEnLigne]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('numero_facture', 'client', 'commande_vente', 'date_echeance', 'statut')
        }),
        ('Montants', {
            'fields': ('sous_total', 'montant_tva', 'total', 'montant_paye', 'solde_display')
        }),
        ('Notes et suivi', {
            'fields': ('notes', 'date_creation'),
            'classes': ('collapse',)
        }),
    )
    
    def solde_display(self, obj):
        """Affiche le solde restant"""
        solde = obj.solde
        if solde > 0:
            return f"{solde:,.2f} FCFA (à payer)"
        elif solde == 0:
            return "0 FCFA (soldé)"
        else:
            return f"{abs(solde):,.2f} FCFA (trop-perçu)"
    solde_display.short_description = "Solde"
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()
        # Recalculer les totaux après modification des lignes
        facture = form.instance
        lignes = facture.lignes.all()
        facture.sous_total = sum(ligne.sous_total for ligne in lignes)
        facture.montant_tva = sum(ligne.montant_tva for ligne in lignes)
        facture.total = facture.sous_total + facture.montant_tva
        facture.save()

# ==================== LIGNES (optionnel) ====================

@admin.register(LigneCommandeVente)
class AdminLigneCommandeVente(admin.ModelAdmin):
    list_display = ['commande', 'produit', 'quantite', 'prix_unitaire', 'remise', 'taux_tva', 'total_display']
    search_fields = ['commande__numero_commande', 'produit__nom']
    list_filter = ['commande__date_commande', 'produit__categorie']
    
    def total_display(self, obj):
        """Affiche le total de la ligne"""
        return f"{obj.total:,.2f} FCFA"
    total_display.short_description = "Total TTC"

@admin.register(LigneFacture)
class AdminLigneFacture(admin.ModelAdmin):
    list_display = ['facture', 'produit', 'quantite', 'prix_unitaire', 'remise', 'taux_tva', 'total_display']
    search_fields = ['facture__numero_facture', 'produit__nom']
    list_filter = ['facture__date_facture', 'produit__categorie']
    
    def total_display(self, obj):
        """Affiche le total de la ligne"""
        return f"{obj.total:,.2f} FCFA"
    total_display.short_description = "Total TTC"