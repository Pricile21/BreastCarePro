# Déployer BreastCare Pro sur Google Cloud

Ce guide vous permet de déployer l’application (frontend Next.js, backend FastAPI, PostgreSQL) sur Google Cloud en utilisant **Cloud Run** et **Cloud SQL**, avec vos **300 $ de crédit gratuit sur 3 mois**.

**Sous Windows** : vous pouvez exécuter les commandes dans **PowerShell** (remplacez `export VAR=value` par `$env:VAR="value"`) ou utiliser **Git Bash** / **WSL** pour garder la syntaxe bash du guide.

## Vue d’ensemble

| Composant   | Service Google Cloud |
|------------|----------------------|
| Backend API | Cloud Run (conteneur) |
| Frontend    | Cloud Run (conteneur) |
| Base de données | Cloud SQL (PostgreSQL 15) |

---

## Prérequis

1. **Compte Google Cloud** avec les 300 $ de crédit activés.
2. **Google Cloud SDK (gcloud)** installé : https://cloud.google.com/sdk/docs/install  
   Après installation, exécutez : `gcloud init` et connectez-vous.
3. **Docker** installé localement (pour construire les images) : https://docs.docker.com/get-docker/

---

## Étape 1 : Créer un projet et activer les APIs

```bash
# Définir un ID de projet (remplacez par le vôtre, ex: breastcare-pro-123456)
export PROJECT_ID=breastcare-pro
export REGION=europe-west1

# Créer le projet (ou utilisez la console Cloud)
gcloud projects create $PROJECT_ID --name="BreastCare Pro"

# Définir le projet actif
gcloud config set project $PROJECT_ID

# Activer la facturation (obligatoire même avec crédit gratuit)
# À faire une fois dans la console : https://console.cloud.google.com/billing

# Activer les APIs nécessaires
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## Étape 2 : Créer la base PostgreSQL (Cloud SQL)

```bash
# Mot de passe pour l'utilisateur PostgreSQL (changez-le en production)
export DB_PASSWORD="VotreMotDePasseSecurise123"

# Créer l'instance Cloud SQL (PostgreSQL 15)
# db-f1-micro est la plus petite instance (économique)
gcloud sql instances create breastcare-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION \
  --root-password=$DB_PASSWORD \
  --storage-type=SSD \
  --storage-size=10GB

# Créer la base de données
gcloud sql databases create breastcare_db --instance=breastcare-db

# Créer l'utilisateur (même nom que dans docker-compose)
gcloud sql users create breastcare \
  --instance=breastcare-db \
  --password=$DB_PASSWORD
```

Récupérer l’**IP de connexion** (pour plus tard) :

```bash
gcloud sql instances describe breastcare-db --format="value(ipAddresses[0].ipAddress)"
```

Notez cette IP : vous en aurez besoin pour `DATABASE_URL`.

---

## Étape 3 : Stocker les secrets (Secret Manager)

```bash
# Générer une clé secrète pour JWT (exemple)
export SECRET_KEY=$(openssl rand -hex 32)

# Créer le secret pour la clé API
echo -n "$SECRET_KEY" | gcloud secrets create SECRET_KEY --data-file=-

# Créer le secret pour le mot de passe DB (optionnel si vous préférez le mettre en variable d'env)
echo -n "$DB_PASSWORD" | gcloud secrets create DB_PASSWORD --data-file=-
```

---

## Étape 4 : Créer le dépôt d’images (Artifact Registry)

```bash
# Créer le dépôt Docker
gcloud artifacts repositories create breastcare-repo \
  --repository-format=docker \
  --location=$REGION \
  --description="BreastCare Pro images"

# Configurer Docker pour s'authentifier
gcloud auth configure-docker $REGION-docker.pkg.dev
```

---

## Étape 5 : Construire et pousser les images

Depuis la **racine du projet** (Breast_Cancer) :

### Backend

```bash
# Construire l'image (peut prendre plusieurs minutes à cause des dépendances ML)
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/breastcare-repo/backend:latest ./backend

# Pousser vers Artifact Registry
docker push $REGION-docker.pkg.dev/$PROJECT_ID/breastcare-repo/backend:latest
```

### Frontend

Vous devez d’abord connaître l’URL du backend Cloud Run. Après le premier déploiement du backend (étape 6), vous obtiendrez une URL du type :  
`https://backend-xxxxx-ew.a.run.app`

Pour le premier déploiement du frontend, vous pouvez utiliser une URL temporaire (à mettre à jour après) :

```bash
# Remplacer BACKEND_URL par l'URL réelle du backend Cloud Run après l'étape 6
export BACKEND_URL=https://backend-XXXXX-ew.a.run.app
# Puis pour le build :
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/breastcare-repo/frontend:latest \
  --build-arg NEXT_PUBLIC_API_URL=$BACKEND_URL/api/v1 \
  ./frontend

docker push $REGION-docker.pkg.dev/$PROJECT_ID/breastcare-repo/frontend:latest
```

---

## Étape 6 : Déployer le backend sur Cloud Run

Construisez l’URL de la base (remplacez `DB_IP` par l’IP de l’étape 2) :

```bash
export DB_IP=$(gcloud sql instances describe breastcare-db --format="value(ipAddresses[0].ipAddress)")
export DATABASE_URL="postgresql://breastcare:${DB_PASSWORD}@${DB_IP}:5432/breastcare_db"
```

Donner à Cloud Run l’accès à Cloud SQL et déployer. **Remplacez** `VOTRE_MOT_DE_PASSE`, `Votre_Secret_Key_Genere` et (après le 1er déploiement) l’URL du frontend pour CORS :

