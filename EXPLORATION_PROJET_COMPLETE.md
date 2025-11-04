# Exploration Approfondie du Projet BreastCare

## 📋 Vue d'Ensemble

**BreastCare Benin Pro** est une plateforme complète d'IA pour le dépistage du cancer du sein, spécifiquement conçue pour l'Afrique (avec focus sur le Bénin). Elle combine des technologies de deep learning pour l'analyse d'images mammographiques avec un système de calcul de risque personnalisé basé sur le modèle Gail.

---

## 🏗️ Architecture Générale

### Stack Technologique

#### Backend
- **Framework** : FastAPI (Python 3.9+)
- **Base de données** : SQLite (actuellement) / PostgreSQL (production)
- **ORM** : SQLAlchemy 2.0
- **Authentification** : JWT (JSON Web Tokens)
- **IA/ML** : 
  - PyTorch 2.1.0
  - TensorFlow 2.15.0
  - Transformers 4.40.0
  - OpenCV 4.8.1
  - Pillow 10.1.0

#### Frontend
- **Framework** : Next.js 15.2.4 (React 19)
- **Langage** : TypeScript 5
- **Styling** : Tailwind CSS 4.1.9
- **UI Components** : Radix UI
- **Cartographie** : Leaflet + React-Leaflet
- **Forms** : React Hook Form + Zod

#### Infrastructure
- **Containerisation** : Docker Compose
- **Base de données** : PostgreSQL 15
- **Cache** : Redis 7
- **Reverse Proxy** : Nginx

---

## 📁 Structure du Projet

```
Breast_Cancer/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── endpoints/          # 10 endpoints principaux
│   │   │   │   ├── auth.py          # Authentification
│   │   │   │   ├── mammography.py  # Analyse d'images
│   │   │   │   ├── patients.py     # Gestion patients
│   │   │   │   ├── professionals.py # Gestion professionnels
│   │   │   │   ├── risk_assessment.py # Calcul risque
│   │   │   │   ├── healthcare_centers.py # Centres de santé
│   │   │   │   ├── appointments.py  # Rendez-vous
│   │   │   │   ├── admin.py        # Administration
│   │   │   │   ├── access_requests.py # Demandes d'accès
│   │   │   │   └── articles.py      # Contenu éducatif
│   │   │   └── api.py              # Routeur principal
│   │   ├── core/
│   │   │   ├── config.py           # Configuration
│   │   │   └── security.py         # Sécurité (JWT, hash)
│   │   ├── db/
│   │   │   ├── session.py          # Session DB
│   │   │   ├── init_db.py          # Initialisation
│   │   │   └── seed_centers.py     # Données Bénin
│   │   ├── models/                 # 8 modèles SQLAlchemy
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   │   ├── mammography.py
│   │   │   ├── professional.py
│   │   │   ├── risk_assessment.py
│   │   │   ├── healthcare_center.py
│   │   │   ├── appointment.py
│   │   │   └── access_request.py
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── services/               # Logique métier
│   │   │   ├── auth_service.py
│   │   │   ├── mammography_service_simple.py
│   │   │   ├── patient_service.py
│   │   │   ├── professional_service.py
│   │   │   ├── risk_assessment_service.py
│   │   │   ├── admin_service.py
│   │   │   └── access_request_service.py
│   │   └── ml/                     # Intelligence Artificielle
│   │       ├── inference_service_simple.py # Modèle MedSigLIP
│   │       ├── gail_risk_calculator.py     # Modèle Gail (NCI)
│   │       ├── api_risk_calculator.py      # API risque
│   │       ├── medsiglip_model.py          # Architecture modèle
│   │       └── model/
│   │           └── best_medsiglip_model.pth # Modèle entraîné
│   └── main.py                     # Point d'entrée FastAPI
│
├── frontend/
│   ├── app/
│   │   ├── mobile/                 # Application mobile patient
│   │   │   ├── login/
│   │   │   ├── signup/
│   │   │   ├── dashboard/
│   │   │   ├── assessment/         # Évaluation risque
│   │   │   ├── booking/            # Prise RDV
│   │   │   ├── education/          # Articles éducatifs
│   │   │   ├── providers/          # Liste professionnels
│   │   │   └── page.tsx             # Page d'accueil
│   │   ├── professional/           # Interface professionnel
│   │   │   ├── login/
│   │   │   ├── dashboard/
│   │   │   ├── patients/
│   │   │   ├── upload/             # Upload mammographies
│   │   │   ├── analysis/[id]/      # Détails analyse
│   │   │   ├── reports/            # Rapports
│   │   │   └── settings/
│   │   ├── admin/                  # Interface admin
│   │   │   ├── login/
│   │   │   ├── dashboard/
│   │   │   ├── users/
│   │   │   ├── requests/
│   │   │   ├── analytics/
│   │   │   └── settings/
│   │   └── page.tsx                # Page principale
│   ├── components/
│   │   ├── ui/                     # 40+ composants UI
│   │   ├── auth-guard.tsx          # Protection routes
│   │   ├── admin-sidebar.tsx
│   │   └── professional-sidebar.tsx
│   ├── contexts/
│   │   └── auth-context.tsx        # État authentification
│   ├── hooks/
│   │   └── use-api.ts              # Hook API
│   └── lib/
│       ├── api.ts                  # Client API
│       └── utils.ts
│
└── docker-compose.yml              # Orchestration services
```

