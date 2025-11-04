# Guide pour obtenir des images réalistes africaines

Ce guide explique comment obtenir et générer des images adaptées pour représenter des femmes africaines sur le site BreastCare Pro.

## 🎯 Problème identifié

Les images actuelles peuvent paraître trop blanches/surexposées et ne représentent pas fidèlement les tons de peau africains.

## ✅ Solutions disponibles

### Option 1: Télécharger depuis Unsplash (RECOMMANDÉ - Gratuit)

Unsplash a une excellente collection d'images libres de droits avec des personnes africaines authentiques.

**Étapes:**

1. Créez un compte développeur sur [Unsplash Developers](https://unsplash.com/developers)
2. Créez une nouvelle application (gratuit)
3. Copiez votre Access Key
4. Exécutez le script:

```bash
# Windows PowerShell
$env:UNSPLASH_ACCESS_KEY="votre_clé_ici"
python scripts/download_images.py

# Linux/Mac
export UNSPLASH_ACCESS_KEY="votre_clé_ici"
python scripts/download_images.py
```

Le script téléchargera automatiquement des images adaptées pour chaque section.

### Option 2: Générer avec AI (Stable Diffusion)

Pour générer des images personnalisées avec AI:

#### Avec Replicate (Recommandé - Gratuit avec crédits):

```bash
# Installer
pip install replicate requests pillow

# Configurer
export REPLICATE_API_TOKEN="votre_token_replicate"

# Générer
python scripts/generate_images_ai.py
```

Obtenez votre token sur [Replicate](https://replicate.com/)

#### Avec Stability AI:

```bash
# Installer
pip install requests pillow

# Configurer
export STABILITY_API_KEY="votre_key_stability"

# Générer
python scripts/generate_images_ai.py
```

### Option 3: Téléchargement manuel

Si vous préférez choisir les images vous-même:

1. **Unsplash** - Recherchez:
   - [African woman healthcare](https://unsplash.com/s/photos/african-woman-healthcare)
   - [African doctor](https://unsplash.com/s/photos/african-doctor)
   - [African women community](https://unsplash.com/s/photos/african-women-community)
   - [Modern hospital building Africa](https://unsplash.com/s/photos/modern-hospital-building-africa)

2. **Pexels** - Recherchez:
   - [African woman healthcare](https://www.pexels.com/search/african%20woman%20healthcare/)
   - [African doctor](https://www.pexels.com/search/african%20doctor/)
   - [Modern hospital building](https://www.pexels.com/search/modern%20hospital%20building/)

3. **Pixabay** - Recherchez:
   - [African woman health](https://pixabay.com/images/search/african%20woman%20health/)
   - [Modern hospital](https://pixabay.com/images/search/modern%20hospital/)

Téléchargez les images et placez-les dans `frontend/public/` avec les noms suivants:

- `african-woman-hero-empowered-confident.jpg` - Hero image (femme africaine confiante)
- `african-woman-mobile-health-app.jpg` - Étape 1 (femme avec smartphone)
- `modern-medical-clinic-building-healthcare-center-a.jpg` - **Étape 2 (hôpital moderne africain)** ⭐
- `african-doctor-woman-consultation.jpg` - Étape 3 (docteure en consultation)
- `african-women-community-support-group.jpg` - Section éducation (groupe de femmes)
- `african-woman-confident-empowered-healthcare-welln.jpg` - CTA (femme confiante)

## 🔧 Ajustements CSS déjà appliqués

Les images ont déjà des filtres CSS pour améliorer leur apparence:

- `brightness-90`: Réduit la luminosité de 10%
- `contrast-110`: Augmente le contraste de 10%
- `saturate-110`: Augmente la saturation légèrement

Ces ajustements sont dans `frontend/app/mobile/page.tsx`.

## 📝 Critères pour de bonnes images

- ✅ Représentation authentique des tons de peau africains (pour les images avec personnes)
- ✅ **Hôpital moderne africain** pour l'étape 2 (architecture contemporaine, contexte africain)
- ✅ Éclairage naturel et équilibré
- ✅ Contexte professionnel/healthcare approprié
- ✅ Diversité dans la représentation
- ✅ Haute résolution (minimum 1920x1080)
- ✅ Format horizontal (landscape) pour les hero images

## 🚀 Après avoir ajouté les nouvelles images

1. Vérifiez que les images sont bien dans `frontend/public/`
2. Redémarrez le serveur de développement si nécessaire
3. Actualisez la page `http://localhost:3000/mobile`
4. Les filtres CSS s'appliqueront automatiquement

## 💡 Notes importantes

- Les images téléchargées via Unsplash nécessitent une attribution (incluse dans le script)
- Les images générées via AI sont généralement libres de droits
- Vérifiez toujours les licences des images avant utilisation commerciale
- Les scripts gèrent automatiquement la conversion PNG → JPG si nécessaire

