from django.contrib import admin
from .models import Entreprise, Client, Fournisseur

@admin.register(Entreprise)
class AdminEntreprise(admin.ModelAdmin):
    list_display = ['nom', 'email', 'telephone', 'date_creation']
    search_fields = ['nom', 'email']
    list_filter = ['date_creation']

@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ['code', 'nom', 'email', 'ville', 'pays', 'limite_credit', 'est_actif']
    search_fields = ['code', 'nom', 'email']
    list_filter = ['est_actif', 'pays', 'ville', 'date_creation']
    ordering = ['-date_creation']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'nom', 'email', 'telephone', 'est_actif')
        }),
        ('Adresse', {
            'fields': ('adresse', 'ville', 'pays')
        }),
        ('Informations financières', {
            'fields': ('numero_fiscal', 'limite_credit')
        }),
    )

@admin.register(Fournisseur)
class AdminFournisseur(admin.ModelAdmin):
    list_display = ['code', 'nom', 'email', 'ville', 'pays', 'delai_paiement', 'est_actif']
    search_fields = ['code', 'nom', 'email']
    list_filter = ['est_actif', 'pays', 'ville', 'date_creation']
    ordering = ['-date_creation']
