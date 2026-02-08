# ============================================
# comptabilite/admin.py - Administration
# ============================================

from django.contrib import admin
from .models import (
    PlanComptable, Exercice, Journal, Piece, Ecriture,
    Banque, MouvementBancaire, Budget
)

@admin.register(PlanComptable)
class AdminPlanComptable(admin.ModelAdmin):
    list_display = ['numero_compte', 'libelle', 'type_compte', 'compte_parent', 'est_actif']
    list_filter = ['type_compte', 'est_actif']
    search_fields = ['numero_compte', 'libelle']
    ordering = ['numero_compte']


@admin.register(Exercice)
class AdminExercice(admin.ModelAdmin):
    list_display = ['nom', 'date_debut', 'date_fin', 'est_cloture']
    list_filter = ['est_cloture']
    ordering = ['-date_debut']


@admin.register(Journal)
class AdminJournal(admin.ModelAdmin):
    list_display = ['code', 'libelle', 'type_journal', 'est_actif']
    list_filter = ['type_journal', 'est_actif']
    search_fields = ['code', 'libelle']


class EcritureEnLigne(admin.TabularInline):
    model = Ecriture
    extra = 2
    fields = ['compte', 'libelle', 'debit', 'credit']


@admin.register(Piece)
class AdminPiece(admin.ModelAdmin):
    list_display = ['numero_piece', 'journal', 'date_piece', 'libelle', 'est_validee', 'total_debit', 'total_credit']
    list_filter = ['est_validee', 'journal', 'exercice']
    search_fields = ['numero_piece', 'libelle', 'reference']
    ordering = ['-date_piece']
    inlines = [EcritureEnLigne]
    readonly_fields = ['numero_piece', 'date_validation', 'validee_par', 'cree_par', 'date_creation']


@admin.register(Ecriture)
class AdminEcriture(admin.ModelAdmin):
    list_display = ['piece', 'compte', 'libelle', 'debit', 'credit']
    list_filter = ['piece__journal', 'compte__type_compte']
    search_fields = ['libelle', 'piece__numero_piece', 'compte__numero_compte']
    ordering = ['-piece__date_piece']


@admin.register(Banque)
class AdminBanque(admin.ModelAdmin):
    list_display = ['nom', 'numero_compte', 'devise', 'solde_initial', 'est_actif']
    list_filter = ['est_actif', 'devise']
    search_fields = ['nom', 'numero_compte', 'iban']


@admin.register(MouvementBancaire)
class AdminMouvementBancaire(admin.ModelAdmin):
    list_display = ['banque', 'date_mouvement', 'type_mouvement', 'montant', 'libelle', 'est_rapproche']
    list_filter = ['type_mouvement', 'est_rapproche', 'banque']
    search_fields = ['libelle', 'reference']
    ordering = ['-date_mouvement']
    readonly_fields = ['cree_par', 'date_creation']


@admin.register(Budget)
class AdminBudget(admin.ModelAdmin):
    list_display = ['exercice', 'compte', 'mois', 'montant_prevu', 'montant_realise', 'ecart']
    list_filter = ['exercice', 'mois']
    search_fields = ['compte__numero_compte', 'compte__libelle']
    ordering = ['exercice', 'mois', 'compte']
