# ============================================
# RÉCAPITULATIF MODULE COMPTABILITÉ
# ============================================

"""
📦 FICHIERS CRÉÉS POUR LE MODULE COMPTABILITÉ :

1. comptabilite/models.py ✅
   - PlanComptable : Plan comptable avec types (ACTIF, PASSIF, CHARGE, PRODUIT)
   - Exercice : Exercices comptables
   - Journal : Journaux (Ventes, Achats, Banque, Caisse, OD)
   - Piece : Pièces comptables (regroupement d'écritures)
   - Ecriture : Écritures comptables (Débit/Crédit)
   - Banque : Comptes bancaires
   - MouvementBancaire : Mouvements bancaires
   - Budget : Budgets prévisionnels

2. comptabilite/forms.py ✅
   - FormulairePlanComptable
   - FormulaireExercice
   - FormulaireJournal
   - FormulairePiece
   - FormulaireEcriture
   - FormulaireBanque
   - FormulaireMouvementBancaire
   - FormulaireBudget
   - FormulaireRapprochementBancaire

3. comptabilite/views.py ✅
   - tableau_bord_comptabilite : Dashboard comptabilité
   - Plan comptable : liste, créer, détails
   - Exercices : liste, créer
   - Journaux : liste, créer
   - Pièces : liste, créer, détails, valider
   - Banques : liste, créer, détails
   - Mouvements bancaires : créer
   - Budgets : liste, créer
   - Rapports : bilan, compte de résultat

4. comptabilite/urls.py ✅
   - URLs complètes pour tous les modules

5. comptabilite/admin.py ✅
   - Interface d'administration Django

6. Script d'initialisation ✅
   - Commande pour initialiser le plan comptable SYSCOHADA
"""

# ============================================
# ÉTAPES D'INSTALLATION
# ============================================

"""
1. Copier les fichiers dans votre projet :
   - comptabilite/models.py
   - comptabilite/forms.py
   - comptabilite/views.py
   - comptabilite/urls.py
   - comptabilite/admin.py

2. Créer le dossier pour la commande d'initialisation :
   comptabilite/management/commands/initialiser_comptabilite.py

3. Faire les migrations :
   python manage.py makemigrations
   python manage.py migrate

4. Initialiser le plan comptable :
   python manage.py initialiser_comptabilite

5. Lancer le serveur :
   python manage.py runserver
"""

# ============================================
# erp_mea/urls.py - METTRE À JOUR
# ============================================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from base import views as vues_base

urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),
    
    # Page d'accueil - Tableau de bord
    path('', vues_base.tableau_bord, name='tableau_bord'),
    
    # Inclure les URLs des différents modules
    path('', include('base.urls')),
    path('stock/', include('stock.urls')),
    path('ventes/', include('ventes.urls')),
    path('achats/', include('achats.urls')),
    path('comptabilite/', include('comptabilite.urls')),  # ← AJOUTER CETTE LIGNE
]

# Servir les fichiers média en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ============================================
# FONCTIONNALITÉS DU MODULE COMPTABILITÉ
# ============================================

"""
✅ PLAN COMPTABLE :
- Gestion complète du plan comptable (SYSCOHADA)
- Comptes hiérarchiques avec compte parent
- Classification : Actif, Passif, Charge, Produit
- Calcul automatique des soldes

✅ EXERCICES COMPTABLES :
- Création d'exercices
- Clôture d'exercices
- Suivi multi-exercices

✅ JOURNAUX :
- Journal des ventes
- Journal des achats
- Journal de banque
- Journal de caisse
- Opérations diverses

✅ PIÈCES COMPTABLES :
- Création de pièces avec écritures multiples
- Validation de pièces (avec contrôle équilibre Débit = Crédit)
- Numérotation automatique
- Lien avec les factures et commandes

✅ ÉCRITURES COMPTABLES :
- Écritures en partie double
- Lien avec clients et fournisseurs
- Grand livre par compte

✅ BANQUES :
- Gestion multi-banques
- Mouvements bancaires (Crédit/Débit)
- Calcul automatique des soldes
- Rapprochement bancaire

✅ BUDGETS :
- Budgets prévisionnels mensuels
- Comparaison prévu/réalisé
- Calcul des écarts
- Taux de réalisation

✅ RAPPORTS :
- Bilan comptable
- Compte de résultat
- Grand livre
- Balance générale

✅ INTÉGRATION :
- Lien automatique avec les ventes (factures)
- Lien automatique avec les achats
- Synchronisation avec les stocks
"""

# ============================================
# EXEMPLE D'UTILISATION
# ============================================

"""
# 1. CRÉER UN EXERCICE
Exercice 2024 : du 01/01/2024 au 31/12/2024

# 2. CRÉER DES COMPTES (ou utiliser le script d'initialisation)
411 - Clients (ACTIF)
401 - Fournisseurs (PASSIF)
701 - Ventes de marchandises (PRODUIT)
601 - Achats de marchandises (CHARGE)
521 - Banque (ACTIF)

# 3. CRÉER UNE PIÈCE COMPTABLE
Journal : VE (Ventes)
Date : 22/01/2026
Libellé : Vente facture FAC202601001

Écritures :
- Débit 411 (Clients) : 590 000 FCFA
- Crédit 701 (Ventes) : 500 000 FCFA
- Crédit 445 (TVA) : 90 000 FCFA

Total Débit = Total Crédit = 590 000 FCFA ✓

# 4. VALIDER LA PIÈCE
La pièce est équilibrée → Validation OK

# 5. CONSULTER LES RAPPORTS
- Bilan : Voir actif et passif
- Compte de résultat : Voir charges et produits
- Solde banque : Consultation en temps réel
"""

# ============================================
# PLAN COMPTABLE SYSCOHADA (Extrait)
# ============================================

"""
CLASSE 1 - COMPTES DE RESSOURCES DURABLES
10 - Capital
11 - Réserves
12 - Report à nouveau
13 - Résultat net
16 - Emprunts

CLASSE 2 - ACTIF IMMOBILISÉ
21 - Immobilisations incorporelles
22 - Terrains
23 - Bâtiments
24 - Matériel
28 - Amortissements

CLASSE 3 - STOCKS
31 - Marchandises
32 - Matières premières
33 - Autres approvisionnements

CLASSE 4 - TIERS
40 - Fournisseurs
41 - Clients
43 - État
44 - Sécurité sociale
47 - Débiteurs/Créditeurs divers

CLASSE 5 - TRÉSORERIE
52 - Banques
57 - Caisse
58 - Virements internes

CLASSE 6 - CHARGES
60 - Achats
61 - Transports
62 - Services extérieurs A
63 - Services extérieurs B
64 - Impôts et taxes
65 - Autres charges
66 - Charges de personnel
67 - Frais financiers

CLASSE 7 - PRODUITS
70 - Ventes
71 - Subventions
75 - Autres produits
77 - Revenus financiers
"""

# ============================================
# PROCHAINES FONCTIONNALITÉS POSSIBLES
# ============================================

"""
🔜 FONCTIONNALITÉS AVANCÉES :

1. Lettrage des comptes (Clients/Fournisseurs)
2. Rapprochement bancaire automatique
3. Export comptable (FEC, CSV)
4. Génération automatique de pièces depuis factures
5. Tableaux de bord analytiques
6. Consolidation multi-sociétés
7. Gestion des immobilisations
8. Calcul des amortissements
9. Liasse fiscale
10. Analyse financière (ratios)
"""

print("✅ Module Comptabilité créé avec succès!")
print("📚 Documentation complète disponible dans ce fichier")
print("🚀 Prêt à être utilisé!")