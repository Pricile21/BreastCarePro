# Intégration de Leaflet avec OpenStreetMap

## ✅ Problèmes résolus

1. **Carte ne s'affichait pas** → Maintenant fonctionnelle avec OpenStreetMap
2. **Géolocalisation pas demandée** → Demande explicite à l'utilisateur au chargement
3. **Besoin d'une carte interactive** → Utilisation de Leaflet + OpenStreetMap (open source, gratuit)

## 📦 Packages installés

```bash
npm install leaflet react-leaflet @types/leaflet --legacy-peer-deps
```

## 🔧 Modifications apportées

### 1. Nouveau composant `MapComponent.tsx`
- **Lieu**: `frontend/components/MapComponent.tsx`
- **Fonctionnalités**:
  - Carte OpenStreetMap via Leaflet
  - Marqueurs pour chaque centre de santé
  - Position de l'utilisateur (si autorisé)
  - Popups avec nom et type de chaque centre
  - Zoom automatique pour afficher tous les centres

### 2. Mise à jour de la page Providers
- **Fichier**: `frontend/app/mobile/providers/page.tsx`
- **Changements**:
  - Import dynamique du composant de carte (SSR disabled)
  - Gestion de la géolocalisation avec demande explicite
  - Remplacement du placeholder par une vraie carte
  - Affichage de la position de l'utilisateur sur la carte
  - Description dynamique selon présence de position GPS

### 3. Ajout des styles Leaflet
- **Fichier**: `frontend/app/globals.css`
- Import global des styles Leaflet

## 🎯 Fonctionnalités

### Géolocalisation
- Demande automatique au chargement de la page
- Timeout de 10 secondes
- Cache de 5 minutes
- Haute précision activée
- Gestion gracieuse si l'utilisateur refuse

### Carte
- Tiles OpenStreetMap (gratuit, sans clé API)
- Marqueurs bleus standards pour les centres
- Marqueur bleu circulaire pour la position utilisateur
- Popups avec nom du centre
- Zoom adaptatif selon les marqueurs présents
- Vue par défaut: Cotonou (centre du Bénin)

### Responsive
- Hauteur de carte: 400px
- Largeur: 100%
- Compatible mobile et desktop

## 🔍 Comportement

### Si géolocalisation acceptée:
1. Demande de position au chargement
2. Affichage de la position sur la carte
3. Affichage de tous les centres avec marqueurs
4. Description: "Position détectée - centres à proximité"

### Si géolocalisation refusée:
1. Affichage de la carte centrée sur Cotonou
2. Affichage de tous les centres avec marqueurs
3. Description: "Carte interactive des centres de dépistage"
4. Aucune erreur - fonctionnement normal

## 🐛 Fix technique Leaflet/Next.js

Les icônes Leaflet nécessitent une configuration spéciale pour Next.js:

```typescript
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})
```

Cela fixe le problème où les icônes ne s'affichaient pas correctement.

## 📍 Coordination des données

- Les coordonnées proviennent de la base de données des centres
- Chaque centre a sa latitude/longitude
- Par défaut: Cotonou (6.3667, 2.4167) si coordonnées absentes
- Recherche par proximité activée si position utilisateur disponible

## 🚀 Prochaines améliorations possibles

1. Clustering des marqueurs (regroupement en zoom faible)
2. Filtrage des centres par type sur la carte
3. Calcul et affichage des distances
4. Itinéraires (bouton "Y aller")
5. Personnalisation des icônes par type de centre

