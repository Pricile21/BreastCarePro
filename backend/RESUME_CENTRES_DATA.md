# Résumé des Données de Centres de Santé

## ✅ Coordonnées disponibles

**OUI, la base de données a des coordonnées GPS** pour tous les 15 centres :

### Exemples de coordonnées :

1. **CNHU Hubert Koutoukou Maga** (Cotonou)
   - Latitude: 6.3557
   - Longitude: 2.4124

2. **CHU-MEL Lagune** (Cotonou)
   - Latitude: 6.3722
   - Longitude: 2.4211

3. **Hôpital Évangélique de Bembéréké**
   - Latitude: 10.2281
   - Longitude: 2.6625

4. **Parakou**
   - Latitude: 9.3372
   - Longitude: 2.6303

## 📊 Total des centres

- **15 centres** au total
- **Tous ont latitude et longitude**
- Répartis sur 7 départements du Bénin

## ⚠️ Problème actuel : "Failed to fetch"

Le message d'erreur "Failed to fetch" sur le frontend indique que **le backend n'est pas démarré** ou qu'il n'est pas accessible.

### Pour résoudre :

1. **Démarrer le backend** :
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

2. **Vérifier que le backend est accessible** :
```bash
# Ouvrir navigateur : http://localhost:8000/docs
# Ou test API : http://localhost:8000/api/v1/healthcare-centers/
```

3. **Relancer le frontend** :
```bash
cd frontend
npm run dev
```

## 🗄️ Base de données

Les données sont dans `backend/app/db/seed_centers.py` et doivent être chargées dans la base PostgreSQL.

### Charger les données :
```bash
cd backend
python app/db/seed_centers.py
```

## 📍 Informations disponibles par centre

Chaque centre a :
- ✅ Latitude/Longitude (GPS)
- ✅ Nom
- ✅ Type (hospital, clinic, center)
- ✅ Adresse
- ✅ Ville
- ✅ Département
- ✅ Services
- ✅ Spécialités
- ✅ Horaires
- ⚠️ Téléphone (None - à vérifier)
- ⚠️ Email (None - à vérifier)

## 🎯 Carte Leaflet

Une fois le backend démarré, la carte affichera automatiquement tous les centres avec leurs coordonnées GPS.

