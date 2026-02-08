from django.core.management.base import BaseCommand
from base.models import User, Client, Fournisseur, Entreprise
from stock.models import Categorie, Produit, Entrepot
from datetime import datetime

class Command(BaseCommand):
    help = 'Initialise les données de test pour ERP MEA (en français)'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Initialisation des données en cours...\n')
        
        # Créer un superutilisateur si n'existe pas
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@erp-mea.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✓ Superutilisateur créé (admin/admin123)'))
        
        # Créer l'entreprise
        entreprise, cree = Entreprise.objects.get_or_create(
            nom='ERP MEA Entreprise',
            defaults={
                'adresse': 'Zone Industrielle, Dakar, Sénégal',
                'telephone': '+221 33 123 45 67',
                'email': 'contact@erp-mea.com',
                'numero_fiscal': 'NINEA123456789',
            }
        )
        if cree:
            self.stdout.write(self.style.SUCCESS('✓ Entreprise créée'))
        
        # Créer des catégories
        donnees_categories = [
            'Électronique',
            'Informatique',
            'Mobilier de bureau',
            'Fournitures',
            'Équipements',
        ]
        
        compteur_categories = 0
        for nom_categorie in donnees_categories:
            _, cree = Categorie.objects.get_or_create(nom=nom_categorie)
            if cree:
                compteur_categories += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {compteur_categories} catégories créées'))
        
        # Créer un entrepôt principal
        entrepot, cree = Entrepot.objects.get_or_create(
            code='ENT001',
            defaults={
                'nom': 'Entrepôt Principal Dakar',
                'adresse': 'Zone Industrielle, Route de Rufisque, Dakar',
                'est_actif': True,
            }
        )
        if cree:
            self.stdout.write(self.style.SUCCESS('✓ Entrepôt principal créé'))
        
        # Créer des clients
        donnees_clients = [
            {'code': 'CLI001', 'nom': 'Société ABC Sénégal', 'ville': 'Dakar', 'pays': 'Sénégal'},
            {'code': 'CLI002', 'nom': 'Entreprise XYZ', 'ville': 'Abidjan', 'pays': 'Côte d\'Ivoire'},
            {'code': 'CLI003', 'nom': 'Commerce 123', 'ville': 'Lagos', 'pays': 'Nigeria'},
            {'code': 'CLI004', 'nom': 'Trading Ltd', 'ville': 'Accra', 'pays': 'Ghana'},
            {'code': 'CLI005', 'nom': 'Import Export SA', 'ville': 'Casablanca', 'pays': 'Maroc'},
            {'code': 'CLI006', 'nom': 'Distribution Mauritanie', 'ville': 'Nouakchott', 'pays': 'Mauritanie'},
            {'code': 'CLI007', 'nom': 'Services Mali', 'ville': 'Bamako', 'pays': 'Mali'},
        ]
        
        compteur_clients = 0
        for donnees in donnees_clients:
            _, cree = Client.objects.get_or_create(
                code=donnees['code'],
                defaults={
                    'nom': donnees['nom'],
                    'email': f"{donnees['code'].lower()}@exemple.com",
                    'telephone': '+221 33 XXX XX XX',
                    'adresse': f"Adresse de {donnees['nom']}",
                    'ville': donnees['ville'],
                    'pays': donnees['pays'],
                    'limite_credit': 5000000,
                    'est_actif': True,
                }
            )
            if cree:
                compteur_clients += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {compteur_clients} clients créés'))
        
        # Créer des fournisseurs
        donnees_fournisseurs = [
            {'code': 'FOUR001', 'nom': 'Fournisseur Technologies Dakar', 'ville': 'Dakar', 'pays': 'Sénégal'},
            {'code': 'FOUR002', 'nom': 'Import Global Dubai', 'ville': 'Dubai', 'pays': 'Émirats Arabes Unis'},
            {'code': 'FOUR003', 'nom': 'Grossiste Paris', 'ville': 'Paris', 'pays': 'France'},
            {'code': 'FOUR004', 'nom': 'Électronique Chine', 'ville': 'Shanghai', 'pays': 'Chine'},
        ]
        
        compteur_fournisseurs = 0
        for donnees in donnees_fournisseurs:
            _, cree = Fournisseur.objects.get_or_create(
                code=donnees['code'],
                defaults={
                    'nom': donnees['nom'],
                    'email': f"{donnees['code'].lower()}@exemple.com",
                    'telephone': '+221 33 XXX XX XX',
                    'adresse': f"Adresse de {donnees['nom']}",
                    'ville': donnees['ville'],
                    'pays': donnees['pays'],
                    'delai_paiement': 30,
                    'est_actif': True,
                }
            )
            if cree:
                compteur_fournisseurs += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {compteur_fournisseurs} fournisseurs créés'))
        
        # Créer des produits
        electronique = Categorie.objects.get(nom='Électronique')
        informatique = Categorie.objects.get(nom='Informatique')
        mobilier = Categorie.objects.get(nom='Mobilier de bureau')
        
        donnees_produits = [
            {
                'code': 'PROD001',
                'nom': 'Ordinateur portable Dell Latitude',
                'categorie': informatique,
                'prix_achat': 450000,
                'prix_vente': 550000
            },
            {
                'code': 'PROD002',
                'nom': 'Écran LCD 24 pouces Samsung',
                'categorie': informatique,
                'prix_achat': 120000,
                'prix_vente': 150000
            },
            {
                'code': 'PROD003',
                'nom': 'Clavier sans fil Logitech',
                'categorie': informatique,
                'prix_achat': 15000,
                'prix_vente': 20000
            },
            {
                'code': 'PROD004',
                'nom': 'Souris optique USB',
                'categorie': informatique,
                'prix_achat': 8000,
                'prix_vente': 12000
            },
            {
                'code': 'PROD005',
                'nom': 'Imprimante laser HP',
                'categorie': informatique,
                'prix_achat': 180000,
                'prix_vente': 230000
            },
            {
                'code': 'PROD006',
                'nom': 'Smartphone Samsung Galaxy',
                'categorie': electronique,
                'prix_achat': 200000,
                'prix_vente': 250000
            },
            {
                'code': 'PROD007',
                'nom': 'Tablette iPad Pro',
                'categorie': electronique,
                'prix_achat': 350000,
                'prix_vente': 420000
            },
            {
                'code': 'PROD008',
                'nom': 'Casque audio Bluetooth Sony',
                'categorie': electronique,
                'prix_achat': 25000,
                'prix_vente': 35000
            },
            {
                'code': 'PROD009',
                'nom': 'Bureau ergonomique 160x80cm',
                'categorie': mobilier,
                'prix_achat': 85000,
                'prix_vente': 120000
            },
            {
                'code': 'PROD010',
                'nom': 'Chaise de bureau confortable',
                'categorie': mobilier,
                'prix_achat': 45000,
                'prix_vente': 65000
            },
        ]
        
        compteur_produits = 0
        for donnees in donnees_produits:
            _, cree = Produit.objects.get_or_create(
                code=donnees['code'],
                defaults={
                    'nom': donnees['nom'],
                    'categorie': donnees['categorie'],
                    'unite': 'PCE',
                    'prix_achat': donnees['prix_achat'],
                    'prix_vente': donnees['prix_vente'],
                    'taux_tva': 18,
                    'stock_min': 5,
                    'stock_max': 100,
                    'seuil_reapprovisionnement': 10,
                    'est_actif': True,
                }
            )
            if cree:
                compteur_produits += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {compteur_produits} produits créés'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Initialisation terminée avec succès!\n'))
        self.stdout.write('━' * 60)
        self.stdout.write('\n📋 INFORMATIONS DE CONNEXION:\n')
        self.stdout.write('━' * 60)
        self.stdout.write(f'  🌐 URL: http://localhost:8000')
        self.stdout.write(f'  👤 Nom d\'utilisateur: admin')
        self.stdout.write(f'  🔑 Mot de passe: admin123')
        self.stdout.write('━' * 60)
        self.stdout.write(f'\n  ✓ {Client.objects.count()} clients')
        self.stdout.write(f'  ✓ {Fournisseur.objects.count()} fournisseurs')
        self.stdout.write(f'  ✓ {Produit.objects.count()} produits')
        self.stdout.write(f'  ✓ {Categorie.objects.count()} catégories')
        self.stdout.write(f'  ✓ {Entrepot.objects.count()} entrepôt\n')