---

## 🎯 Fonctionnalités Principales

### 1. **Authentification Multi-Plateforme**

#### Système à 3 types d'utilisateurs :
- **Patients** (`user_type: "patient"`) : Application mobile
- **Professionnels** (`user_type: "professional"`) : Interface professionnelle
- **Administrateurs** (`user_type: "admin"`) : Interface admin

#### Sécurité :
- **JWT Tokens** avec expiration (8 jours)
- **Hashage bcrypt** des mots de passe
- **Blocage croisé** : Admins bloqués sur mobile, patients bloqués sur admin
- **Gestion sessions** via localStorage

#### Endpoints :
- `POST /api/v1/auth/login` - Connexion (avec paramètre `source`)
- `POST /api/v1/auth/register` - Inscription professionnels
- `POST /api/v1/auth/mobile-signup` - Inscription patients
- `GET /api/v1/auth/me` - Profil utilisateur
- `POST /api/v1/auth/forgot-password` - Réinitialisation
- `POST /api/v1/auth/reset-password` - Nouveau mot de passe

---

### 2. **Analyse de Mammographies par IA**

#### Modèle MedSigLIP :
- **Architecture** : Modèle vision-language adapté au médical
- **Fichier** : `best_medsiglip_model.pth`
- **Classification BI-RADS** : Catégories 1-5
- **Détection de vues** : Classifieur spécialisé (CC, MLO, etc.)
- **Annotations** : Utilisation de CSV d'annotations VinDr-Mammo

#### Fonctionnalités :
- Upload multiples fichiers
- Classification automatique BI-RADS
- Score de confiance (0-1)
- Détection densité mammaire
- Localisation zones d'intérêt (bounding boxes)
- Détection findings (anomalies)

#### Service d'inference :
```python
MedSigLIPInferenceService
├── load_model()           # Chargement modèle PyTorch
├── load_view_classifier() # Classifieur de vues
├── load_annotations()     # CSV VinDr annotations
├── predict_single_image() # Prédiction image unique
└── predict_batch()        # Prédiction batch
```

#### Endpoints :
- `POST /api/v1/mammography/analyze` - Analyser images
- `GET /api/v1/mammography/analysis/{id}` - Résultat analyse
- `GET /api/v1/mammography/history/{patient_id}` - Historique
- `GET /api/v1/mammography/image/{path}` - Servir images

---

### 3. **Calcul de Risque Personnalisé (Modèle Gail)**

#### Modèle Gail Officiel (NCI) :
- **Validation scientifique** : Basé sur études NCI
- **Coefficients β** : Provenant de publications officielles
- **Variables principales** :
  - Âge
  - Antécédents familiaux (1er degré)
  - Biopsies précédentes
  - Hyperplasie atypique
  - Âge ménarche
  - Âge premier enfant
  - Facteurs mode de vie (IMC, alcool, exercice, tabac, hormonothérapie)

