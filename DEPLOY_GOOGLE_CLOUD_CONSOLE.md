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

## Guide étape par étape : ajouter les variables d’environnement et Cloud SQL

Suivez ces étapes **dans l’ordre** pour configurer le service **breastcarepro** (variables d’environnement + connexion Cloud SQL).

### Étape 1 : Ouvrir le service Cloud Run

1. Allez sur [Cloud Run](https://console.cloud.google.com/run) (ou recherchez **« Cloud Run »** dans la barre de recherche).
2. Dans la liste des services, cliquez sur le nom **breastcarepro**.

### Étape 2 : Ouvrir la configuration du service (où sont les variables d’environnement)

**Important** : « Modifier les paramètres du dépôt » ouvre le **déclencheur Cloud Build** (source, branche, type de build). Ce n’est **pas** là qu’on met les variables d’environnement.

Pour ajouter les variables d’environnement, il faut éditer le **service** (révision) :

1. Allez sur **Cloud Run** → **Services** → cliquez sur **breastcarepro**.
2. Ouvrez l’onglet **« Révisions »** (Revisions).
3. En haut de la liste des révisions, cliquez sur **« Déployer une nouvelle révision »** (ou **« NEW REVISION »** / **« Deploy new revision »**).  
   **Ou** : cliquez sur le **nom d’une révision** existante, puis sur **« Modifier »** / **« Edit »** si disponible.
4. La page qui s’ouvre contient les paramètres du **conteneur** : onglets **Conteneurs**, **Variables et secrets**, **Connexions**, etc. C’est là que vous ajoutez les variables d’environnement (étape 3 ci‑dessous).

**Si vous ne voyez pas « Déployer une nouvelle révision »** : ouvrez l’onglet **« YAML »** du service. Vous pouvez ajouter les variables sous `spec.template.spec.containers[0].env`. Exemple :

```yaml
env:
  - name: DATABASE_URL
    value: "postgresql://breastcare:MOT_DE_PASSE@/breastcare_db?host=/cloudsql/project-6268991f-ee15-44f6-875:europe-west1:breastcare-db"
  - name: SECRET_KEY
    value: "votre-cle-secrete"
  - name: ENVIRONMENT
    value: "production"
```

Puis enregistrez / déployez.

### Étape 3 : Où définir les variables d’environnement

1. Cliquez sur l’onglet **« Variables et secrets »** (ou **« Variables & Secrets »**).
2. Dans la section **« Variables d’environnement »**, vous verrez soit « Aucune » soit une liste.
3. Cliquez sur **« + Ajouter une variable »** (ou **« ADD VARIABLE »**).
4. Ajoutez **une variable à la fois** comme ci-dessous.

| Nom            | Valeur (à adapter) |
|----------------|--------------------|
| `DATABASE_URL` | `postgresql://breastcare:VOTRE_MOT_DE_PASSE@/breastcare_db?host=/cloudsql/project-6268991f-ee15-44f6-875:europe-west1:breastcare-db` |
| `SECRET_KEY`   | Une longue chaîne aléatoire (ex. 32 caractères) |
| `ENVIRONMENT`  | `production` |

- **DATABASE_URL** : remplacez **VOTRE_MOT_DE_PASSE** par le mot de passe de l’utilisateur **breastcare** que vous avez créé dans Cloud SQL (section Utilisateurs).
- **SECRET_KEY** : inventez une clé secrète (ex. `MaCleSecrete123TresLonguePourJWT!`) ou générez-en une sur [randomkeygen.com](https://randomkeygen.com/) (onglet « Code Key »).
- **ENVIRONMENT** : tapez exactement `production`.

5. Après avoir ajouté les 3 variables, vérifiez qu’elles s’affichent bien dans la liste.

### Étape 4 : Ajouter la connexion Cloud SQL

1. Restez sur la page de modification (ou allez dans l’onglet **« Connexions »** / **« Connections »** selon l’interface).
2. Cherchez la section **« Connexions Cloud SQL »** ou **« Cloud SQL connections »**.
3. Cliquez sur **« Ajouter une connexion »** (ou **« ADD CLOUD SQL CONNECTION »**).
4. Sélectionnez votre instance **breastcare-db** dans la liste.
5. Validez (Enregistrer / OK).

### Étape 5 : Vérifier le port et la mémoire (onglet Conteneurs)

1. Cliquez sur l’onglet **« Conteneurs »** (ou **« CONTAINER »**).
2. Développez la section du conteneur (ex. « breastcarepro ») si besoin.
3. **Port** : vérifiez que **8080** est indiqué (sinon, mettez **8080**).
4. **Mémoire** : mettez au moins **2 Gio** (2 Go) pour le backend avec ML.
5. Optionnel : si disponible, augmentez le **« Délai de démarrage du conteneur »** (Container startup timeout) à **300** secondes.

### Étape 6 : Déployer

1. En bas de la page, cliquez sur **« Déployer »** (ou **« DEPLOY »**).
2. Attendez la fin du déploiement (quelques minutes).
3. Une fois « Révision déployée » ou « Deployment complete », testez l’URL du service (ex. `https://breastcarepro-510831995538.europe-west1.run.app/health`).

---

**Résumé** : Les variables d’environnement se définissent dans **Cloud Run** → service **breastcarepro** → onglet **« Révisions »** → **« Déployer une nouvelle révision »** (ou **YAML**), puis onglet **« Variables et secrets »** → **« Ajouter une variable »**. Pas dans le déclencheur Cloud Build.

---

## Corriger le déclencheur pour que le build parte du dossier backend

Sur la page du **déclencheur** (celle avec Source, Branche, Configuration) :

1. Section **Configuration** :
   - **Type** : au lieu de « Détection automatique », choisissez **« Dockerfile »**.
   - **Emplacement** (ou « Répertoire source » / « Context ») : indiquez **`backend`** pour que le build utilise le dossier `backend/` et le fichier `backend/Dockerfile`.  
     Si l’interface propose **« Fichier Dockerfile »** : mettez **`Dockerfile`** (relatif au répertoire `backend`) ou **`backend/Dockerfile`** si le chemin est relatif à la racine du dépôt.
2. Enregistrez le déclencheur.

Ainsi, le prochain build construira l’image à partir du backend et le build pourra réussir.

---

## Dépannage : « The user-provided container failed to start and listen on PORT=8080 »

Cette erreur apparaît souvent quand **aucune variable d’environnement** n’est définie et/ou **Cloud SQL** n’est pas connecté. Le backend ne peut pas démarrer correctement.

### À faire sur le service Cloud Run (breastcarepro)

1. **Ouvrir le service**  
   Cloud Run → cliquez sur le service **breastcarepro**.

2. **Modifier et déployer une nouvelle révision**  
   Onglet **« Révisions »** ou en haut : **« Modifier et déployer une nouvelle révision »** (Edit & deploy new revision).

3. **Variables d’environnement**  
   Section **« Variables et secrets »** → **« Variables d’environnement »** → **« Ajouter une variable »**. Ajoutez :
   - **`DATABASE_URL`**  
     `postgresql://breastcare:VOTRE_MOT_DE_PASSE@/breastcare_db?host=/cloudsql/project-6268991f-ee15-44f6-875:europe-west1:breastcare-db`  
     (remplacez `VOTRE_MOT_DE_PASSE` par le mot de passe de l’utilisateur `breastcare` dans Cloud SQL.)
   - **`SECRET_KEY`**  
     Une chaîne aléatoire longue (ex. générée sur https://randomkeygen.com/ ou `openssl rand -hex 32`).
   - **`ENVIRONMENT`**  
     `production`

4. **Connexion Cloud SQL**  
   Section **« Connexions »** (ou **Connections**, **Cloud SQL**) → **« Ajouter une connexion »** → sélectionnez l’instance **`breastcare-db`**. Enregistrez.

5. **Port**  
   Dans **« Conteneurs »** → **« Port »**, vérifiez que **8080** est bien indiqué.

6. **Délai de démarrage (optionnel)**  
   Si le backend met longtemps à démarrer (modèles ML), augmentez le **« Délai de démarrage du conteneur »** (Container startup timeout) à **300** secondes ou plus (si l’interface le propose dans Paramètres avancés).

7. **Mémoire**  
   Pour le backend avec ML, mettez au moins **2 Gio** (512 Mio peut être insuffisant au démarrage).

8. **Déployer**  
   Cliquez sur **« Déployer »**. Attendez la fin du déploiement puis testez l’URL du service.

Après avoir poussé les changements du Dockerfile (port 8080, healthcheck), déclenchez un **nouveau build** depuis GitHub (nouveau commit ou « Déclencher un déploiement » dans Cloud Run) pour que l’image soit reconstruite.

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
