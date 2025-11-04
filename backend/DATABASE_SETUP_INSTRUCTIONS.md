# Instructions pour résoudre "no such table: healthcare_centers"

## Problème

L'erreur `no such table: healthcare_centers` indique que la base de données n'a pas la table nécessaire.

## Solution

### Option 1: Activer l'environnement virtuel et exécuter le script

```bash
cd backend

# Activer l'environnement virtuel
# Pour Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Pour Windows CMD:
venv\Scripts\activate.bat

# Pour Linux/Mac:
source venv/bin/activate

# Ensuite exécuter le script
python init_db_with_centers.py
```

### Option 2: Exécuter les commandes manuellement

1. **Créer les tables:**
```bash
python -c "from app.db.session import engine; from app.models.base import Base; from app.models.healthcare_center import HealthcareCenter; Base.metadata.create_all(bind=engine); print('✅ Tables créées')"
```

2. **Charger les centres:**
```bash
python app/db/seed_centers.py
```

## Résultat attendu

Vous devriez voir:
```
🏗️  Création des tables...
✅ Compte administrateur créé
📋 Chargement de 15 centres de santé...
✅ Added: Centre National Hospitalier Universitaire...
...
✅ Base de données initialisée avec succès!
📊 15 centres chargés
```

## Vérification

Pour vérifier que les centres sont bien dans la base:
```bash
python -c "from app.db.session import SessionLocal; from app.models.healthcare_center import HealthcareCenter; db = SessionLocal(); centers = db.query(HealthcareCenter).all(); print(f'Total centres: {len(centers)}'); [print(f'{c.name}: {c.latitude}, {c.longitude}') for c in centers[:3]]"
```

## Si le problème persiste

1. Supprimer la base SQLite existante:
```bash
rm breastcare.db  # Linux/Mac
del breastcare.db  # Windows
```

2. Recréer la base avec le script:
```bash
python init_db_with_centers.py
```

3. Redémarrer le serveur backend:
```bash
uvicorn app.main:app --reload --port 8000
```