#### Calculs :
- **Risque 5 ans** : Risque absolu sur 5 ans (%)
- **Risque lifetime** : Risque à vie (optionnel)
- **Risque relatif** : Multiplicateur vs population moyenne
- **Ajustements mode de vie** : Impact positif/négatif

#### Service :
```python
GailModelRiskCalculator
├── _calculate_relative_risk_official()
├── _calculate_absolute_risk_5_years_official()
├── _adjust_for_lifestyle_factors()
└── calculate_comprehensive_risk()
```

#### Endpoints :
- `POST /api/v1/risk/calculate` - Calcul complet
- `POST /api/v1/risk/calculate-and-save` - Calcul + sauvegarde
- `GET /api/v1/risk/my-assessments` - Historique évaluations
- `GET /api/v1/risk/assessments/{id}` - Détails évaluation
- `GET /api/v1/risk/factors` - Liste facteurs de risque

---

### 4. **Gestion des Patients**

#### Modèle Patient :
```python
Patient
├── patient_id (unique)
├── full_name
├── date_of_birth / age
├── phone_number
├── address
├── medical_history
├── family_history
├── emergency_contact
└── notes
```

#### Fonctionnalités :
- Création patient par professionnel
- Historique analyses
- Liaison avec utilisateur
- Gestion notes médicales

#### Endpoints :
- `POST /api/v1/patients/` - Créer
- `GET /api/v1/patients/{id}` - Détails
- `PUT /api/v1/patients/{id}` - Modifier
- `GET /api/v1/patients/` - Liste

---

### 5. **Gestion des Professionnels de Santé**

#### Modèle Professional :
```python
Professional
├── full_name
├── specialty (ex: "Nuclear Medicine", "Radiology")
├── license_number (unique)
├── phone_number, email, address
├── latitude, longitude (géolocalisation)
├── consultation_fee
├── languages
├── is_active
└── is_verified
```

#### Fonctionnalités :
- Création profil professionnel
- Géolocalisation
- Recherche proximité
- Vérification licence
- Dashboard professionnel

#### Endpoints :
- `POST /api/v1/professionals/` - Créer
- `GET /api/v1/professionals/me` - Profil connecté
- `GET /api/v1/professionals/{id}` - Détails
- `PUT /api/v1/professionals/{id}` - Modifier
- `GET /api/v1/professionals/nearby` - Recherche géographique
- `GET /api/v1/professionals/dashboard/stats` - Statistiques
- `GET /api/v1/professionals/reports` - Rapports

---

### 6. **Centres de Santé (Bénin)**

#### Modèle HealthcareCenter :
```python
HealthcareCenter
├── name
├── type (hôpital, clinique, etc.)
├── address, city, department
├── latitude, longitude
├── phone_number, email, website
├── services (liste)
├── equipment (liste)
├── specialties (liste)
├── operating_hours (JSON)
├── languages_spoken
├── rating, total_reviews
├── is_available
├── is_verified
└── accepts_appointments
```

#### Données pré-chargées :
- **67 centres béninois** dans la base
- Répartis sur plusieurs départements
- Coordonnées GPS réelles
- Services disponibles

#### Endpoints :
- `GET /api/v1/healthcare-centers/` - Liste (filtres multiples)
- `GET /api/v1/healthcare-centers/{id}` - Détails
- `GET /api/v1/healthcare-centers/nearby/search` - Recherche géographique
- `POST /api/v1/healthcare-centers/` - Créer
- `PUT /api/v1/healthcare-centers/{id}` - Modifier

---

### 7. **Prise de Rendez-vous**

#### Modèle Appointment :
```python
Appointment
├── center_id
├── user_id (optionnel)
├── patient_name
├── patient_phone
├── patient_email
├── appointment_date
├── appointment_time
├── notes
├── status (pending, confirmed, cancelled)
└── confirmation_code
```

#### Endpoints :
- `POST /api/v1/appointments/` - Créer RDV
- `GET /api/v1/appointments/` - Liste (filtres)
- `GET /api/v1/appointments/{id}` - Détails

---

### 8. **Contenu Éducatif**

#### Modèle Article :
```python
Article
├── title
├── content
├── category
├── author
├── published_at
├── image_url
└── is_published
```

#### Catégories :
- Prévention
- Dépistage
- Traitement
- Témoignages
- Actualités

