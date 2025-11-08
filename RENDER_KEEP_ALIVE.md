# Solutions pour garder Render actif (plan gratuit)

## Problème
Sur Render (plan gratuit), les services s'endorment après 15 minutes d'inactivité, causant :
- ⏱️ Délai de 30-50 secondes pour le réveil (cold start)
- 😞 Mauvaise expérience utilisateur
- ❌ Erreurs de connexion fréquentes

## Solutions

### ✅ Solution 1 : Service de monitoring gratuit (RECOMMANDÉ)

#### Option A : UptimeRobot (Gratuit)
1. Créez un compte sur [UptimeRobot.com](https://uptimerobot.com)
2. Ajoutez un nouveau monitor :
   - **Type** : HTTP(s)
   - **URL** : `https://breastcare-backend.onrender.com/health`
   - **Intervalle** : 5 minutes (gratuit)
   - **Timeout** : 30 secondes
3. Le service pingera votre backend toutes les 5 minutes → le serveur restera actif

**Avantages** :
- ✅ Gratuit
- ✅ Fiable
- ✅ Monitoring en bonus (vous saurez si le serveur est down)
- ✅ Alertes par email/SMS si le serveur est down

#### Option B : Better Uptime (Gratuit)
1. Créez un compte sur [betteruptime.com](https://betteruptime.com)
2. Ajoutez un monitor similaire
3. Ping toutes les 30 secondes (plan gratuit)

#### Option C : StatusCake (Gratuit)
1. Créez un compte sur [statuscake.com](https://www.statuscake.com)
2. Ajoutez un uptime test
3. Ping toutes les 5 minutes

### ✅ Solution 2 : Cron job externe (Gratuit)

Utilisez un service de cron job gratuit pour faire des requêtes HTTP régulières :

#### Option A : Cron-job.org
1. Allez sur [cron-job.org](https://cron-job.org)
2. Créez un compte gratuit
3. Ajoutez un nouveau cron job :
   - **URL** : `https://breastcare-backend.onrender.com/health`
   - **Intervalle** : Toutes les 10 minutes
   - **Méthode** : GET

#### Option B : EasyCron
1. Allez sur [easycron.com](https://www.easycron.com)
2. Créez un compte gratuit
3. Configurez un cron job similaire

### ✅ Solution 3 : GitHub Actions (Gratuit)

Créez un workflow GitHub Actions qui ping votre serveur toutes les 10 minutes :

```yaml
# .github/workflows/keep-alive.yml
name: Keep Render Alive

on:
  schedule:
    - cron: '*/10 * * * *'  # Toutes les 10 minutes
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Render backend
        run: |
          curl -f https://breastcare-backend.onrender.com/health || exit 1
          curl -f https://breastcare-frontend.onrender.com || exit 1
```

**Avantages** :
- ✅ Totalement gratuit
- ✅ Pas de limite de requêtes
- ✅ Intégré à votre repo GitHub

### ✅ Solution 4 : Upgrader vers un plan payant Render

#### Plan Starter ($7/mois par service)
- ⚡ Pas de sleep (serveur toujours actif)
- 🚀 Démarrage instantané
- 💾 512 MB RAM
- 🔄 SSL gratuit

**Coût** :
- Backend : $7/mois
- Frontend : $7/mois
- **Total** : ~$14/mois (~8,500 FCFA/mois)

### ✅ Solution 5 : Migrer vers une autre plateforme

#### Option A : Railway (Recommandé)
- 💰 Plan gratuit généreux ($5 de crédit/mois)
- ⚡ Pas de sleep (tant que vous avez des crédits)
- 🚀 Déploiement simple (similaire à Render)
- 📊 Monitoring intégré

**Migration** :
1. Créez un compte sur [railway.app](https://railway.app)
2. Connectez votre repo GitHub
3. Déployez backend et frontend
4. Configurez les variables d'environnement

#### Option B : Fly.io
- 💰 Plan gratuit généreux
- ⚡ Pas de sleep
- 🌍 Déploiement global (CDN)

#### Option C : Vercel (Frontend) + Railway (Backend)
- ✅ Vercel : Excellent pour Next.js (frontend gratuit, pas de sleep)
- ✅ Railway : Backend (plan gratuit avec crédits)
- 🎯 Solution hybride optimale

## Recommandation

### Pour commencer (Gratuit) :
1. **UptimeRobot** pour garder les serveurs actifs
2. **GitHub Actions** en backup (si vous utilisez GitHub)

### Pour la production (Payant) :
1. **Option 1** : Upgrader Render ($14/mois total)
2. **Option 2** : Migrer vers Railway (gratuit avec crédits, puis payant selon usage)

## Configuration UptimeRobot (Détails)

### Backend
- **Type** : HTTP(s)
- **URL** : `https://breastcare-backend.onrender.com/health`
- **Nom** : BreastCare Backend
- **Intervalle** : 5 minutes
- **Timeout** : 30 secondes

### Frontend
- **Type** : HTTP(s)
- **URL** : `https://breastcare-frontend.onrender.com`
- **Nom** : BreastCare Frontend
- **Intervalle** : 5 minutes
- **Timeout** : 30 secondes

## Notes importantes

1. **Respecter les limites** : Les services de ping gratuits ont des limites (généralement toutes les 5 minutes minimum)
2. **Health check endpoint** : Votre backend a un endpoint `/health` qui répond rapidement
3. **Monitoring** : UptimeRobot vous enverra des alertes si le serveur est down
4. **Coût** : Les solutions de ping sont gratuites et ne coûtent rien

## URLs de vos services Render

- **Backend** : `https://breastcare-backend.onrender.com`
- **Frontend** : `https://breastcare-frontend.onrender.com`
- **Health Check** : `https://breastcare-backend.onrender.com/health`

