# Solution pour l'erreur 405 sur UptimeRobot

## Problème
UptimeRobot reçoit une erreur **405 Method Not Allowed** sur l'endpoint `/health`.

## Causes possibles

1. **Cold start Render** : Le serveur est en train de démarrer (30-50 secondes)
2. **Méthode HTTP non supportée** : UptimeRobot utilise peut-être HEAD ou OPTIONS
3. **Reverse proxy Render** : Pendant le démarrage, Render peut retourner des erreurs

## Solutions appliquées

### ✅ Solution 1 : Améliorer l'endpoint `/health`

J'ai modifié l'endpoint pour accepter :
- **GET** (méthode standard)
- **HEAD** (utilisée par certains services de monitoring)
- **OPTIONS** (pour CORS preflight)

### ✅ Solution 2 : Utiliser l'endpoint racine `/` en alternative

L'endpoint `/` est également disponible et fonctionne toujours :
- **URL** : `https://breastcare-backend.onrender.com/`
- **Méthode** : GET
- **Réponse** : Informations sur l'API

## Configuration UptimeRobot

### Option A : Utiliser `/health` (recommandé après le fix)

1. Dans UptimeRobot, modifiez votre monitor :
   - **URL** : `https://breastcare-backend.onrender.com/health`
   - **Méthode** : `GET` (ou laissez par défaut)
   - **Timeout** : `60 secondes` (pour laisser le temps au cold start)
   - **Intervalle** : `5 minutes`

### Option B : Utiliser `/` (solution alternative)

Si `/health` continue à poser problème, utilisez l'endpoint racine :

1. Dans UptimeRobot, modifiez votre monitor :
   - **URL** : `https://breastcare-backend.onrender.com/`
   - **Méthode** : `GET`
   - **Timeout** : `60 secondes`
   - **Intervalle** : `5 minutes`

## Vérification

### Test manuel de l'endpoint

Testez l'endpoint dans votre navigateur ou avec curl :

```bash
# Test GET
curl https://breastcare-backend.onrender.com/health

# Test HEAD
curl -I https://breastcare-backend.onrender.com/health

# Test de l'endpoint racine
curl https://breastcare-backend.onrender.com/
```

### Réponse attendue

**Pour `/health` :**
```json
{
  "status": "healthy",
  "service": "breastcare-api",
  "version": "1.0.0"
}
```

**Pour `/` :**
```json
{
  "message": "BreastCare Pro API",
  "version": "1.0.0",
  "status": "active",
  "description": "AI-powered breast cancer screening platform for Africa"
}
```

## Déploiement du correctif

1. **Commiter les changements** :
   ```bash
   git add backend/app/main.py
   git commit -m "Fix: Improve /health endpoint to support HEAD and OPTIONS methods"
   git push
   ```

2. **Attendre le déploiement Render** (2-5 minutes)

3. **Tester l'endpoint** après le déploiement

4. **Mettre à jour UptimeRobot** si nécessaire

## Notes importantes

- **Cold start** : Le premier ping après 15 minutes d'inactivité peut prendre 30-50 secondes
- **Timeout** : Configurez un timeout de 60 secondes dans UptimeRobot pour gérer le cold start
- **Intervalle** : 5 minutes est suffisant pour éviter le sleep sur Render

## Si le problème persiste

1. **Vérifier les logs Render** pour voir ce qui se passe
2. **Utiliser l'endpoint `/`** en alternative
3. **Augmenter le timeout** dans UptimeRobot à 90 secondes
4. **Vérifier que le serveur Render est bien démarré** (pas en erreur)