#### Endpoints :
- `GET /api/v1/articles/` - Liste
- `GET /api/v1/articles/{id}` - Détails
- `GET /api/v1/articles/categories/list` - Catégories

---

### 9. **Administration**

#### Fonctionnalités Admin :
- **Gestion utilisateurs** : Liste, activation/désactivation, reset password
- **Gestion demandes d'accès** : Approbation/rejet professionnels
- **Statistiques système** : Dashboard complet
- **Export données** : Rapports CSV
- **Notifications** : Système d'alertes

#### Endpoints Admin :
- `GET /api/v1/admin/dashboard/stats` - Stats générales
- `GET /api/v1/admin/users` - Liste utilisateurs
- `PUT /api/v1/admin/users/{id}/status` - Activer/Désactiver
- `DELETE /api/v1/admin/users/{id}` - Supprimer
- `POST /api/v1/admin/users/{id}/reset-password` - Reset
- `GET /api/v1/admin/access-requests` - Demandes
- `PUT /api/v1/admin/access-requests/{id}` - Traiter
- `GET /api/v1/admin/system-stats` - Stats système
- `GET /api/v1/admin/analyses/summary` - Résumé analyses
- `GET /api/v1/admin/reports/export` - Export CSV

---

## 🔐 Sécurité et Authentification

### Système JWT :
```python
create_access_token(subject=user.id, expires_delta=8_days)
verify_password(password, hashed_password)
get_password_hash(password)  # bcrypt
```

### Middleware :
- **CORS** : Configuration multi-origines
- **Logging** : Toutes requêtes loggées
- **Trusted Hosts** : Protection contre host header attacks

### Restrictions par plateforme :
- Mobile : `source='mobile'` → Bloque admins (403)
- Professional : Accès professionnels uniquement
- Admin : Accès administrateurs uniquement

---

## 🗄️ Modèle de Données

### Relations principales :

```
User (users)
├── 1:N → Patient (patients.user_id)
├── 1:N → MammographyAnalysis (analyses.user_id)
├── 1:N → RiskAssessment (risk_assessments.user_id)
└── N:1 → Professional (users.professional_id)

Patient (patients)
├── N:1 → User (patients.user_id)
└── 1:N → MammographyAnalysis (analyses.patient_id)

MammographyAnalysis (mammography_analyses)
├── N:1 → Patient
└── N:1 → User

Professional (professionals)
├── N:1 → User (via users.professional_id)
└── (peut avoir plusieurs patients)

HealthcareCenter (healthcare_centers)
└── 1:N → Appointment (appointments.center_id)

Appointment (appointments)
└── N:1 → HealthcareCenter

AccessRequest (access_requests)
└── (Demande d'accès professionnel)
```

---

## 🌐 API Endpoints Complets

### Authentification (8 endpoints)
- `OPTIONS /auth/login`, `/auth/me` - CORS
- `POST /auth/login` - Connexion
- `POST /auth/register` - Inscription pro
- `POST /auth/mobile-signup` - Inscription mobile
- `GET /auth/me` - Profil
- `POST /auth/forgot-password` - Oubli
- `POST /auth/reset-password` - Reset

### Mammographie (4 endpoints)
- `POST /mammography/analyze` - Analyser
- `GET /mammography/analysis/{id}` - Résultat
- `GET /mammography/history/{patient_id}` - Historique
- `GET /mammography/image/{path}` - Image

### Patients (4 endpoints)
- `POST /patients/` - Créer
- `GET /patients/{id}` - Détails
- `PUT /patients/{id}` - Modifier
- `GET /patients/` - Liste

### Professionnels (12 endpoints)
- `POST /professionals/` - Créer
- `GET /professionals/me` - Profil
- `GET /professionals/{id}` - Détails
- `PUT /professionals/{id}` - Modifier
- `GET /professionals/nearby` - Proximité
- `GET /professionals/` - Liste
- `GET /professionals/dashboard/stats` - Stats
- `GET /professionals/reports` - Rapports
- `GET /professionals/reports/{id}` - Détail rapport
- `POST /professionals/reports/{id}/download` - Télécharger

