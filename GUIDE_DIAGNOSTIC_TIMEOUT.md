# Guide de Diagnostic - Erreur Timeout Backend

## 🔍 Problème Identifié

Vous avez une erreur `AbortError` (timeout) lors de la connexion :
- Le frontend envoie bien la requête vers `http://localhost:8000/api/v1/auth/login`
- Le backend ne répond pas dans les 30 secondes (maintenant 60 secondes)
- La requête est interrompue avant d'obtenir une réponse

## ✅ Solutions Implémentées

1. **Timeout augmenté** : De 30s à 60s pour permettre l'initialisation complète du backend
2. **Message d'erreur amélioré** : Indique les vérifications à faire
3. **Script de diagnostic** : `test_backend_connection.py` pour tester la connexion

## 🔧 Étapes de Diagnostic

### 1. Vérifier que le Backend est Démarré

**Dans le terminal backend :**
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
✅ X centres déjà dans la base
INFO:     Application startup complete.
```

### 2. Tester l'Endpoint /health

**Dans votre navigateur :**
```
http://localhost:8000/health
```

**Ou avec le script Python :**
```bash
python test_backend_connection.py
```

**Réponse attendue :**
```json
{"status": "healthy", "service": "breastcare-api"}
```

### 3. Vérifier les Logs du Backend

Quand vous tentez de vous connecter, vous devriez voir dans les logs du backend :

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

### 4. Vérifier les Problèmes Courants

#### A. Backend en train de Charger des Modèles ML

**Symptôme :** Première requête très lente (>30s)

**Solution :** Attendre que le backend finisse de charger les modèles
```
INFO:     Loading ML models...
INFO:     Models loaded successfully
```

#### B. Problème de Base de Données

**Symptôme :** Erreurs dans les logs concernant SQLite

**Solution :**
```bash
cd backend
# Vérifier que breastcare.db existe
ls -la breastcare.db

# Si problème, réinitialiser
python app/db/init_db.py
```

#### C. Port 8000 Déjà Utilisé

**Symptôme :** Erreur "Address already in use"

**Solution :**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Ou changer le port dans backend/app/core/config.py
```

#### D. Problème CORS

**Symptôme :** Erreur CORS dans la console navigateur

**Vérifier :** `backend/app/core/config.py`
```python
BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",  # Doit être présent
    "http://127.0.0.1:3000",
]
```

### 5. Test Manuel de l'Endpoint Login

**Avec PowerShell :**
```powershell
$body = @{
    email = "admin@breastcare.bj"
    password = "admin123"
    source = "mobile"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/v1/auth/login" `
    -Method POST `
    -Body $body `
    -ContentType "application/json" `
    -TimeoutSec 60
```

**Avec Python :**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "email": "admin@breastcare.bj",
        "password": "admin123",
        "source": "mobile"
    },
    timeout=60
)
print(response.status_code)
print(response.json())
```

### 6. Vérifier la Configuration Frontend

**Fichier :** `frontend/lib/api.ts`

**URL doit être :**
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
```

**Vérifier dans `.env.local` (frontend) :**
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 🚨 Problèmes Spécifiques

### Problème 1 : Backend Démarre mais Ne Répond Pas

**Causes possibles :**
- Initialisation DB très lente
- Chargement modèles ML bloqué
- Erreur silencieuse dans le code

**Solution :**
1. Vérifier les logs du backend
2. Ajouter des print() dans `backend/app/main.py` au démarrage
3. Tester avec un endpoint simple (`/health`)

### Problème 2 : Erreur 400 au lieu de Timeout

**Si vous obtenez une erreur 400 :**
- Le backend reçoit la requête mais la requête est mal formatée
- Vérifier le Content-Type : `application/json`
- Vérifier le format JSON envoyé

### Problème 3 : Backend Bloqué sur une Opération

**Le backend peut être bloqué sur :**
- Chargement modèles ML (première fois)
- Migration base de données
- Seed centres béninois

**Solution :** Attendre ou regarder les logs

## 📝 Checklist Rapide

- [ ] Backend démarré avec `uvicorn app.main:app --reload`
- [ ] Test `/health` fonctionne
- [ ] Pas d'erreurs dans les logs backend
- [ ] Port 8000 libre
- [ ] CORS configuré correctement
- [ ] URL API correcte dans frontend
- [ ] Timeout augmenté à 60s (déjà fait)

## 🎯 Test Rapide

1. **Démarrer le backend :**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. **Attendre le message :**
   ```
   INFO:     Application startup complete.
   ```

3. **Tester dans le navigateur :**
   ```
   http://localhost:8000/health
   ```

4. **Si OK, tester le login depuis le frontend**

## 💡 Note Importante

Si vous essayez de vous connecter avec un compte **admin** sur la plateforme **mobile**, vous obtiendrez une erreur **403 Forbidden** (comportement attendu). C'est normal ! Les admins doivent se connecter via `/admin/login`.

Pour tester la connexion mobile, utilisez un compte patient ou professionnel.

## 🔗 Fichiers Modifiés

- ✅ `frontend/lib/api.ts` : Timeout augmenté à 60s
- ✅ `test_backend_connection.py` : Script de diagnostic créé
- ✅ `GUIDE_DIAGNOSTIC_TIMEOUT.md` : Ce guide

