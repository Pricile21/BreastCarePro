# BreastCare - Plateforme d'Analyse Mammographique avec IA

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-FF6F00?logo=tensorflow)](https://www.tensorflow.org/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript)](https://www.typescriptlang.org/)

**BreastCare** est une plateforme web complète dédiée à l'analyse de mammographies assistée par intelligence artificielle. Le système permet aux professionnels de santé d'uploader des mammographies, d'obtenir des analyses automatiques basées sur l'IA, et de gérer efficacement les dossiers patients.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Technologies utilisées](#technologies-utilisées)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [API Documentation](#api-documentation)
- [Déploiement](#déploiement)
- [Sécurité](#sécurité)
- [Contribution](#contribution)
- [Licence](#licence)

## Fonctionnalités

### Pour les Professionnels de Santé
- **Analyse de mammographies** : Upload et analyse automatique de mammographies avec classification BI-RADS
- **Gestion des patients** : Création, consultation et suivi des dossiers patients
- **Rapports détaillés** : Génération de rapports PDF professionnels avec recommandations
- **Historique complet** : Accès à l'historique de toutes les analyses effectuées
- **Validation d'analyses** : Validation et annotation des résultats d'analyse

### Pour les Patients (Application Mobile)
- **Inscription et authentification** : Création de compte patient sécurisée
- **Consultation des résultats** : Accès aux résultats d'analyses personnelles
- **Éducation** : Articles et ressources éducatives sur le cancer du sein
- **Suivi médical** : Historique personnel des analyses

### Pour les Administrateurs
- **Tableau de bord** : Statistiques complètes sur l'utilisation de la plateforme
- **Gestion des utilisateurs** : Administration des comptes professionnels et patients
- **Gestion des demandes d'accès** : Validation des demandes d'accès professionnel
- **Rapports système** : Monitoring des performances et statistiques

## Architecture

Le projet suit une architecture microservices avec trois composants principaux :

```
┌─────────────────┐
│   Frontend      │  Next.js 14 (React 19)
│   (Port 3000)   │  TypeScript + Tailwind CSS
└────────┬────────┘
         │
         │ HTTP/REST
         │
┌────────▼────────┐
│    Backend      │  FastAPI (Python 3.10)
│   (Port 8000)   │  SQLAlchemy ORM
└────────┬────────┘
         │
         │ PostgreSQL Protocol
         │
┌────────▼────────┐
│   PostgreSQL    │  Database (Port 5432)
│   (Postgres 15) │
└─────────────────┘
```

## Technologies utilisées

### Backend
- **FastAPI** : Framework web moderne et rapide pour l'API
- **SQLAlchemy** : ORM pour la gestion de base de données
- **Alembic** : Migrations de base de données
- **PostgreSQL** : Base de données relationnelle
- **TensorFlow** : Framework d'apprentissage automatique
- **PyTorch** : Bibliothèque d'apprentissage profond
- **Transformers** : Modèles de traitement du langage naturel
- **OpenCV** : Traitement d'images
- **ReportLab** : Génération de rapports PDF

### Frontend
- **Next.js 14** : Framework React avec SSR et SSG
- **React 19** : Bibliothèque UI
- **TypeScript** : Typage statique
- **Tailwind CSS** : Framework CSS utility-first
- **Radix UI** : Composants UI accessibles
- **Shadcn/ui** : Composants UI modernes

### Infrastructure
- **Docker** : Containerisation
- **Docker Compose** : Orchestration multi-conteneurs
- **Nginx** : Reverse proxy (production)

### Intelligence Artificielle
- **MedSigLIP** : Modèle de vision pour l'analyse médicale
- **Classification BI-RADS** : Système de classification standardisé
- **Analyse de densité mammaire** : Détection automatique de la densité

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Docker** (version 20.10 ou supérieure)
- **Docker Compose** (version 2.0 ou supérieure)
- **Git**

Pour un développement local sans Docker :
- **Python 3.10+**
- **Node.js 20+**
- **PostgreSQL 15+**
- **npm** ou **pnpm**

## Installation

### Installation avec Docker (Recommandé)

1. **Cloner le repository**
```bash
git clone <repository-url>
cd Breast_Cancer
```

2. **Lancer l'application avec Docker Compose**
```bash
docker-compose up --build
```

Cette commande va :
- Construire les images Docker pour le backend et le frontend
- Démarrer PostgreSQL
- Initialiser la base de données
- Lancer tous les services

3. **Accéder à l'application**
- Frontend : http://localhost:3000
- Backend API : http://localhost:8000
- Documentation API : http://localhost:8000/docs
- PostgreSQL : localhost:5432

### Installation locale (Développement)

#### Backend

1. **Créer un environnement virtuel**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer la base de données**
```bash
# Créer un fichier .env dans backend/
DATABASE_URL=postgresql://user:password@localhost:5432/breastcare_db
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
```

4. **Lancer les migrations**
```bash
alembic upgrade head
```

5. **Démarrer le serveur**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

1. **Installer les dépendances**
```bash
cd frontend
npm install --legacy-peer-deps
```

2. **Créer un fichier .env.local**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

3. **Démarrer le serveur de développement**
```bash
npm run dev
```

## Configuration

### Variables d'environnement

#### Backend (`backend/.env`)
```env
DATABASE_URL=postgresql://breastcare:password@db:5432/breastcare_db
SECRET_KEY=your-secret-key-change-in-production
ENVIRONMENT=development
```

#### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

#### Docker Compose (`docker-compose.yml`)
Les variables d'environnement sont déjà configurées pour le développement local. Pour la production, modifiez :
- `SECRET_KEY` : Utilisez une clé secrète forte
- `POSTGRES_PASSWORD` : Utilisez un mot de passe sécurisé
- `NEXT_PUBLIC_API_URL` : Ajustez selon votre domaine

### Base de données

Le système crée automatiquement :
- Tables nécessaires via Alembic
- Compte administrateur par défaut :
  - Email : `admin@breastcare.bj`
  - Mot de passe : (configuré dans les migrations)

## Utilisation

### Première connexion

1. **Accéder au dashboard admin**
   - URL : http://localhost:3000/admin/login
   - Utiliser les identifiants administrateur

2. **Créer un compte professionnel**
   - Via le dashboard admin → "Demandes d'accès"
   - Ou directement via l'API

3. **Se connecter en tant que professionnel**
   - URL : http://localhost:3000/professional/login
   - Uploader une mammographie
   - Consulter les résultats

### Upload d'une mammographie

1. Connectez-vous en tant que professionnel
2. Naviguez vers "Upload Mammographie"
3. Sélectionnez un patient ou créez-en un nouveau
4. Uploadez l'image mammographique
5. Attendez l'analyse automatique (quelques secondes)
6. Consultez les résultats avec classification BI-RADS
7. Téléchargez le rapport PDF si nécessaire

### Génération de rapport

1. Accédez à la liste des analyses
2. Cliquez sur "Télécharger le rapport"
3. Le PDF est généré automatiquement avec :
   - Informations patient
   - Résultats de l'analyse
   - Classification BI-RADS
   - Recommandations médicales

## Structure du projet

```
Breast_Cancer/
│
├── backend/                 # Application FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints API
│   │   │   └── v1/
│   │   │       ├── endpoints/  # Routes API
│   │   │       └── api.py      # Router principal
│   │   ├── core/           # Configuration et sécurité
│   │   ├── models/         # Modèles SQLAlchemy
│   │   ├── schemas/        # Schémas Pydantic
│   │   ├── services/       # Logique métier
│   │   ├── ml/             # Modèles d'IA
│   │   │   ├── inference_service_simple.py
│   │   │   └── models/     # Modèles ML
│   │   └── main.py         # Point d'entrée
│   ├── alembic/            # Migrations de base de données
│   ├── requirements.txt    # Dépendances Python
│   └── Dockerfile          # Image Docker backend
│
├── frontend/               # Application Next.js
│   ├── app/                # Pages et routes
│   │   ├── admin/          # Dashboard admin
│   │   ├── professional/   # Interface professionnelle
│   │   ├── mobile/         # Interface patient
│   │   └── api/            # Routes API Next.js
│   ├── components/         # Composants React
│   ├── lib/                # Utilitaires
│   ├── public/             # Assets statiques
│   ├── package.json        # Dépendances Node.js
│   └── Dockerfile          # Image Docker frontend
│
├── articles/               # Articles éducatifs (Markdown)
├── data/                   # Données et uploads
├── docker-compose.yml      # Configuration Docker Compose
└── README.md               # Ce fichier
```

## API Documentation

Une documentation interactive de l'API est disponible à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Endpoints principaux

#### Authentification
- `POST /api/v1/auth/register` - Inscription
- `POST /api/v1/auth/login` - Connexion
- `GET /api/v1/auth/me` - Informations utilisateur

#### Patients
- `GET /api/v1/patients` - Liste des patients
- `GET /api/v1/patients/{id}` - Détails d'un patient
- `POST /api/v1/patients` - Créer un patient

#### Analyses
- `POST /api/v1/mammography/analyze` - Analyser une mammographie
- `GET /api/v1/mammography/analysis/{id}` - Résultats d'analyse
- `POST /api/v1/mammography/validate/{id}` - Valider une analyse

#### Rapports
- `GET /api/v1/professionals/reports` - Liste des rapports
- `GET /api/v1/professionals/reports/{id}/download` - Télécharger un rapport PDF

## Déploiement

### Déploiement sur Render

1. **Préparer le repository**
   - Assurez-vous que toutes les modifications sont commitées
   - Vérifiez que `docker-compose.yml` est correctement configuré

2. **Configurer Render**
   - Créer un nouveau service "Web Service"
   - Connecter votre repository Git
   - Utiliser Docker comme build command
   - Configurer les variables d'environnement

3. **Variables d'environnement sur Render**
```env
DATABASE_URL=<postgresql-url-from-render>
SECRET_KEY=<generate-strong-secret-key>
ENVIRONMENT=production
NEXT_PUBLIC_API_URL=https://your-backend-url.render.com/api/v1
```

### Déploiement avec Docker Compose (Production)

1. **Créer un fichier `docker-compose.prod.yml`**
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    restart: always

  frontend:
    build: ./frontend
    environment:
      - NEXT_PUBLIC_API_URL=${API_URL}
    restart: always

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

volumes:
  postgres_data:
```

2. **Lancer en production**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Sécurité

### Mesures de sécurité implémentées

- **Authentification JWT** : Tokens sécurisés pour l'authentification
- **Hachage des mots de passe** : Utilisation de bcrypt
- **Validation des données** : Validation stricte avec Pydantic
- **CORS configuré** : Restriction des origines autorisées
- **Protection SQL injection** : Utilisation d'ORM avec requêtes paramétrées
- **Variables d'environnement** : Secrets stockés en dehors du code

### Recommandations pour la production

- [ ] Changer `SECRET_KEY` par une clé forte générée aléatoirement
- [ ] Configurer HTTPS avec certificat SSL
- [ ] Mettre en place un rate limiting
- [ ] Activer les logs de sécurité
- [ ] Configurer un firewall
- [ ] Mettre en place des sauvegardes automatiques de la base de données
- [ ] Utiliser des secrets managers (AWS Secrets Manager, HashiCorp Vault)

## Tests

### Tests backend
```bash
cd backend
pytest
```

### Tests frontend
```bash
cd frontend
npm test
```

## Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Standards de code

- Backend : Suivre PEP 8, utiliser Black pour le formatage
- Frontend : Utiliser ESLint et Prettier
- Commits : Messages clairs et descriptifs en français

## Licence

Ce projet est sous licence [MIT](LICENSE) - voir le fichier LICENSE pour plus de détails.

## Auteurs

- **Équipe BreastCare** - Développement initial

## Remerciements

- Modèle MedSigLIP pour l'analyse médicale
- Communauté open source pour les bibliothèques utilisées
- Professionnels de santé pour leurs retours et suggestions

## Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Contacter l'équipe : support@breastcare.bj

## Changelog

### Version 1.0.0 (2025)
- Version initiale
- Analyse de mammographies avec IA
- Gestion complète des patients
- Génération de rapports PDF
- Interface admin, professionnel et patient
- Déploiement Docker

---

<div align="center">

**Fait avec passion pour améliorer la santé des femmes**

[Retour en haut](#breastcare---plateforme-danalyse-mammographique-avec-ia)

</div>
