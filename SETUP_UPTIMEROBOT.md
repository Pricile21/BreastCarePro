# Guide de configuration UptimeRobot pour garder Render actif

## Étape 1 : Créer un compte

1. Allez sur [https://uptimerobot.com](https://uptimerobot.com)
2. Cliquez sur **"Sign Up"** (gratuit)
3. Créez votre compte avec votre email

## Étape 2 : Ajouter le monitor pour le Backend

1. Une fois connecté, cliquez sur **"+ Add New Monitor"**
2. Configurez :
   - **Monitor Type** : `HTTP(s)`
   - **Friendly Name** : `BreastCare Backend`
   - **URL** : `https://breastcare-backend.onrender.com/health`
   - **Monitoring Interval** : `5 minutes` (plan gratuit)
   - **Timeout** : `60 seconds` (important pour gérer le cold start Render)
   - **Alert Contacts** : Sélectionnez votre email (vous recevrez des alertes si le serveur est down)
   - **HTTP Method** : `GET` (ou laissez par défaut)
3. Cliquez sur **"Create Monitor"**

### ⚠️ Si vous obtenez une erreur 405 Method Not Allowed

**Solution alternative** : Utilisez l'endpoint racine `/` au lieu de `/health` :
   - **URL** : `https://breastcare-backend.onrender.com/`
   - **Timeout** : `60 seconds`
   
Cet endpoint fonctionne toujours et est plus simple.

## Étape 3 : Ajouter le monitor pour le Frontend

1. Cliquez à nouveau sur **"+ Add New Monitor"**
2. Configurez :
   - **Monitor Type** : `HTTP(s)`
   - **Friendly Name** : `BreastCare Frontend`
   - **URL** : `https://breastcare-frontend.onrender.com`
   - **Monitoring Interval** : `5 minutes` (plan gratuit)
   - **Timeout** : `30 seconds`
   - **Alert Contacts** : Sélectionnez votre email
3. Cliquez sur **"Create Monitor"**

## Étape 4 : Vérifier que ça fonctionne

1. Attendez 5-10 minutes
2. Vérifiez le statut des monitors dans le dashboard UptimeRobot
3. Les monitors devraient être **"UP"** (vert)
4. Votre serveur Render devrait rester actif maintenant !

## Résultat attendu

- ✅ Les serveurs Render ne s'endorment plus
- ✅ Accès instantané pour vos utilisateurs
- ✅ Alertes par email si un serveur est down
- ✅ Statistiques de disponibilité (uptime)

## Notes importantes

- **Plan gratuit** : Permet jusqu'à 50 monitors et ping toutes les 5 minutes (suffisant pour éviter le sleep sur Render)
- **Alertes** : Vous recevrez un email si un serveur est down (utile pour le monitoring)
- **Statistiques** : UptimeRobot garde des statistiques d'uptime (disponibilité)

## Dépannage

### Erreur 405 Method Not Allowed
**Cause** : Le serveur Render est peut-être en train de démarrer (cold start) ou l'endpoint ne supporte pas la méthode HTTP utilisée.

**Solutions** :
1. **Augmentez le timeout** à 60-90 secondes dans UptimeRobot
2. **Utilisez l'endpoint racine `/`** au lieu de `/health` :
   - URL : `https://breastcare-backend.onrender.com/`
3. **Vérifiez que le serveur Render est démarré** (attendez 2-3 minutes après un déploiement)
4. **Après le correctif déployé** : L'endpoint `/health` devrait maintenant accepter GET, HEAD et OPTIONS

### Le monitor montre "Down" (rouge)
- Vérifiez que l'URL est correcte
- Vérifiez que le serveur Render est démarré (peut prendre 30-50 secondes la première fois après un sleep)
- Vérifiez les logs Render pour voir s'il y a des erreurs
- Augmentez le timeout à 60-90 secondes pour gérer le cold start

### Le serveur s'endort quand même
- Vérifiez que le monitor est bien actif (statut "UP")
- Augmentez la fréquence (nécessite un plan payant, mais 5 minutes devrait suffire)
- Vérifiez que l'URL du health check est correcte : `/health` ou `/` pour le backend
- Vérifiez que le timeout est suffisant (60 secondes minimum)

## URLs de vos services

- **Backend Health Check** : `https://breastcare-backend.onrender.com/health`
- **Frontend** : `https://breastcare-frontend.onrender.com`

