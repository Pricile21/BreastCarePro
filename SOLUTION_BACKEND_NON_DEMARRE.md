# 🔴 SOLUTION : Backend Non Démarré

## Problème Identifié

Le test de connexion montre que **le port 8000 n'est PAS ouvert**, ce qui signifie que **le backend n'est PAS démarré**.

C'est pourquoi toutes vos requêtes timeout après 60 secondes - il n'y a simplement personne pour répondre !

## ✅ Solution Immédiate

### Option 1 : Utiliser le Script de Démarrage (Recommandé)

**Windows PowerShell :**
```powershell
.\start_backend.ps1
```

**Windows CMD :**
```cmd
start_backend.bat
```

### Option 2 : Démarrage Manuel

**Dans un terminal, exécutez :**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔍 Vérification que le Backend est Démarré

### 1. Vérifier les Logs du Démarrage

Vous devriez voir dans le terminal :
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
🏗️  Création des tables si nécessaire...
✅ Tables vérifiées
✅ X centres déjà dans la base
INFO:     Application startup complete.
```

### 2. Tester dans le Navigateur

Ouvrez :
```
http://localhost:8000/health
```

**Réponse attendue :**
```json
{"status": "healthy", "service": "breastcare-api"}
```

### 3. Vérifier le Port

**PowerShell :**
```powershell
Test-NetConnection -ComputerName localhost -Port 8000
```

**Devrait montrer :**
```
TcpTestSucceeded : True
```

## 🚨 Problèmes Courants

### Problème 1 : "Python n'est pas reconnu"

**Solution :**
1. Vérifier que Python est installé : `python --version`
2. Ajouter Python au PATH si nécessaire
3. Ou utiliser le chemin complet : `C:\Python39\python.exe -m uvicorn ...`

### Problème 2 : "Module uvicorn not found"

**Solution :**
```bash
cd backend
pip install -r requirements.txt
```

### Problème 3 : "Port 8000 already in use"

**Solution :**
```powershell
# Trouver le processus utilisant le port 8000
Get-NetTCPConnection -LocalPort 8000

# Tuer le processus (remplacer PID par l'ID trouvé)
taskkill /PID <PID> /F

# Ou changer le port dans le code
```

### Problème 4 : "Erreur lors de l'initialisation"

Si vous voyez des erreurs dans les logs de démarrage :

**Vérifier la base de données :**
```bash
cd backend
# Vérifier que breastcare.db existe
ls breastcare.db
```

**Réinitialiser si nécessaire :**
```bash
python app/db/init_db.py
```

## 📝 Checklist

Avant de tenter de vous connecter :

- [ ] Backend démarré (commande `uvicorn` en cours)
- [ ] Message "Application startup complete" visible
- [ ] Test `http://localhost:8000/health` fonctionne
- [ ] Port 8000 accessible (Test-NetConnection retourne True)
- [ ] Pas d'erreurs dans les logs du backend

## 🎯 Test Complet

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

4. **Si OK, tenter la connexion depuis le frontend**

## 💡 Pourquoi ça fonctionnait avant ?

Il y a plusieurs possibilités :
- Le backend était démarré automatiquement (script, service Windows)
- Vous utilisiez Docker Compose qui démarrait automatiquement le backend
- Un autre processus gérait le démarrage du backend

Maintenant, vous devez le démarrer manuellement.

## 🔧 Démarrage Automatique (Optionnel)

Si vous voulez démarrer automatiquement le backend avec le frontend :

**Créer un script `start_all.bat` :**
```batch
@echo off
start cmd /k "cd backend && python -m uvicorn app.main:app --reload"
timeout /t 3
cd frontend
npm run dev
```

Ou utiliser `docker-compose` si vous avez Docker installé.

## 🚀 Une Fois le Backend Démarré

1. Le frontend devrait pouvoir se connecter
2. Les tokens seront automatiquement sauvegardés
3. L'authentification fonctionnera normalement

**Important :** Le backend DOIT rester démarré pendant que vous utilisez le frontend !