### Centres de santé (5 endpoints)
- `GET /healthcare-centers/` - Liste
- `GET /healthcare-centers/{id}` - Détails
- `GET /healthcare-centers/nearby/search` - Recherche
- `POST /healthcare-centers/` - Créer
- `PUT /healthcare-centers/{id}` - Modifier

### Rendez-vous (3 endpoints)
- `POST /appointments/` - Créer
- `GET /appointments/` - Liste
- `GET /appointments/{id}` - Détails

### Évaluation Risque (5 endpoints)
- `POST /risk/calculate` - Calculer
- `POST /risk/calculate-and-save` - Calculer + sauver
- `GET /risk/my-assessments` - Mes évaluations
- `GET /risk/assessments/{id}` - Détails
- `GET /risk/factors` - Facteurs

### Articles (3 endpoints)
- `GET /articles/` - Liste
- `GET /articles/{id}` - Détails
- `GET /articles/categories/list` - Catégories

### Administration (15+ endpoints)
- Dashboard, utilisateurs, demandes, stats, exports, etc.

### Demandes d'accès (6 endpoints)
- CRUD complet + approbation/rejet

### Endpoints spéciaux :
- `GET /real-patients` - Vraies données patients
- `GET /real-reports` - Vraies données rapports
- `GET /real-dashboard-stats` - Vraies stats
- `GET /real-recent-analyses` - Analyses récentes
- `GET /real-alerts` - Alertes réelles
- `GET /real-professional` - Données professionnel
- `POST /clean-database` - Nettoyage DB (dev)

---

## 📱 Interfaces Frontend

### 1. Application Mobile (`/mobile/*`)

#### Pages :
- **Page d'accueil** (`/mobile`) : Landing page avec présentation
- **Login** (`/mobile/login`) : Connexion patients
- **Signup** (`/mobile/signup`) : Inscription patients
- **Dashboard** (`/mobile/dashboard`) : Tableau de bord utilisateur
- **Évaluation** (`/mobile/assessment`) : Questionnaire risque (modèle Gail)
- **Résultats** (`/mobile/assessment/results`) : Résultats évaluation
- **Booking** (`/mobile/booking`) : Prise de rendez-vous
- **Confirmation** (`/mobile/booking/confirmation`) : Confirmation RDV
- **Providers** (`/mobile/providers`) : Liste professionnels
- **Provider Details** (`/mobile/providers/[id]`) : Détails professionnel
- **Education** (`/mobile/education`) : Liste articles
- **Article** (`/mobile/education/article/[id]`) : Détails article
- **Forgot Password** (`/mobile/forgot-password`) : Oubli mot de passe
- **Reset Password** (`/mobile/reset-password`) : Réinitialisation

#### Composants clés :
- Formulaire évaluation multi-étapes
- Carte géographique (Leaflet) pour centres
- Graphiques de risque (Recharts)
- Design responsive mobile-first

---

### 2. Interface Professionnelle (`/professional/*`)

#### Pages :
- **Login** (`/professional/login`) : Connexion professionnels
- **Dashboard** (`/professional/dashboard`) : Stats et analyses récentes
- **Patients** (`/professional/patients`) : Liste patients
- **Upload** (`/professional/upload`) : Upload mammographies
- **Analysis** (`/professional/analysis/[id]`) : Détails analyse
- **Reports** (`/professional/reports`) : Liste rapports
- **Settings** (`/professional/settings`) : Paramètres
- **Request Access** (`/professional/request-access`) : Demande accès

#### Fonctionnalités :
- Upload multiples images
- Visualisation résultats BI-RADS
- Tableaux statistiques
- Graphiques de tendances
- Export rapports PDF

---

### 3. Interface Administration (`/admin/*`)

#### Pages :
- **Login** (`/admin/login`) : Connexion admin
- **Dashboard** (`/admin/dashboard`) : Vue d'ensemble système
- **Users** (`/admin/users`) : Gestion utilisateurs
  - `/admin/users/mobile` : Patients
  - `/admin/users/professionals` : Professionnels
- **Requests** (`/admin/requests`) : Demandes d'accès
- **Analytics** (`/admin/analytics`) : Statistiques avancées
- **Settings** (`/admin/settings`) : Configuration système

#### Fonctionnalités :
- Graphiques analytics
- Gestion utilisateurs (activate/deactivate)
- Approuver/rejeter demandes
- Export données
- Monitoring système

