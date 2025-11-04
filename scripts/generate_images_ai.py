#!/usr/bin/env python3
"""
Script pour générer des images réalistes avec Stable Diffusion
via Replicate API ou Stability AI.

Nécessite:
- pip install replicate (pour Replicate)
- ou pip install stability-sdk (pour Stability AI)
"""

import os
import requests
from pathlib import Path
from typing import Optional
import time

# Configuration
PUBLIC_DIR = Path(__file__).parent.parent / "frontend" / "public"

# Prompts optimisés pour générer des images réalistes de femmes africaines
IMAGE_PROMPTS = {
    "african-woman-hero-empowered-confident.jpg": {
        "prompt": (
            "Professional portrait of a confident, empowered African woman, "
            "healthcare professional, medical setting, warm lighting, "
            "authentic representation, high quality photography, "
            "natural skin tones, professional attire, warm smile"
        ),
        "negative_prompt": "cartoon, illustration, unrealistic, whitewashed, overexposed"
    },
    "african-woman-mobile-health-app.jpg": {
        "prompt": (
            "African woman using smartphone with health app, "
            "modern home setting, natural lighting, authentic representation, "
            "focused expression, technology and healthcare, "
            "realistic photography, diverse representation"
        ),
        "negative_prompt": "cartoon, illustration, unrealistic, whitewashed, overexposed"
    },
    "modern-medical-clinic-building-healthcare-center-a.jpg": {
        "prompt": (
            "Modern hospital building in Africa, healthcare center, "
            "medical facility architecture, contemporary design, "
            "professional architecture photography, clean modern exterior, "
            "healthcare infrastructure, realistic photography, "
            "tropical/subtropical setting, blue sky"
        ),
        "negative_prompt": "cartoon, illustration, unrealistic, old building, dilapidated"
    },
    "african-doctor-woman-consultation.jpg": {
        "prompt": (
            "Professional African female doctor in consultation with patient, "
            "medical office setting, authentic healthcare environment, "
            "natural lighting, realistic photography, "
            "diverse representation, professional medical setting"
        ),
        "negative_prompt": "cartoon, illustration, unrealistic, whitewashed, overexposed"
    },
    "african-women-community-support-group.jpg": {
        "prompt": (
            "Group of African women in community support meeting, "
            "healthcare education, diverse group, natural lighting, "
            "authentic representation, realistic photography, "
            "community health setting, warm atmosphere"
        ),
        "negative_prompt": "cartoon, illustration, unrealistic, whitewashed, overexposed"
    },
    "african-woman-confident-empowered-healthcare-welln.jpg": {
        "prompt": (
            "Empowered confident African woman, healthcare wellness theme, "
            "professional portrait, natural lighting, authentic representation, "
            "realistic photography, diverse representation, "
            "inspirational healthcare setting"
        ),
        "negative_prompt": "cartoon, illustration, unrealistic, whitewashed, overexposed"
    }
}


def generate_with_replicate(filename: str, prompt: str, negative_prompt: str) -> Optional[bool]:
    """Génère une image avec Replicate API (Stable Diffusion)"""
    try:
        import replicate
    except ImportError:
        print("❌ Le module 'replicate' n'est pas installé.")
        print("   Installez-le avec: pip install replicate")
        return False
    
    replicate_token = os.getenv("REPLICATE_API_TOKEN")
    if not replicate_token:
        print("❌ REPLICATE_API_TOKEN non défini")
        print("   1. Créez un compte sur https://replicate.com/")
        print("   2. Obtenez votre API token")
        print("   3. Définissez: export REPLICATE_API_TOKEN=votre_token")
        return False
    
    try:
        print(f"🎨 Génération avec Replicate pour: {filename}")
        print(f"   Prompt: {prompt[:100]}...")
        
        # Utiliser Stable Diffusion XL pour de meilleures images
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_outputs": 1,
                "guidance_scale": 7.5,
                "num_inference_steps": 50,
                "scheduler": "K_EULER",
                "output_format": "png"
            }
        )
        
        if isinstance(output, list) and len(output) > 0:
            image_url = output[0]
            
            # Télécharger l'image générée
            print("📥 Téléchargement de l'image générée...")
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            output_path = PUBLIC_DIR / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convertir PNG en JPG si nécessaire
            if filename.endswith('.jpg'):
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(response.content))
                rgb_img = img.convert('RGB')
                rgb_img.save(output_path, 'JPEG', quality=95)
            else:
                with open(output_path, "wb") as f:
                    f.write(response.content)
            
            print(f"✅ Image sauvegardée: {output_path}\n")
            return True
        else:
            print(f"❌ Aucune image générée\n")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}\n")
        return False


