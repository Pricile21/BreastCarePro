#!/usr/bin/env python3
"""
Script pour remplacer les 3 images des étapes sur la page mobile
"""

from PIL import Image
from pathlib import Path
import os

# Chemins source
SOURCE_DIR = Path(r"C:\Users\DELL PRECISION 5510\Desktop\Breast_Cancer")
SOURCE_FILES = {
    "première_image.png": "african-woman-mobile-health-app.jpg",  # Étape 1
    "Deuxieme_image.png": "modern-medical-clinic-building-healthcare-center-a.jpg",  # Étape 2
    "Troisieme_image.png": "african-doctor-woman-consultation.jpg",  # Étape 3
}

# Dossier de destination
PUBLIC_DIR = Path(__file__).parent.parent / "frontend" / "public"

print("=" * 60)
print("🖼️  Remplacement des images des 3 étapes")
print("=" * 60)
print()

PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

success_count = 0

for source_name, dest_name in SOURCE_FILES.items():
    source_path = SOURCE_DIR / source_name
    dest_path = PUBLIC_DIR / dest_name
    
    if not source_path.exists():
        print(f"❌ Fichier source introuvable: {source_path}")
        continue
    
    try:
        print(f"📥 Traitement: {source_name}")
        print(f"   → {dest_name}")
        
        # Ouvrir l'image PNG
        img = Image.open(source_path)
        
        # Convertir en RGB si nécessaire (pour les PNG avec transparence)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Créer un fond blanc pour les images avec transparence
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Sauvegarder en JPG avec haute qualité
        img.save(dest_path, 'JPEG', quality=95, optimize=True)
        
        print(f"✅ Image sauvegardée: {dest_path}")
        print(f"   Taille: {img.size[0]}x{img.size[1]} pixels")
        print()
        
        success_count += 1
        
    except Exception as e:
        print(f"❌ Erreur lors du traitement de {source_name}: {e}")
        print()

print("=" * 60)
print(f"✅ {success_count}/{len(SOURCE_FILES)} images remplacées avec succès")
print("=" * 60)
print()
print("💡 Pour voir les changements:")
print("   1. Actualisez la page http://localhost:3000/mobile")
print("   2. Les filtres CSS s'appliqueront automatiquement")

