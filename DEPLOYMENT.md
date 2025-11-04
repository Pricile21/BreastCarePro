# Guide de Déploiement sur Render

Ce guide vous explique comment déployer l'application BreastCare sur Render.

## Prérequis

- Un compte GitHub (gratuit)
- Un compte Render (gratuit avec limitations)
- Git installé sur votre machine

## Étape 1 : Initialiser Git et pousser sur GitHub

### 1.1 Initialiser le repository Git

```bash
# Initialiser Git
git init

# Ajouter tous les fichiers (sauf ceux dans .gitignore)
git add .

# Créer le premier commit
git commit -m "Initial commit: BreastCare application"
```

### 1.2 Créer un repository sur GitHub

1. Allez sur https://github.com
2. Cliquez sur le bouton "+" en haut à droite → "New repository"
3. Nommez votre repository (ex: `breastcare-app`)
4. Ne cochez PAS "Initialize with README" (vous avez déjà un README)
5. Cliquez sur "Create repository"

### 1.3 Connecter votre projet local à GitHub

```bash
# Remplacez USERNAME et REPO_NAME par vos valeurs
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Renommer la branche principale (si nécessaire)
git branch -M main

# Pousser le code sur GitHub
git push -u origin main
```

## Étape 2 : Créer une base de données PostgreSQL sur Render

1. Connectez-vous sur https://render.com
2. Cliquez sur "New +" → "PostgreSQL"
3. Configurez :
   - **Name** : `breastcare-db` (ou un nom de votre choix)
   - **Database** : `breastcare_db`
   - **User** : `breastcare` (ou laissez par défaut)
   - **Region** : Choisissez la région la plus proche
   - **PostgreSQL Version** : 15
   - **Plan** : Free (pour commencer)
4. Cliquez sur "Create Database"
5. **Important** : Notez les informations de connexion :
   - **Internal Database URL** (pour le backend)
   - **External Database URL** (pour les connexions externes)
   - **Host**, **Port**, **Database**, **User**, **Password**

## Étape 3 : Déployer le Backend (FastAPI)

### 3.1 Créer le service Web Backend

1. Sur Render, cliquez sur "New +" → "Web Service"
2. Connectez votre repository GitHub (autorisez Render à accéder à votre repo)
3. Sélectionnez le repository `breastcare-app`
4. Configurez :
   - **Name** : `breastcare-backend`
   - **Region** : Même région que la base de données
   - **Branch** : `main`
   - **Root Directory** : `backend` (important !)
   - **Environment** : `Docker`
   - **Dockerfile Path** : `backend/Dockerfile`

### 3.2 Configurer les variables d'environnement du Backend

Dans la section "Environment Variables", ajoutez :

```
DATABASE_URL=<votre-internal-database-url-depuis-render>
SECRET_KEY=<générez-une-clé-secrète-forte>
ENVIRONMENT=production
BACKEND_CORS_ORIGINS=https://breastcare-frontend.onrender.com,http://localhost:3000
```