```bash
# Après le déploiement du frontend (étape 7), mettez ici son URL pour CORS, ex:
# export FRONTEND_URL=https://frontend-xxxxx-ew.a.run.app
# Pour le premier déploiement, vous pouvez mettre l'URL du backend temporairement ou *
export FRONTEND_URL=https://frontend-XXXXX-ew.a.run.app

gcloud run deploy backend \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/breastcare-repo/backend:latest \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --add-cloudsql-instances=$PROJECT_ID:$REGION:breastcare-db \
  --set-env-vars="DATABASE_URL=postgresql://breastcare:VOTRE_MOT_DE_PASSE@/breastcare_db?host=/cloudsql/$PROJECT_ID:$REGION:breastcare-db" \
  --set-env-vars="SECRET_KEY=Votre_Secret_Key_Genere" \
  --set-env-vars="ENVIRONMENT=production" \
  --set-env-vars="BACKEND_CORS_ORIGINS=$FRONTEND_URL,https://*.run.app" \
  --memory=2Gi \
  --cpu=2 \
  --timeout=300 \
  --min-instances=0 \
  --max-instances=2
```

**Important** : avec Cloud SQL en mode “connexion Unix”, l’URL correcte est :

```text
postgresql://breastcare:MOT_DE_PASSE@/breastcare_db?host=/cloudsql/PROJECT_ID:REGION:breastcare-db
```

Remplacez `MOT_DE_PASSE` et `PROJECT_ID`/`REGION` par vos valeurs.

À la fin du déploiement, notez l’**URL du service** (ex. `https://backend-xxxxx-ew.a.run.app`).

---

## Étape 7 : Déployer le frontend sur Cloud Run

Utilisez l’URL du backend notée à l’étape 6 :

```bash
export BACKEND_URL=https://backend-XXXXX-ew.a.run.app   # Remplacez par votre URL

# Reconstruire le frontend avec la bonne URL d'API
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/breastcare-repo/frontend:latest \
  --build-arg NEXT_PUBLIC_API_URL=$BACKEND_URL/api/v1 \
  ./frontend

docker push $REGION-docker.pkg.dev/$PROJECT_ID/breastcare-repo/frontend:latest

# Déployer
gcloud run deploy frontend \
  --image=$REGION-docker.pkg.dev/$PROJECT_ID/breastcare-repo/frontend:latest \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --memory=512Mi \
  --min-instances=0 \
  --max-instances=2
```

Notez l’**URL du frontend** (ex. `https://frontend-xxxxx-ew.a.run.app`) : c’est l’URL de votre application.

---

## Connexion Cloud Run → Cloud SQL (détail)

Cloud Run se connecte à Cloud SQL via une **socket Unix** montée par Google. L’URL doit donc utiliser le paramètre `host=/cloudsql/...` et non l’IP publique.

1. Dans la commande `gcloud run deploy backend`, vous avez déjà :
   - `--add-cloudsql-instances=$PROJECT_ID:$REGION:breastcare-db`
   - `DATABASE_URL=postgresql://breastcare:PASSWORD@/breastcare_db?host=/cloudsql/$PROJECT_ID:$REGION:breastcare-db`

2. Si votre backend lit `DATABASE_URL` depuis les variables d’environnement (comme avec docker-compose), cela suffit. Sinon, adaptez `app/core/config.py` ou votre chargement de config pour utiliser cette variable.

3. Pour autoriser Cloud Run à se connecter à l’instance :
   - L’instance Cloud SQL doit avoir l’**API Cloud SQL Admin** activée (déjà fait avec `sqladmin.googleapis.com`).
   - Pas besoin d’activer l’IP publique pour Cloud Run : la connexion passe par le connecteur Cloud SQL.

---

## Résumé des commandes (ordre recommandé)

1. `gcloud init` et `gcloud config set project PROJECT_ID`
2. Activer les APIs (étape 1)
3. Créer Cloud SQL + DB + user (étape 2)
4. Secrets (étape 3)
5. Artifact Registry (étape 4)
6. Build + push **backend** (étape 5)
7. **Deploy backend** (étape 6) → noter l’URL backend
8. Build + push **frontend** avec `NEXT_PUBLIC_API_URL=<URL_BACKEND>/api/v1` (étape 5 + 7)
9. **Deploy frontend** (étape 7)

---

## Coûts estimés (avec 300 $ de crédit)

- **Cloud Run** : facturation à l’usage (requêtes, CPU/mémoire, temps d’exécution). Avec `min-instances=0`, pas de coût quand il n’y a pas de trafic.
- **Cloud SQL** (db-f1-micro) : environ 7–15 $ / mois selon la région.
- **Artifact Registry** : stockage des images, quelques dollars par mois.

Avec un trafic faible à modéré, les 300 $ couvrent largement 3 mois.

---

## Dépannage

- **Backend ne démarre pas** : vérifiez les logs dans la console Cloud Run (Logs) et que `DATABASE_URL` et `SECRET_KEY` sont bien définis.
- **Frontend ne joint pas l’API** : vérifiez que `NEXT_PUBLIC_API_URL` a été défini **au build** (pas seulement au runtime) et que l’URL du backend est correcte.
- **Erreur de connexion à la base** : vérifiez le format de `DATABASE_URL` avec `host=/cloudsql/...` et que `--add-cloudsql-instances` est bien renseigné.

---

## Liens utiles

- [Cloud Run – Déploiement d’un conteneur](https://cloud.google.com/run/docs/deploying)
- [Cloud SQL – Connexion depuis Cloud Run](https://cloud.google.com/sql/docs/postgres/connect-run)
- [Console Google Cloud](https://console.cloud.google.com/)