---

## 🤖 Intelligence Artificielle

### 1. Modèle MedSigLIP (Mammographie)

#### Architecture :
- Modèle vision-language adapté médical
- Classification BI-RADS (1-5)
- Détection de vues (CC, MLO, etc.)
- Localisation anomalies (bounding boxes)

#### Pipeline :
```
Image Input
  ↓
Preprocessing (OpenCV, PIL)
  ↓
View Classification (classifier spécialisé)
  ↓
MedSigLIP Inference (best_medsiglip_model.pth)
  ↓
BI-RADS Classification
  ↓
Confidence Score
  ↓
Findings Detection (annotations CSV)
  ↓
Output JSON
```

#### Fichiers :
- `app/ml/model/best_medsiglip_model.pth` - Modèle principal
- `app/ml/model/view_classifier_trained.pth` - Classifieur vues
- `breast-level_annotations (1).csv` - Annotations VinDr
- `finding_annotations (1).csv` - Annotations findings

---

### 2. Modèle Gail (Calcul Risque)

#### Validation :
- ✅ Basé sur NCI (National Cancer Institute)
- ✅ Coefficients validés scientifiquement
- ✅ Compatible calculateur officiel : bcrisktool.cancer.gov

#### Variables :
- **Obligatoires** : Âge, antécédents familiaux, biopsies, ménarche, premier enfant
- **Optionnelles (mode de vie)** : IMC, alcool, exercice, tabac, hormonothérapie

#### Calculs :
- Risque relatif (RR multiplier)
- Risque absolu 5 ans (%)
- Ajustements mode de vie
- Comparaison population moyenne

---

## 🔄 Flux de Données

### Connexion Mobile :
```
Frontend /mobile/login
  ↓ (email, password, source='mobile')
API Client.login()
  ↓
POST /api/v1/auth/login
  ↓
AuthService.authenticate_user()
  ↓
Vérification type utilisateur
  ↓
Si admin → 403 Forbidden
Si patient/pro → JWT Token
  ↓
localStorage.setItem('auth_token')
  ↓
checkAuth() → GET /auth/me
  ↓
Redirection /mobile/dashboard
```

### Analyse Mammographie :
```
Frontend Upload
  ↓ (files[], patient_id)
POST /api/v1/mammography/analyze
  ↓
MammographyService.analyze_mammography()
  ↓
Sauvegarde fichiers (uploads/)
  ↓
MedSigLIPInferenceService.predict_batch()
  ↓
Classification BI-RADS
  ↓
Sauvegarde DB (MammographyAnalysis)
  ↓
Retour résultats JSON
```

### Évaluation Risque :
```
Frontend /mobile/assessment
  ↓ (Formulaire multi-étapes)
POST /api/v1/risk/calculate
  ↓
GailModelRiskCalculator.calculate_comprehensive_risk()
  ↓
Calcul risque 5 ans
Ajustements mode de vie
Catégorisation risque
  ↓
Sauvegarde DB (RiskAssessment)
  ↓
Retour résultats + recommandations
```

---

## 🗺️ Géolocalisation

### Données :
- **67 centres béninois** avec coordonnées GPS
- Professionnels avec latitude/longitude
- Recherche par proximité (radius_km)

### Technologies :
- **Leaflet** : Cartes interactives
- **React-Leaflet** : Composants React
- **Calcul distance** : Haversine formula

---

## 📊 Base de Données

### Tables principales :
1. `users` - Utilisateurs (patients, pros, admins)
2. `patients` - Informations patients
3. `professionals` - Professionnels santé
4. `mammography_analyses` - Analyses mammographies
5. `risk_assessments` - Évaluations risque
6. `healthcare_centers` - Centres de santé
7. `appointments` - Rendez-vous
8. `access_requests` - Demandes d'accès
9. `articles` - Contenu éducatif

### Migration :
- SQLite en développement
- PostgreSQL en production
- Alembic pour migrations (si nécessaire)
- Initialisation auto au startup

---

## 🚀 Déploiement

### Docker Compose :
```yaml
Services:
  - backend (FastAPI)
  - frontend (Next.js)
  - db (PostgreSQL)
  - redis (Cache)
  - nginx (Reverse Proxy)
```

