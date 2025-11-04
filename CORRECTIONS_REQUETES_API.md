# Corrections Apportées - Problème de Requêtes API

## 🔧 Corrections Effectuées

### 1. **Gestion du Body de Requête**
**Problème** : Le body était doublement stringifié (une fois dans `login()`, une fois dans `request()`)

**Solution** : 
- La méthode `request()` détecte maintenant si le body est un objet et le convertit en JSON
- La méthode `login()` passe directement l'objet, pas une string JSON

**Code corrigé :**
```typescript
// Avant (problème)
body: JSON.stringify(loginData) // Stringifiée ici
// Puis dans request(), si c'est une string, elle était envoyée telle quelle

// Après (corrigé)
body: loginData as any // Objet passé
// Dans request(), détection et conversion en JSON si nécessaire
```

### 2. **Amélioration des Logs**
- Ajout de logs plus détaillés pour le debugging
- Log du timeout avec URL précise
- Log des headers de requête

### 3. **Gestion des Erreurs Améliorée**
- Messages d'erreur plus clairs et actionnables
- Distinction entre erreur réseau et timeout
- Instructions précises pour résoudre les problèmes

### 4. **Validation de la Réponse**
- Vérification que la réponse contient bien un token
- Message d'erreur clair si le token est manquant

## 🎯 Actions Immédiates à Effectuer

### Étape 1 : Vérifier que le Backend est Démarré

**Dans un terminal, exécutez :**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Vous devriez voir :**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
🏗️  Création des tables si nécessaire...
✅ Tables vérifiées
INFO:     Application startup complete.
```

### Étape 2 : Tester l'Endpoint Health

**Ouvrez dans votre navigateur :**
```
http://localhost:8000/health
```

**Réponse attendue :**
```json
{"status": "healthy", "service": "breastcare-api"}
```

**Si vous obtenez une erreur :**
- Le backend n'est pas démarré
- Le port 8000 est utilisé par un autre programme
- Il y a une erreur dans le code du backend

### Étape 3 : Vérifier les Logs du Backend

Quand vous tentez de vous connecter depuis le frontend, vous devriez voir dans les logs du backend :

```
================================================================================
🌐 REQUÊTE REÇUE: POST /api/v1/auth/login
📥 Headers: {...}
📦 Body (preview): b'{"email":"admin@breastcare.bj","password":"admin123",...}'
================================================================================

🔐 ========== REQUÊTE LOGIN REÇUE ==========
📥 Email reçu: admin@breastcare.bj
📥 Source reçu: mobile
...
```

**Si vous NE voyez PAS ces logs :**
- Le backend ne reçoit pas la requête
- Problème CORS ou firewall
- Le frontend ne peut pas atteindre le backend

### Étape 4 : Vérifier CORS

**Vérifier dans `backend/app/core/config.py` :**
```python
BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",  # DOIT être présent
    "http://127.0.0.1:3000",
]
```

### Étape 5 : Tester avec un Compte Non-Admin

**Important :** Si vous essayez de vous connecter avec un compte **admin** (`admin@breastcare.bj`) sur la plateforme **mobile**, vous obtiendrez une erreur **403 Forbidden**. C'est normal ! Les admins doivent se connecter via `/admin/login`.

Pour tester la connexion mobile, créez un compte patient ou utilisez un compte professionnel existant.

## 🔍 Diagnostic Détaillé

### Si le Backend Reçoit la Requête mais Ne Répond Pas

**Causes possibles :**
1. **Initialisation lente** : Première requête peut prendre du temps (chargement modèles ML, DB)
2. **Erreur silencieuse** : Le backend crash mais ne log pas l'erreur
3. **Timeout interne** : Une opération dans le backend dépasse le timeout

**Solutions :**
1. Regarder les logs du backend attentivement
2. Vérifier qu'il n'y a pas d'erreurs Python
3. Augmenter le timeout du frontend (déjà fait : 60 secondes)

### Si le Backend Ne Reçoit Pas la Requête

**Causes possibles :**
1. **CORS mal configuré** : Le backend rejette la requête
2. **Firewall/Proxy** : Bloque la connexion
3. **URL incorrecte** : Le frontend pointe vers la mauvaise URL

**Solutions :**
1. Vérifier CORS dans `backend/app/core/config.py`
2. Vérifier l'URL dans `frontend/lib/api.ts` : `http://localhost:8000/api/v1`
3. Tester avec `curl` ou Postman pour isoler le problème

## 📝 Checklist de Résolution

- [ ] Backend démarré et accessible sur http://localhost:8000
- [ ] Endpoint `/health` répond correctement
- [ ] Logs backend montrent la réception de la requête
- [ ] CORS correctement configuré
- [ ] Pas d'erreurs dans les logs backend
- [ ] Utilisation d'un compte non-admin pour tester mobile
- [ ] Timeout augmenté à 60 secondes (déjà fait)

## 🚀 Test Rapide

1. **Démarrer le backend**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. **Attendre le message de démarrage complet**

3. **Tester dans le navigateur :**
   ```
   http://localhost:8000/health
   ```

4. **Si OK, tenter la connexion depuis le frontend**

## 💡 Notes Importantes

- Les tokens sont maintenant correctement sauvegardés dans `localStorage`
- La gestion automatique des tokens dans les headers fonctionne
- Les logs sont améliorés pour faciliter le debugging
- Le timeout est de 60 secondes (au lieu de 30)

## 🔗 Fichiers Modifiés

- ✅ `frontend/lib/api.ts` : Corrections du body, logs, gestion d'erreurs
- ✅ `GUIDE_DIAGNOSTIC_TIMEOUT.md` : Guide de diagnostic
- ✅ `CORRECTIONS_REQUETES_API.md` : Ce document

