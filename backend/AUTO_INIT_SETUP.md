# Initialisation Automatique de la Base de Données

## ✅ Changement apporté

J'ai ajouté un événement `@app.on_event("startup")` dans `app/main.py` qui s'exécute automatiquement au démarrage du backend.

## 🎯 Ce qui se passe maintenant au démarrage

1. **Vérification des tables** : Toutes les tables sont créées si elles n'existent pas
2. **Vérification des centres** : Si aucun centre n'est dans la base, les 15 centres sont chargés automatiquement
3. **Logs informatifs** : Des messages dans le terminal informent de l'état de la base

## 📋 Messages attendus dans le terminal

Au démarrage du backend, vous devriez voir :
```
🏗️  Création des tables si nécessaire...
✅ Tables vérifiées
📋 Aucun centre trouvé. Chargement de 15 centres...
✅ Added: Centre National Hospitalier Universitaire...
...
✅ 15 centres chargés
```

Ou si les centres existent déjà :
```
🏗️  Création des tables si nécessaire...
✅ Tables vérifiées
✅ 15 centres déjà dans la base
```

## 🔄 Pour appliquer les changements

1. **Arrêter le backend** (Ctrl+C dans le terminal où il tourne)

2. **Redémarrer le backend** :
```bash
uvicorn app.main:app --reload --port 8000
```

3. **Vérifier les logs** : Les messages d'initialisation devraient apparaître

4. **Tester la page** : Rouvrir `http://localhost:3000/mobile/providers`

## ✨ Avantages

- ✅ Plus besoin d'exécuter manuellement des scripts de migration
- ✅ La base est toujours à jour au démarrage
- ✅ Pas de risque d'oublier d'initialiser les données
- ✅ Idempotent : ne recrée pas les données si elles existent déjà

