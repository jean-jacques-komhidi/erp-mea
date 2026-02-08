
# comptabilite/management/commands/initialiser_comptabilite.py

from django.core.management.base import BaseCommand
from comptabilite.models import PlanComptable, Exercice, Journal
from datetime import date

class Command(BaseCommand):
    help = 'Initialise le plan comptable de base'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Initialisation du plan comptable...\n')
        
        # Plan comptable de base (système SYSCOHADA)
        comptes = [
            # CLASSE 1 - COMPTES DE RESSOURCES DURABLES
            {'numero': '10', 'libelle': 'Capital', 'type': 'PASSIF'},
            {'numero': '11', 'libelle': 'Réserves', 'type': 'PASSIF'},
            {'numero': '12', 'libelle': 'Report à nouveau', 'type': 'PASSIF'},
            {'numero': '13', 'libelle': 'Résultat net de l\'exercice', 'type': 'PASSIF'},
            {'numero': '16', 'libelle': 'Emprunts et dettes assimilées', 'type': 'PASSIF'},
            
            # CLASSE 2 - COMPTES D'ACTIF IMMOBILISÉ
            {'numero': '21', 'libelle': 'Immobilisations incorporelles', 'type': 'ACTIF'},
            {'numero': '22', 'libelle': 'Terrains', 'type': 'ACTIF'},
            {'numero': '23', 'libelle': 'Bâtiments', 'type': 'ACTIF'},
            {'numero': '24', 'libelle': 'Matériel', 'type': 'ACTIF'},
            {'numero': '28', 'libelle': 'Amortissements', 'type': 'ACTIF'},
            
            # CLASSE 3 - COMPTES DE STOCKS
            {'numero': '31', 'libelle': 'Marchandises', 'type': 'ACTIF'},
            {'numero': '32', 'libelle': 'Matières premières', 'type': 'ACTIF'},
            {'numero': '33', 'libelle': 'Autres approvisionnements', 'type': 'ACTIF'},
            
            # CLASSE 4 - COMPTES DE TIERS
            {'numero': '40', 'libelle': 'Fournisseurs et comptes rattachés', 'type': 'PASSIF'},
            {'numero': '401', 'libelle': 'Fournisseurs', 'type': 'PASSIF'},
            {'numero': '41', 'libelle': 'Clients et comptes rattachés', 'type': 'ACTIF'},
            {'numero': '411', 'libelle': 'Clients', 'type': 'ACTIF'},
            {'numero': '43', 'libelle': 'État', 'type': 'PASSIF'},
            {'numero': '445', 'libelle': 'État - TVA', 'type': 'PASSIF'},
            {'numero': '47', 'libelle': 'Débiteurs et créditeurs divers', 'type': 'ACTIF'},
            
            # CLASSE 5 - COMPTES DE TRÉSORERIE
            {'numero': '52', 'libelle': 'Banques', 'type': 'ACTIF'},
            {'numero': '521', 'libelle': 'Banques locales', 'type': 'ACTIF'},
            {'numero': '57', 'libelle': 'Caisse', 'type': 'ACTIF'},
            
            # CLASSE 6 - COMPTES DE CHARGES
            {'numero': '60', 'libelle': 'Achats', 'type': 'CHARGE'},
            {'numero': '601', 'libelle': 'Achats de marchandises', 'type': 'CHARGE'},
            {'numero': '61', 'libelle': 'Transports', 'type': 'CHARGE'},
            {'numero': '62', 'libelle': 'Services extérieurs A', 'type': 'CHARGE'},
            {'numero': '63', 'libelle': 'Services extérieurs B', 'type': 'CHARGE'},
            {'numero': '64', 'libelle': 'Impôts et taxes', 'type': 'CHARGE'},
            {'numero': '65', 'libelle': 'Autres charges', 'type': 'CHARGE'},
            {'numero': '66', 'libelle': 'Charges de personnel', 'type': 'CHARGE'},
            {'numero': '67', 'libelle': 'Frais financiers', 'type': 'CHARGE'},
            
            # CLASSE 7 - COMPTES DE PRODUITS
            {'numero': '70', 'libelle': 'Ventes', 'type': 'PRODUIT'},
            {'numero': '701', 'libelle': 'Ventes de marchandises', 'type': 'PRODUIT'},
            {'numero': '71', 'libelle': 'Subventions d\'exploitation', 'type': 'PRODUIT'},
            {'numero': '75', 'libelle': 'Autres produits', 'type': 'PRODUIT'},
            {'numero': '77', 'libelle': 'Revenus financiers', 'type': 'PRODUIT'},
        ]
        
        compteur = 0
        for compte_data in comptes:
            _, cree = PlanComptable.objects.get_or_create(
                numero_compte=compte_data['numero'],
                defaults={
                    'libelle': compte_data['libelle'],
                    'type_compte': compte_data['type'],
                    'est_actif': True
                }
            )
            if cree:
                compteur += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {compteur} comptes créés'))
        
        # Créer les journaux par défaut
        journaux = [
            {'code': 'VE', 'libelle': 'Journal des ventes', 'type': 'VENTE'},
            {'code': 'AC', 'libelle': 'Journal des achats', 'type': 'ACHAT'},
            {'code': 'BQ', 'libelle': 'Journal de banque', 'type': 'BANQUE'},
            {'code': 'CA', 'libelle': 'Journal de caisse', 'type': 'CAISSE'},
            {'code': 'OD', 'libelle': 'Opérations diverses', 'type': 'OD'},
        ]
        
        compteur_journaux = 0
        for journal_data in journaux:
            _, cree = Journal.objects.get_or_create(
                code=journal_data['code'],
                defaults={
                    'libelle': journal_data['libelle'],
                    'type_journal': journal_data['type'],
                    'est_actif': True
                }
            )
            if cree:
                compteur_journaux += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {compteur_journaux} journaux créés'))
        
        # Créer l'exercice en cours
        annee_actuelle = date.today().year
        _, cree = Exercice.objects.get_or_create(
            nom=f'Exercice {annee_actuelle}',
            defaults={
                'date_debut': date(annee_actuelle, 1, 1),
                'date_fin': date(annee_actuelle, 12, 31),
                'est_cloture': False
            }
        )
        
        if cree:
            self.stdout.write(self.style.SUCCESS('✓ Exercice créé'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Initialisation de la comptabilité terminée!\n'))
