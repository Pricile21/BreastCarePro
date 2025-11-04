#!/usr/bin/env python3
"""
Script pour télécharger des images réalistes de femmes africaines
pour le site BreastCare Pro.

Options:
1. Utiliser Unsplash API (gratuit, nécessite une clé API)
2. Utiliser des URLs d'images libres de droits directement
"""

import os
import requests
from pathlib import Path
from typing import Optional
import json

# Configuration
PUBLIC_DIR = Path(__file__).parent.parent / "frontend" / "public"
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")

# Mappings des images nécessaires
IMAGE_REQUIREMENTS = {
    "african-woman-hero-empowered-confident.jpg": {
        "query": "confident african woman healthcare professional",
        "description": "Hero image - femme africaine confiante et professionnelle"
    },
    "african-woman-mobile-health-app.jpg": {
        "query": "african woman using smartphone health app",
        "description": "Étape 1 - femme africaine utilisant une app santé"
    },
    "modern-medical-clinic-building-healthcare-center-a.jpg": {
        "query": "modern hospital building africa healthcare center medical facility",
        "description": "Étape 2 - hôpital moderne africain"
    },
    "african-doctor-woman-consultation.jpg": {
        "query": "african female doctor consultation patient",
        "description": "Étape 3 - docteure africaine en consultation"
    },
    "african-women-community-support-group.jpg": {
        "query": "african women group support community healthcare",
        "description": "Section éducation - groupe de femmes africaines"
    },
    "african-woman-confident-empowered-healthcare-welln.jpg": {
        "query": "empowered confident african woman healthcare wellness",
        "description": "CTA - femme africaine confiante et autonome"
    }
}


def download_from_unsplash(filename: str, query: str, description: str) -> Optional[bool]:
    """Télécharge une image depuis Unsplash API"""
    if not UNSPLASH_ACCESS_KEY:
        print(f"⚠️  UNSPLASH_ACCESS_KEY non configurée. Pour obtenir une clé:")
        print("   1. Créez un compte sur https://unsplash.com/developers")
        print("   2. Créez une nouvelle application")
        print("   3. Copiez votre Access Key")
        print("   4. Définissez: export UNSPLASH_ACCESS_KEY=votre_clé")
        return False
    
    try:
        # Rechercher une image
        search_url = "https://api.unsplash.com/search/photos"
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        params = {
            "query": query,
            "per_page": 1,
            "orientation": "landscape",
            "content_filter": "high"
        }
        
        print(f"🔍 Recherche d'image pour: {description}")
        print(f"   Query: {query}")
        
        response = requests.get(search_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not data.get("results"):
            print(f"❌ Aucune image trouvée pour '{query}'")
            return False
        
        # Obtenir l'URL de l'image haute résolution
        image_url = data["results"][0]["urls"]["regular"]
        photographer = data["results"][0]["user"]["name"]
        photographer_url = data["results"][0]["user"]["links"]["html"]
        
        print(f"📥 Téléchargement depuis Unsplash...")
        print(f"   Photographe: {photographer}")
        
        # Télécharger l'image
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()
        
        # Sauvegarder
        output_path = PUBLIC_DIR / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(img_response.content)
        
        print(f"✅ Image sauvegardée: {output_path}")
        print(f"   Attribution: Photo par {photographer} sur Unsplash")
        print(f"   Lien: {photographer_url}\n")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors du téléchargement: {e}")
        return False


def download_from_url(filename: str, url: str, description: str) -> Optional[bool]:
    """Télécharge une image depuis une URL directe"""
    try:
        print(f"📥 Téléchargement: {description}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        output_path = PUBLIC_DIR / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"✅ Image sauvegardée: {output_path}\n")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}\n")
        return False


def generate_with_stable_diffusion(filename: str, prompt: str, description: str) -> Optional[bool]:
    """
    Génère une image avec Stable Diffusion API (ex: Replicate, Stability AI)
    Nécessite une clé API pour Stability AI ou Replicate
    """
    stability_api_key = os.getenv("STABILITY_API_KEY", "")
    replicate_api_token = os.getenv("REPLICATE_API_TOKEN", "")
    
    if not stability_api_key and not replicate_api_token:
        print(f"⚠️  Pour générer des images avec AI:")
        print("   Option 1 - Stability AI: https://platform.stability.ai/")
        print("   Option 2 - Replicate: https://replicate.com/")
        print("   Définissez STABILITY_API_KEY ou REPLICATE_API_TOKEN")
        return False
    
    # Ajouter des prompts pour des images réalistes africaines
    enhanced_prompt = (
        f"{prompt}, "
        "professional photography, high quality, realistic, "
        "natural lighting, authentic representation, "
        "diverse african women, healthcare setting, "
        "warm colors, professional composition"
    )
    
    print(f"🎨 Génération d'image avec AI pour: {description}")
    print(f"   Prompt: {enhanced_prompt}")
    
    # Exemple avec Stability AI (nécessite l'installation de stability-sdk)
    try:
        if stability_api_key:
            # Code pour Stability AI SDK
            print("📝 Utilisation de Stability AI...")
            print("   Installez: pip install stability-sdk")
            print("   Documentation: https://platform.stability.ai/docs")
            # TODO: Implémenter l'appel API
            return False
    except Exception as e:
        print(f"❌ Erreur génération: {e}")
    
    return False


def main():
    """Fonction principale"""
    print("=" * 60)
    print("📸 Téléchargement/Génération d'images pour BreastCare Pro")
    print("=" * 60)
    print()
    
    if not PUBLIC_DIR.exists():
        print(f"❌ Dossier public introuvable: {PUBLIC_DIR}")
        print("   Assurez-vous d'exécuter ce script depuis la racine du projet")
        return
    
    print(f"📁 Dossier de destination: {PUBLIC_DIR}\n")
    
    # Méthode: Unsplash (recommandé)
    print("🌐 Méthode 1: Téléchargement depuis Unsplash API\n")
    
    success_count = 0
    for filename, config in IMAGE_REQUIREMENTS.items():
        filepath = PUBLIC_DIR / filename
        
        # Vérifier si l'image existe déjà
        if filepath.exists():
            response = input(f"⚠️  {filename} existe déjà. Remplacer? (o/N): ")
            if response.lower() != 'o':
                print(f"⏭️  Ignoré: {filename}\n")
                continue
        
        if download_from_unsplash(filename, config["query"], config["description"]):
            success_count += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ {success_count}/{len(IMAGE_REQUIREMENTS)} images téléchargées")
    print("=" * 60)
    
    if success_count == 0:
        print("\n💡 Alternatives:")
        print("   1. Utilisez des images libres de droits depuis:")
        print("      - Unsplash: https://unsplash.com/s/photos/african-woman-healthcare")
        print("      - Pexels: https://www.pexels.com/search/african%20woman%20healthcare/")
        print("      - Pixabay: https://pixabay.com/images/search/african%20woman%20health/")
        print()
        print("   2. Créez une clé API Unsplash gratuite:")
        print("      https://unsplash.com/developers")
        print()
        print("   3. Pour générer des images avec AI:")
        print("      - Stability AI: https://platform.stability.ai/")
        print("      - Replicate: https://replicate.com/")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

