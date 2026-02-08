"""
 # ERP MEA - Système de Gestion d'Entreprise

## 📋 Description

Application ERP complète pour la région MEA (Middle East & Africa) développée avec Django et Jinja2.
Toutes les variables et noms sont en français pour une meilleure compréhension.

## 🚀 Installation

### 1. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer la base de données
Modifiez les paramètres dans `settings.py` selon votre configuration PostgreSQL.

### 4. Créer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Initialiser les données de test
```bash
python manage.py initialiser_donnees
```

### 6. Lancer le serveur
```bash
python manage.py runserver
```

### 7. Accéder à l'application
- URL: http://localhost:8000
- Interface admin: http://localhost:8000/admin
- Nom d'utilisateur: admin
- Mot de passe: admin123

## 📦 Modules

### Module Base
- Gestion des clients
- Gestion des fournisseurs
- Configuration de l'entreprise

### Module Stock
- Gestion des produits
- Catégories de produits
- Gestion des entrepôts
- Mouvements de stock (entrées/sorties)

### Module Ventes
- Commandes de vente
- Factures clients
- Gestion des paiements
- Workflow: Brouillon → Confirmé → Expédié → Facturé

### Module Achats
- Commandes d'achat
- Réception des marchandises
- Gestion des fournisseurs

## 🎯 Fonctionnalités

✅ Interface moderne et intuitive en français
✅ Gestion complète des stocks multi-entrepôts
✅ Workflow de vente complet
✅ Calcul automatique des prix et taxes (TVA)
✅ Alertes de rupture de stock
✅ Système de recherche et filtres
✅ Messages de confirmation
✅ Interface d'administration Django
✅ Données de test pré-remplies

## 📁 Structure du projet

erp_mea/
├── base/              # Module de base (clients, fournisseurs)
├── stock/             # Gestion des stocks
├── ventes/            # Gestion des ventes
├── achats/            # Gestion des achats
├── comptabilite/      # Module comptabilité (à développer)
├── templates/         # Templates Jinja2
├── static/            # Fichiers CSS, JS, images
├── media/             # Fichiers uploadés
└── manage.py          # Script Django

## 🔧 Technologies utilisées

- Python 3.10+
- Django 5.0
- Jinja2 (moteur de templates)
- SQLite (base de données)
- CSS3 (design moderne)

## 📝 Convention de nommage

Toutes les variables, fonctions et noms de classes sont en français :
- Modèles: Client, Fournisseur, Produit, CommandeVente, etc.
- Variables: nom, adresse, prix_achat, prix_vente, etc.
- Fonctions: liste_clients(), creer_client(), modifier_client(), etc.
- Templates: liste_clients.jinja, formulaire_client.jinja, etc.

## 🎨 Interface

L'interface utilise un design moderne avec :
- Barre latérale fixe avec navigation
- Cartes statistiques interactives
- Tableaux stylisés
- Formulaires élégants
- Messages de confirmation
- Badges colorés pour les statuts

## 👥 Support

Pour toute question ou assistance, contactez l'équipe de développement.
"""