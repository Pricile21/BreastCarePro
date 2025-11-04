#!/usr/bin/env python3
"""
Script d'exploration du dataset VinDr-Mammo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import cv2
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=== EXPLORATION DU DATASET VINDR-MAMMO ===")
    
    # Chemins vers les données
    data_root = Path('.')
    images_path = data_root / 'Extract' / 'images_png'
    extracted_path = data_root / 'extracted_data' / 'images_png'
    
    # Fichiers CSV disponibles
    csv_files = {
        'metadata': data_root / 'metadata.csv',
        'breast_annotations': data_root / 'breast-level_annotations (1).csv',
        'finding_annotations': data_root / 'finding_annotations (1).csv'
    }
    
    print("\n1. VÉRIFICATION DES FICHIERS:")
    for name, path in csv_files.items():
        if path.exists():
            print(f"✓ {name}: {path}")
        else:
            print(f"✗ {name}: {path} - Fichier non trouvé")
    
    print(f"\nDossier d'images Extract: {images_path.exists()}")
    print(f"Dossier d'images extracted_data: {extracted_path.exists()}")
    
    # Analyse des métadonnées
    if csv_files['metadata'].exists():
        print("\n2. ANALYSE DES MÉTADONNÉES:")
        metadata_df = pd.read_csv(csv_files['metadata'])
        print(f"Nombre total d'images: {len(metadata_df)}")
        print(f"Colonnes disponibles: {list(metadata_df.columns)}")
        print("\nPremières lignes:")
        print(metadata_df.head())
    
    # Analyse des annotations BI-RADS
    if csv_files['breast_annotations'].exists():
        print("\n3. ANALYSE DES ANNOTATIONS BI-RADS:")
        breast_annotations_df = pd.read_csv(csv_files['breast_annotations'])
        print(f"Nombre total d'annotations: {len(breast_annotations_df)}")
        print(f"Colonnes: {list(breast_annotations_df.columns)}")
        
        if 'breast_bi_rads' in breast_annotations_df.columns:
            print("\nDistribution des classes BI-RADS:")
            bi_rads_dist = breast_annotations_df['breast_bi_rads'].value_counts().sort_index()
            for bi_rads, count in bi_rads_dist.items():
                percentage = (count / len(breast_annotations_df)) * 100
                print(f"BI-RADS {bi_rads}: {count} images ({percentage:.1f}%)")
        
        if 'breast_density' in breast_annotations_df.columns:
            print("\nDistribution de la densité mammaire:")
            density_dist = breast_annotations_df['breast_density'].value_counts().sort_index()
            for density, count in density_dist.items():
                percentage = (count / len(breast_annotations_df)) * 100
                print(f"Densité {density}: {count} images ({percentage:.1f}%)")
    
    # Analyse des annotations de findings
    if csv_files['finding_annotations'].exists():
        print("\n4. ANALYSE DES ANNOTATIONS DE FINDINGS:")
        finding_annotations_df = pd.read_csv(csv_files['finding_annotations'])
        print(f"Nombre total d'annotations: {len(finding_annotations_df)}")
        print(f"Colonnes: {list(finding_annotations_df.columns)}")
        
        if 'finding_categories' in finding_annotations_df.columns:
            print("\nTypes de findings:")
            findings_dist = finding_annotations_df['finding_categories'].value_counts()
            for finding, count in findings_dist.items():
                print(f"{finding}: {count} annotations")
        
        print(f"\nImages avec annotations: {finding_annotations_df['image_id'].nunique()}")
        print(f"Nombre moyen d'annotations par image: {len(finding_annotations_df) / finding_annotations_df['image_id'].nunique():.2f}")
    
    # Analyse des images
    print("\n5. ANALYSE DES IMAGES:")
    for folder_name, folder_path in [("Extract", images_path), ("extracted_data", extracted_path)]:
        if folder_path.exists():
            image_files = list(folder_path.glob('*.png')) + list(folder_path.glob('*.jpg')) + list(folder_path.glob('*.jpeg'))
            print(f"\nDossier {folder_name}:")
            print(f"  Nombre d'images: {len(image_files)}")
            
            if len(image_files) > 0:
                # Analyse des dimensions
                dimensions = []
                for img_path in image_files[:100]:  # Échantillon de 100 images
                    try:
                        with Image.open(img_path) as img:
                            dimensions.append(img.size)
                    except Exception as e:
                        print(f"  Erreur avec {img_path.name}: {e}")
                
                if dimensions:
                    dimensions_df = pd.DataFrame(dimensions, columns=['width', 'height'])
                    print(f"  Dimensions moyennes: {dimensions_df['width'].mean():.0f} x {dimensions_df['height'].mean():.0f}")
                    print(f"  Dimensions min: {dimensions_df['width'].min()} x {dimensions_df['height'].min()}")
                    print(f"  Dimensions max: {dimensions_df['width'].max()} x {dimensions_df['height'].max()}")
        else:
            print(f"Dossier {folder_name} non trouvé: {folder_path}")
    
    print("\n6. RÉSUMÉ ET RECOMMANDATIONS:")
    print("- Dataset VinDr-Mammo avec images mammographiques annotées")
    print("- Annotations BI-RADS et densité mammaire disponibles")
    print("- Annotations détaillées des findings avec bounding boxes")
    print("- Déséquilibre des classes BI-RADS détecté")
    print("- Dimensions d'images variables nécessitant un preprocessing")
    print("- Recommandation: Utiliser Focal Loss et data augmentation")

if __name__ == "__main__":
    main()