**Pour générer une SECRET_KEY forte :**
```bash
# Sur votre machine locale
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Exemple de DATABASE_URL (fourni par Render) :**
```
postgresql://breastcare:password@dpg-xxxxx-a/breastcare_db
```

**Important** : Remplacez `breastcare-frontend.onrender.com` par l'URL réelle de votre frontend une fois qu'il sera déployé.

### 3.3 Configurer les paramètres avancés

- **Build Command** : (laissez vide, Docker s'en charge)
- **Start Command** : (laissez vide, Docker s'en charge)
- **Auto-Deploy** : `Yes` (déploiement automatique à chaque push)

### 3.4 Créer le service

Cliquez sur "Create Web Service". Le build va prendre 5-10 minutes.

**Note importante** : Attendez que le backend soit complètement déployé avant de créer le frontend, car le frontend a besoin de l'URL du backend.

## Étape 4 : Déployer le Frontend (Next.js)

### 4.1 Créer le service Web Frontend

1. Sur Render, cliquez sur "New +" → "Web Service"
2. Sélectionnez le même repository `breastcare-app`
3. Configurez :
   - **Name** : `breastcare-frontend`
   - **Region** : Même région que les autres services
   - **Branch** : `main`
   - **Root Directory** : `frontend` (important !)
   - **Environment** : `Docker`
   - **Dockerfile Path** : `frontend/Dockerfile`

### 4.2 Configurer les variables d'environnement du Frontend

Dans la section "Environment Variables", ajoutez :

```
NEXT_PUBLIC_API_URL=https://breastcare-backend.onrender.com/api/v1
```

**Important** : Remplacez `breastcare-backend.onrender.com` par l'URL réelle de votre backend (visible dans le dashboard Render).

### 4.3 Configurer les paramètres avancés

- **Build Command** : (laissez vide, Docker s'en charge)
- **Start Command** : (laissez vide, Docker s'en charge)
- **Auto-Deploy** : `Yes`

### 4.4 Créer le service

Cliquez sur "Create Web Service". Le build va prendre 5-10 minutes.

## Étape 5 : Configurer les migrations de base de données

Une fois le backend déployé, vous devez exécuter les migrations Alembic pour créer les tables.

### Option 1 : Via le Shell Render (Recommandé)

1. Dans le dashboard Render, allez sur votre service backend
2. Cliquez sur l'onglet "Shell"
3. Exécutez :
```bash
cd /opt/render/project/src
alembic upgrade head
```

### Option 2 : Via une commande de build

Modifiez le `backend/Dockerfile` pour inclure les migrations automatiquement (optionnel).

## Étape 6 : Vérifier le déploiement

### 6.1 Vérifier le Backend

1. Allez sur l'URL de votre backend : `https://breastcare-backend.onrender.com`
2. Vérifiez la documentation API : `https://breastcare-backend.onrender.com/docs`
3. Testez l'endpoint de santé : `https://breastcare-backend.onrender.com/health`

### 6.2 Vérifier le Frontend

1. Allez sur l'URL de votre frontend : `https://breastcare-frontend.onrender.com`
2. Vérifiez que l'application se charge correctement
3. Testez la connexion au backend

## Étape 7 : Configuration supplémentaire (Optionnel)

### 7.1 Ajouter un domaine personnalisé

Dans les paramètres de chaque service, vous pouvez ajouter un domaine personnalisé.

### 7.2 Configurer les health checks

Les health checks sont déjà configurés dans `docker-compose.yml`, mais vous pouvez les ajuster dans Render.

### 7.3 Configurer les logs

Les logs sont automatiquement disponibles dans le dashboard Render de chaque service.

## Problèmes courants et solutions

### Problème : Le backend ne démarre pas

**Solution** :
- Vérifiez les logs dans le dashboard Render
- Vérifiez que `DATABASE_URL` est correct
- Vérifiez que toutes les variables d'environnement sont définies

### Problème : Le frontend ne peut pas se connecter au backend

**Solution** :
- Vérifiez que `NEXT_PUBLIC_API_URL` pointe vers l'URL correcte du backend
- Vérifiez que le backend est accessible publiquement
- Vérifiez les CORS dans le backend

### Problème : Erreurs de build Docker

**Solution** :
- Vérifiez que les Dockerfiles sont corrects
- Vérifiez que le `Root Directory` est correct dans Render
- Vérifiez les logs de build pour plus de détails

### Problème : La base de données n'est pas accessible

**Solution** :
- Vérifiez que vous utilisez `Internal Database URL` (pas External) dans le backend
- Vérifiez que le backend et la base de données sont dans la même région
- Sur le plan gratuit, les bases de données s'endorment après inactivité (première requête sera lente)

## Mises à jour et redéploiements

À chaque push sur la branche `main`, Render redéploiera automatiquement les services (si `Auto-Deploy` est activé).

Pour déployer manuellement :
1. Allez sur le service dans Render
2. Cliquez sur "Manual Deploy" → "Deploy latest commit"

## Coûts

- **Plan gratuit** : 
  - Services web s'endorment après 15 minutes d'inactivité
  - Base de données s'endort après 90 jours d'inactivité
  - Démarrage lent au réveil (~30 secondes)

- **Plan payant** : 
  - Services toujours actifs
  - Démarrage immédiat
  - Plus de ressources

## Support

Pour toute question :
- Documentation Render : https://render.com/docs
- Support Render : support@render.com
- Logs de déploiement : Disponibles dans le dashboard de chaque service
