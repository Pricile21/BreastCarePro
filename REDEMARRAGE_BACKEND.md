# 🔄 Redémarrage du Backend - Solution au Problème de Connexion

## 🔴 Problème Identifié

L'erreur `ERR_CONNECTION_REFUSED` est causée par le middleware `TrustedHostMiddleware` qui bloque les requêtes.

## ✅ Solution Appliquée

Le middleware `TrustedHostMiddleware` a été **désactivé temporairement** dans `backend/app/main.py`.

## 🚀 Actions Requises

### Étape 1 : Arrêter le Backend Actuel

**Dans le terminal où le backend tourne :**
- Appuyez sur `Ctrl + C` pour arrêter le serveur

**OU si le processus tourne en arrière-plan :**

**Windows PowerShell :**
```powershell
# Trouver le processus
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess

# Tuer le processus (remplacez <PID> par l'ID trouvé)
Stop-Process -Id <PID> -Force
```

### Étape 2 : Redémarrer le Backend

**Commande à exécuter :**
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

### Étape 3 : Vérifier que ça Fonctionne

**Dans votre navigateur, testez :**
```
http://localhost:8000/health
```

**Réponse attendue :**
```json
{"status": "healthy", "service": "breastcare-api"}
```

### Étape 4 : Tester la Connexion depuis le Frontend

Une fois le backend redémarré, tentez de vous connecter depuis `/mobile/login`.

## 🎯 Ce qui a Changé

**Avant :**
```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"],
)
```

**Après :**
```python
# DÉSACTIVÉ TEMPORAIREMENT - Peut bloquer les requêtes en développement
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"],
# )
```

## ⚠️ Note de Sécurité

Le `TrustedHostMiddleware` est important pour la sécurité en production. Il a été désactivé uniquement pour le développement. 

**Pour la production**, réactivez-le avec la configuration appropriée :
```python
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["votre-domaine.com", "www.votre-domaine.com"],
)
```

## 🔍 Si le Problème Persiste

1. **Vérifiez les logs du backend** pour voir s'il y a des erreurs au démarrage
2. **Vérifiez que le port 8000 est libre :**
   ```powershell
   Get-NetTCPConnection -LocalPort 8000
   ```
3. **Testez avec curl ou Postman** pour isoler le problème
4. **Vérifiez le firewall Windows** qui pourrait bloquer les connexions

## 📝 Checklist

- [ ] Backend arrêté (Ctrl+C ou processus tué)
- [ ] Backend redémarré avec la nouvelle configuration
- [ ] Message "Application startup complete" visible
- [ ] Test `/health` fonctionne dans le navigateur
- [ ] Connexion depuis le frontend fonctionne