### Variables d'environnement :
- `DATABASE_URL`
- `SECRET_KEY`
- `NEXT_PUBLIC_API_URL`
- `BACKEND_CORS_ORIGINS`
- `SMTP_*` (Email)

---

## 📈 Métriques et Monitoring

### Logging :
- Toutes requêtes HTTP loggées
- Logs détaillés authentification
- Erreurs avec stack traces

### Statistiques :
- Dashboard admin avec métriques système
- Statistiques professionnels (analyses, patients)
- Analytics avancées

---

## 🔧 Configuration et Développement

### Backend :
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend :
```bash
cd frontend
npm install
npm run dev
```

### Base de données :
- Initialisation auto au démarrage
- Seed centres béninois automatique
- Migrations SQLite automatiques

---

## 🎨 Design System

### Frontend :
- **Tailwind CSS** : Utility-first CSS
- **Radix UI** : Composants accessibles
- **Lucide React** : Icons
- **Recharts** : Graphiques
- **Dark Mode** : Support thème sombre

### Composants UI :
- 40+ composants réutilisables
- Design cohérent
- Responsive mobile-first
- Accessibilité (ARIA)

---

## 📝 Documentation

### Fichiers MD :
- `LOGIN_LOGIC_MOBILE.md` - Logique connexion
- `README.md` - Documentation principale
- `backend/README.md` - Documentation backend
- Documentation ML dans `backend/app/ml/`

### API :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

---

## 🔍 Points d'Attention et Améliorations

### Actuel :
1. **SQLite en dev** : Migrer vers PostgreSQL en prod
2. **Modèle ML** : Validation continue des performances
3. **Sécurité** : Renforcer validation inputs
4. **Tests** : Ajouter tests unitaires/intégration
5. **Email** : Configurer service SMTP réel
6. **Cache Redis** : Implémenter cache stratégique

### Futures améliorations :
- App mobile native (React Native)
- Notification push
- Téléconsultation
- Export PDF rapports
- Multi-langues (Français/Anglais)
- Intégration paiement

---

## 📚 Technologies et Bibliothèques Clés

### Backend :
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PyTorch 2.1.0
- TensorFlow 2.15.0
- Transformers 4.40.0
- OpenCV 4.8.1
- Pydantic
- Python-JOSE (JWT)
- Passlib (bcrypt)

### Frontend :
- Next.js 15.2.4
- React 19
- TypeScript 5
- Tailwind CSS 4.1.9
- Radix UI (40+ composants)
- React Hook Form
- Zod (validation)
- Leaflet (cartes)
- Recharts (graphiques)

---

## 🎯 Cas d'Usage Principaux

### Patient Mobile :
1. S'inscrire / Se connecter
2. Remplir évaluation risque (Gail)
3. Voir résultats + recommandations
4. Chercher professionnel/centre
5. Prendre rendez-vous
6. Lire articles éducatifs
7. Suivre analyses (si liée à un pro)

### Professionnel :
1. S'inscrire (demande accès)
2. Se connecter (après approbation admin)
3. Créer patients
4. Upload mammographies
5. Analyser images (IA)
6. Voir résultats BI-RADS
7. Générer rapports
8. Gérer patients
9. Dashboard statistiques

### Administrateur :
1. Se connecter
2. Approuver/rejeter demandes
3. Gérer utilisateurs (activate/deactivate)
4. Voir statistiques système
5. Exporter données
6. Gérer articles
7. Monitoring

---

## 🏥 Contexte Médical

### BI-RADS Catégories :
- **BI-RADS 1** : Négatif, rien à signaler
- **BI-RADS 2** : Bénin, pas de suspicion
- **BI-RADS 3** : Probablement bénin, suivi à court terme
- **BI-RADS 4** : Suspicion modérée, biopsie recommandée
- **BI-RADS 5** : Suspicion élevée, action recommandée

### Modèle Gail :
- Validé scientifiquement (NCI)
- Utilisé dans pratique clinique
- Calcul risque personnalisé
- Recommandations basées sur risque

---

Ce document fournit une vue complète et approfondie du projet BreastCare. Pour des détails spécifiques sur une fonctionnalité, consultez les fichiers source correspondants.

