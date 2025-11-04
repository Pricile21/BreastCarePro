# Guide de déploiement sur Render

Ce guide vous explique comment déployer votre application BreastCare sur Render.

## Architecture du déploiement

- **Backend**: Service Web Python (FastAPI + Uvicorn)
- **Base de données**: PostgreSQL (Render managed)
- **Disque persistant**: Pour stocker les fichiers uploadés et le modèle ML
- **Frontend**: Déployé séparément sur Vercel (recommandé) ou Render

## Prérequis

1. Un compte [Render.com](https://render.com) (gratuit pour commencer)
2. Votre code sur GitHub/GitLab/Bitbucket
3. Copie de votre base de données SQLite (pour migration)

## Étapes de déploiement

### 1. Préparer votre repository

Votre structure de fichiers doit être :
```
Breast_Cancer/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── render.yaml
│   └── breastcare.db (pour migration)
├── frontend/
└── README.md
```

### 2. Créer un nouveau service sur Render

1. Allez sur [dashboard.render.com](https://dashboard.render.com)
2. Cliquez sur "New +" → "Blueprint"
3. Connectez votre repository GitHub
4. Sélectionnez le fichier `backend/render.yaml`
5. Cliquez sur "Apply"

### 3. Configuration automatique

Le fichier `backend/render.yaml` va créer :
- Une base de données PostgreSQL
- Un service web pour le backend
- Un disque persistant de 10GB

### 4. Migration de SQLite vers PostgreSQL

**IMPORTANT** : Votre code gère automatiquement SQLite (développement) et PostgreSQL (production).

#### Option A : Partir avec une base PostgreSQL vide (recommandé pour la production)

Votre backend crée automatiquement toutes les tables et données nécessaires :
- Les tables sont créées au premier démarrage
- Le compte admin est créé : `admin@breastcare.bj` / `admin123`
- Les centres de santé du Bénin sont chargés
- **Aucune migration nécessaire** pour démarrer

#### Option B : Migrer vos données SQLite existantes

Si vous avez des données importantes dans SQLite à conserver :

1. **Uploader votre fichier SQLite** :
   ```bash
   # Utiliser Git LFS pour les gros fichiers
   git lfs track "*.db"
   git add backend/breastcare.db
   git commit -m "Add SQLite database for migration"
   git push
   ```

2. **Déployer sur Render** : Le fichier sera disponible

3. **Exécuter la migration** :
   ```bash
   # Se connecter via SSH
   render ssh breastcare-backend
   
   # Exécuter le script
   cd /app
   python migrate_sqlite_to_postgres.py
   ```

⚠️ **Note** : Les fichiers `.db` sont normalement ignorés par Git. Utilisez Git LFS si nécessaire.

#### Ce qui est géré automatiquement

✅ **Compatibilité SQLite/PostgreSQL** :
- Les Enum (BI_RADS_Category, AnalysisStatus) fonctionnent sur les deux
- Les types de colonnes sont compatibles  
- Les Foreign Keys sont gérés
- Le pooling de connexions est configuré différemment

✅ **Démarrage automatique** :
- Les tables sont créées au premier démarrage
- Le compte admin est créé s'il n'existe pas
- Les centres de santé sont chargés si la table est vide
- **Migration SQLite** : Ignorée automatiquement pour PostgreSQL

### 5. Déployer le frontend

**Option A : Sur Vercel (RECOMMANDÉ)**
1. Allez sur [vercel.com](https://vercel.com)
2. Importez votre repository
3. Configurez le root directory : `frontend`
4. Ajoutez la variable d'environnement :
   - `NEXT_PUBLIC_API_URL` = `https://breastcare-backend.onrender.com`

**Option B : Sur Render**
1. Dans Render, créez un nouveau "Static Site"
2. Root directory : `frontend`
3. Build command : `npm install && npm run build`
4. Publish directory : `.next`
5. Ajoutez la variable d'environnement comme ci-dessus

## Configuration des variables d'environnement

Dans Render Dashboard → breastcare-backend → Environment :

| Variable | Valeur | Description |
|----------|--------|-------------|
| DATABASE_URL | Auto | Injecté automatiquement par Render |
| SECRET_KEY | Auto | Généré automatiquement |
| ENVIRONMENT | production | Environnement de production |
| **BACKEND_CORS_ORIGINS** | `https://votre-frontend.vercel.app` | ⚠️ **À définir manuellement après déploiement** - URL de votre frontend (séparées par virgules si plusieurs) |

## Limitations importantes

⚠️ **ATTENTION** : Votre modèle ML (best_medsiglip_model.pth) ne fonctionne pas correctement :
- Le modèle retourne toujours BI-RADS 1 pour toutes les images
- Cela est dû à un biais dans l'entraînement
- **Recommandation** : Réentraîner le modèle avant le déploiement en production

## Coûts estimés

Plan gratuit Render :
- ✅ Backend : 750 heures/mois (gratuit)
- ✅ PostgreSQL : 90 jours (puis $7/mois)
- ✅ Disque persistant : Gratuit pour 10GB
- ❌ Endormissement : Service endormi après 15 min d'inactivité

Plan payant ($7/mois par service) :
- ✅ Pas d'endormissement
- ✅ Performance garantie
- ✅ Support prioritaire

## Support

Si vous avez des problèmes :
1. Vérifiez les logs dans Render Dashboard
2. Vérifiez que DATABASE_URL est bien injecté
3. Vérifiez que le disque persistant est monté

## Notes

- Le fichier `backend/render.yaml` doit être dans le dossier backend/
- Le frontend sera déployé séparément sur Vercel
- Le modèle SQLite restera utilisé en local pour le développement

