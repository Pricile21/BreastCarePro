# Déployer BreastCare Pro depuis la console Google Cloud (GitHub)

Ce guide décrit comment déployer votre code **depuis la console web Google Cloud**, en partant de votre dépôt **GitHub**. Vous n’avez pas besoin d’utiliser les "Solutions de démarrage rapide" du catalogue : on utilise **Cloud Run** + **Cloud SQL** directement.

---

## Ordre des étapes (résumé)

1. Activer les APIs nécessaires  
2. Créer la base PostgreSQL (Cloud SQL)  
3. Déployer le **backend** depuis GitHub (Cloud Run)  
4. Déployer le **frontend** depuis GitHub (Cloud Run)  
5. Configurer l’URL de l’API dans le frontend et CORS

---

## 1. Activer les APIs

1. Ouvrez la **recherche** en haut de la console (icône de recherche ou `/`).  
2. Tapez **"API et services"** → **"Tableau de bord des API"**.  
3. Cliquez sur **"+ Activer des API et des services"**.  
4. Activez une par une :
   - **Cloud Run API**
   - **Cloud SQL Admin API**
   - **Cloud Build API**
   - **Artifact Registry API** (utile pour les images construites par Cloud Build)

Ou en une fois : [Activer les APIs](https://console.cloud.google.com/apis/library?project=project-6268991f-ee15-44f6-875) puis recherchez et activez chacune.

---

## 2. Créer la base PostgreSQL (Cloud SQL)

**Important** : il faut ouvrir la page du **produit Cloud SQL** (où on gère les instances), et non la page « Détails de l’API » Cloud SQL.

1. **Ouvrir Cloud SQL** :
   - Soit dans la **barre de recherche** en haut, tapez **"SQL"** ou **"Cloud SQL"**, puis cliquez sur **"SQL"** dans les résultats (l’entrée avec l’icône base de données, pas « Cloud SQL Admin API »).
   - Soit menu **☰** (hamburger) → **Bases de données** → **SQL**.
   - Lien direct : [console.cloud.google.com/sql](https://console.cloud.google.com/sql)
2. Sur la page **Cloud SQL** (liste des instances, avec le bouton **"Créer une instance"**), cliquez sur **"Créer une instance"**.  
3. Choisissez **"PostgreSQL"** → **"Suivant"**.  
4. Renseignez :
   - **ID de l’instance** : `breastcare-db`
   - **Mot de passe** : définissez un mot de passe pour l’utilisateur `postgres` (notez-le).
   - **Région** : par ex. `europe-west1`.
   - **Type** : "Micro" (db-f1-micro) pour limiter les coûts.
5. Cliquez sur **"Créer une instance"**.  
6. Une fois l’instance créée, ouvrez-la :
   - Onglet **"Bases de données"** → **"Créer une base de données"** → nom : `breastcare_db`.
   - Onglet **"Utilisateurs"** : créez un utilisateur (ex. `breastcare`) avec le même mot de passe que vous utiliserez dans `DATABASE_URL`.

Notez :
- Le **nom de connexion** (format : `votre-projet:europe-west1:breastcare-db`).  
- L’**adresse IP publique** de l’instance (si vous utilisez la connexion par IP) ou le nom de connexion pour la connexion Cloud SQL (socket).

---

## 3. Déployer le backend depuis GitHub (Cloud Run)

1. Dans la recherche, tapez **"Cloud Run"** → **"Cloud Run"**.  
2. Cliquez sur **"Créer un service"**.  
3. **Source du déploiement** :
   - Choisissez **"Continuously deploy from a repository"** (Déployer en continu depuis un dépôt) ou **"Deploy from a repository"**.
   - Cliquez sur **"Configurer une connexion au dépôt"** (ou "Set up with Cloud Build").  
4. **Connexion à GitHub** :
   - Sélectionnez **GitHub** comme fournisseur.
   - Autorisez Google Cloud à accéder à votre compte GitHub si demandé.
   - Choisissez l’**organisation** ou le **compte** puis le **dépôt** BreastCare.
   - Branche : en général **`main`** ou **`master`**.  
5. **Build** :
   - Type de build : **"Dockerfile"**.
   - **Emplacement du Dockerfile** : indiquez le chemin vers le Dockerfile du backend, par ex. **`backend/Dockerfile`** (ou `./backend/Dockerfile` selon l’interface).
   - **Répertoire de contexte** (Context) : **`backend`** (ou le répertoire qui contient le Dockerfile).  
   Si l’interface ne propose qu’un seul champ "Source", mettez le répertoire **backend** comme répertoire source (certaines interfaces construisent alors avec `backend/Dockerfile`).  
6. **Service** :
   - Nom du service : **`backend`**.
   - Région : la même que Cloud SQL (ex. `europe-west1`).  
7. **Variables d’environnement** (bouton "Variables et secrets", "Variables d’environnement") :
   - `DATABASE_URL` :  
     Pour connexion via socket Cloud SQL :  
     `postgresql://breastcare:VOTRE_MOT_DE_PASSE@/breastcare_db?host=/cloudsql/VOTRE_PROJECT_ID:europe-west1:breastcare-db`  
     (remplacez `VOTRE_MOT_DE_PASSE` et `VOTRE_PROJECT_ID`).  
   - `SECRET_KEY` : une clé secrète forte (générée aléatoirement).  
   - `ENVIRONMENT` : `production`.  
8. **Connexion Cloud SQL** (dans "Connexions", "Cloud SQL" ou "Connections") :
   - Ajoutez l’instance **`breastcare-db`** créée à l’étape 2.  
9. **Ressources** (optionnel) :
   - Mémoire : 2 Go, CPU : 2.  
   - Timeout : 300 s (utile pour les analyses longues).  
10. Cliquez sur **"Créer"** ou **"Déployer"**.

Une fois le déploiement terminé, notez **l’URL du service** (ex. `https://backend-xxxxx-ew.a.run.app`).

---

## 4. Déployer le frontend depuis GitHub (Cloud Run)

1. Dans **Cloud Run**, cliquez à nouveau sur **"Créer un service"**.  
2. **Source** : même principe qu’au point 3 :
   - Déploiement depuis le dépôt → connectez le **même dépôt GitHub**.
   - **Répertoire / Dockerfile** : **`frontend`** et **`frontend/Dockerfile`**.  
3. **Build** :
   - Répertoire de contexte : **`frontend`**.
   - **Variable de build** (Build argument) à ajouter si l’interface le permet :
     - Nom : `NEXT_PUBLIC_API_URL`  
     - Valeur : `https://backend-XXXXX-ew.a.run.app/api/v1`  
     (remplacez par l’URL réelle du backend notée à l’étape 3).  
   Si vous ne pouvez pas passer d’argument au build, vous devrez soit redéployer plus tard avec la bonne valeur, soit la définir au build via un fichier `cloudbuild.yaml` (voir ci‑dessous).  
4. **Service** :
   - Nom : **`frontend`**.
   - Région : même que le backend.  
5. Mémoire : 512 Mo suffisent en général.  
6. Cliquez sur **"Créer"** / **"Déployer"**.

Notez **l’URL du frontend** (ex. `https://frontend-xxxxx-ew.a.run.app`).

---

## 5. CORS et URL de l’API

- **Backend** : pour que le navigateur accepte les appels depuis le frontend Cloud Run, ajoutez l’URL du frontend dans CORS.  
  Dans Cloud Run → service **backend** → **"Modifier et déployer une nouvelle révision"** → onglet **Variables et secrets** → variable d’environnement :
  - `BACKEND_CORS_ORIGINS` = `https://frontend-XXXXX-ew.a.run.app`  
  (remplacez par l’URL réelle du frontend). Puis redéployez.

- **Frontend** : la variable `NEXT_PUBLIC_API_URL` doit être définie **au moment du build**. Si vous ne l’aviez pas mise à l’étape 4, modifiez la configuration de déploiement (build) pour ajouter cet argument, puis redéployez le frontend.

---

## Si la console ne propose pas le répertoire (backend / frontend)

Votre projet est un **monorepo** (backend + frontend dans le même dépôt). Certaines interfaces ne permettent pas de choisir un sous-dossier. Dans ce cas :

1. **Option A – Cloud Build**  
   - Menu **Cloud Build** → **Historique** ou **Déclencheurs**.  
   - Créez un déclencheur qui :
     - utilise le dépôt GitHub et la branche voulue ;
     - utilise un fichier **`cloudbuild.yaml`** à la racine du dépôt.  
   Vous pouvez ajouter à la racine un `cloudbuild.yaml` qui construit l’image depuis `backend/` ou `frontend/` et la pousse vers Artifact Registry, puis déploie sur Cloud Run.  

2. **Option B – Deux dépôts GitHub**  
   Copier le dossier `backend` dans un dépôt et `frontend` dans un autre, puis connecter chaque dépôt à Cloud Run (un service par dépôt).

Un fichier **`cloudbuild.yaml`** est fourni à la racine du dépôt. Pour l’utiliser :

1. **Créer le dépôt Artifact Registry** (une seule fois)  
   Recherche → **"Artifact Registry"** → **"Créer un dépôt"** → Nom : `breastcare-repo`, Format : Docker, Région : `europe-west1`.

2. **Modifier les substitutions** dans `cloudbuild.yaml` à la racine :  
   - `_PROJECT_ID` : votre ID de projet (ex. celui de l’URL de votre console).  
   - `_BACKEND_URL` : l’URL du service Cloud Run backend (ex. `https://backend-xxxxx-ew.a.run.app`) **après** avoir déployé le backend une première fois.

3. **Créer un déclencheur Cloud Build**  
   Menu **Cloud Build** → **Déclencheurs** → **Créer un déclencheur** :  
   - Connexion au dépôt GitHub (même dépôt BreastCare).  
   - Branche : `main` (ou votre branche).  
   - Fichier de configuration : **`cloudbuild.yaml`** (à la racine).  
   - Substitutions : renseigner `_PROJECT_ID`, `_REGION`, `_BACKEND_URL` si besoin.

4. **Première fois** : déployer d’abord uniquement le backend (via la console Cloud Run "Deploy from repository" en ciblant le dossier `backend`, ou en exécutant un build qui ne contient que les étapes backend). Puis noter l’URL du backend, la mettre dans `_BACKEND_URL` dans `cloudbuild.yaml`, pousser le commit, et lancer le déclencheur pour construire et déployer le frontend.

---

## Liens directs utiles

- **Cloud Run** : [console.cloud.google.com/run](https://console.cloud.google.com/run)  
- **Cloud SQL** : [console.cloud.google.com/sql](https://console.cloud.google.com/sql)  
- **APIs à activer** : [console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)  

Votre projet actuel :  
[Console – projet](https://console.cloud.google.com/products/solutions/catalog?authuser=1&hl=fr&project=project-6268991f-ee15-44f6-875)

---

## Récap

- Vous **ne passez pas** par les tuiles "Solutions de démarrage rapide" du catalogue pour ce déploiement.
- Vous utilisez **Cloud Run** (créer un service → déployer depuis le dépôt GitHub) pour le backend et le frontend.
- Vous créez **Cloud SQL** une fois, puis vous branchez le backend avec `DATABASE_URL` et la connexion Cloud SQL.
- Avec vos 300 $ de crédit, ce schéma reste raisonnable en coûts si vous gardez une instance Cloud SQL petite et des révisions Cloud Run avec minimum 0 instance quand c’est possible.