def generate_with_stability_ai(filename: str, prompt: str, negative_prompt: str) -> Optional[bool]:
    """Génère une image avec Stability AI API"""
    stability_api_key = os.getenv("STABILITY_API_KEY")
    if not stability_api_key:
        print("❌ STABILITY_API_KEY non défini")
        print("   1. Créez un compte sur https://platform.stability.ai/")
        print("   2. Obtenez votre API key")
        print("   3. Définissez: export STABILITY_API_KEY=votre_key")
        return False
    
    try:
        print(f"🎨 Génération avec Stability AI pour: {filename}")
        
        # API endpoint pour SDXL
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {stability_api_key}"
        }
        
        body = {
            "text_prompts": [
                {"text": prompt, "weight": 1},
                {"text": negative_prompt, "weight": -1}
            ],
            "cfg_scale": 7,
            "steps": 50,
            "samples": 1,
            "style_preset": "photographic"
        }
        
        response = requests.post(url, headers=headers, json=body, timeout=120)
        response.raise_for_status()
        
        data = response.json()
        
        if "artifacts" in data and len(data["artifacts"]) > 0:
            import base64
            image_data = base64.b64decode(data["artifacts"][0]["base64"])
            
            output_path = PUBLIC_DIR / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convertir en JPG si nécessaire
            if filename.endswith('.jpg'):
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(image_data))
                rgb_img = img.convert('RGB')
                rgb_img.save(output_path, 'JPEG', quality=95)
            else:
                with open(output_path, "wb") as f:
                    f.write(image_data)
            
            print(f"✅ Image sauvegardée: {output_path}\n")
            return True
        else:
            print(f"❌ Aucune image générée\n")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}\n")
        return False


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🤖 Génération d'images avec AI pour BreastCare Pro")
    print("=" * 60)
    print()
    
    if not PUBLIC_DIR.exists():
        print(f"❌ Dossier public introuvable: {PUBLIC_DIR}")
        return
    
    print(f"📁 Dossier de destination: {PUBLIC_DIR}\n")
    
    # Vérifier quelle API est disponible
    replicate_token = os.getenv("REPLICATE_API_TOKEN")
    stability_key = os.getenv("STABILITY_API_KEY")
    
    if not replicate_token and not stability_key:
        print("⚠️  Aucune clé API trouvée")
        print("\nOptions disponibles:")
        print("1. Replicate (recommandé): https://replicate.com/")
        print("   - Gratuit avec crédits limités")
        print("   - pip install replicate")
        print("   - export REPLICATE_API_TOKEN=votre_token")
        print()
        print("2. Stability AI: https://platform.stability.ai/")
        print("   - Nécessite un compte payant")
        print("   - export STABILITY_API_KEY=votre_key")
        return
    
    success_count = 0
    for filename, config in IMAGE_PROMPTS.items():
        filepath = PUBLIC_DIR / filename
        
        if filepath.exists():
            response = input(f"⚠️  {filename} existe déjà. Remplacer? (o/N): ")
            if response.lower() != 'o':
                print(f"⏭️  Ignoré: {filename}\n")
                continue
        
        # Essayer Replicate d'abord, puis Stability AI
        if replicate_token:
            if generate_with_replicate(filename, config["prompt"], config["negative_prompt"]):
                success_count += 1
                time.sleep(2)  # Rate limiting
                continue
        
        if stability_key:
            if generate_with_stability_ai(filename, config["prompt"], config["negative_prompt"]):
                success_count += 1
                time.sleep(2)  # Rate limiting
    
    print(f"\n{'=' * 60}")
    print(f"✅ {success_count}/{len(IMAGE_PROMPTS)} images générées")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

