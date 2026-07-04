# ERP MEA — Système de gestion d'entreprise (MEA)

## À propos
ERP MEA est une solution ERP conçue pour les pays du Middle East & Africa (MEA). Développée avec Django et Jinja2, l'application couvre les besoins métier essentiels : gestion des clients et fournisseurs, stocks multi-entrepôts, ventes, achats, et un module comptabilité en cours de développement. L'ensemble des modèles, des variables et des interfaces est en français afin de faciliter l'adoption par les équipes locales.

---

## Fonctionnalités principales

- Gestion clients et fournisseurs
- Gestion produits, catégories et entrepôts
- Mouvements de stock (entrées / sorties) et alertes de rupture
- Processus complet de ventes (Brouillon → Confirmé → Expédié → Facturé)
- Commandes d'achat et réceptions fournisseurs
- Calcul automatique des prix et des taxes (TVA)
- Interface d'administration Django
- Données de démonstration pré-remplies

---

## Technologies

- Python 3.10+
- Django 5.x
- Jinja2 (templates)
- PostgreSQL (recommandé en production) — SQLite possible en développement
- HTML5 / CSS3 pour le front-end

---

## Prérequis

- Python 3.10 ou supérieur
- pip
- PostgreSQL pour une installation production (ou SQLite pour développement)

---

## Installation — guide rapide

1. Cloner le dépôt

```bash
git clone https://github.com/jean-jacques-komhidi/erp-mea.git
cd erp-mea
```

2. Créer et activer un environnement virtuel

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. Installer les dépendances

```bash
pip install -r requirements.txt
```

4. Configurer la base de données

- Modifiez les paramètres de connexion dans `settings.py` ou utilisez des variables d'environnement (HOST, PORT, NAME, USER, PASSWORD).

5. Créer les migrations et appliquer la base

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Charger des données de démonstration (optionnel)

```bash
python manage.py initialiser_donnees
```

7. Lancer le serveur

```bash
python manage.py runserver
```

Accès :
- Application : http://localhost:8000
- Interface d'administration : http://localhost:8000/admin
- Compte d'exemple (si fourni) : `admin` / `admin123` — changez impérativement les identifiants en production.

---

## Structure du projet

```
erp_mea/
├── base/              # Clients, fournisseurs, configuration entreprise
├── stock/             # Produits, entrepôts, mouvements de stock
├── ventes/            # Commandes, factures, paiements
├── achats/            # Commandes d'achat, réceptions
├── comptabilite/      # Module comptabilité (en développement)
├── templates/         # Templates Jinja2
├── static/            # CSS, JS, images
├── media/             # Fichiers uploadés
└── manage.py          # Entrée Django
```

---

## Conventions

- Langue: français pour les modèles, variables et fonctions
- Exemples: Modèles — Client, Fournisseur, Produit, CommandeVente
- Fonctions usuelles: `liste_clients()`, `creer_client()`, `modifier_client()`
- Templates: `liste_clients.jinja`, `formulaire_client.jinja`

---

## Recommandations pour la production

- Utiliser PostgreSQL en production
- Gérer les secrets via des variables d'environnement ou un gestionnaire de secrets
- Mettre `DEBUG = False`
- Déployer avec gunicorn/uvicorn derrière un reverse proxy (Nginx)
- Activer HTTPS et mettre en place des sauvegardes régulières
- Mettre en place une CI pour tests et linting

---

## Contribution

Les contributions sont les bienvenues :

1. Créez une branche descriptive (ex. `feature/` ou `fix/`).
2. Soumettez une pull request avec une description claire des changements.
3. Ajoutez des tests et mettez à jour la documentation si nécessaire.

---

## Support

Ouvrez une issue sur le dépôt GitHub pour toute question ou demande d'aide.

---

## Licence

Indiquez la licence du projet (ex. MIT, Apache-2.0). Si aucune licence n'est définie, précisez les conditions d'utilisation.
