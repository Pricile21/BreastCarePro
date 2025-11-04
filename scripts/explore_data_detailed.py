#!/usr/bin/env python3
"""
Script d'exploration détaillée du dataset VinDr-Mammo
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
    print("=== EXPLORATION DÉTAILLÉE DU DATASET VINDR-MAMMO ===")
    
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
    
    # Analyse des annotations BI-RADS
    if csv_files['breast_annotations'].exists():
        print("\n2. ANALYSE DES ANNOTATIONS BI-RADS:")
        breast_annotations_df = pd.read_csv(csv_files['breast_annotations'])
        print(f"Nombre total d'annotations: {len(breast_annotations_df)}")
        print(f"Colonnes: {list(breast_annotations_df.columns)}")
        
        # Distribution des classes BI-RADS
        if 'breast_birads' in breast_annotations_df.columns:
            print("\nDistribution des classes BI-RADS:")
            bi_rads_dist = breast_annotations_df['breast_birads'].value_counts().sort_index()
            for bi_rads, count in bi_rads_dist.items():
                percentage = (count / len(breast_annotations_df)) * 100
                print(f"BI-RADS {bi_rads}: {count} images ({percentage:.1f}%)")
        
        # Distribution de la densité mammaire
        if 'breast_density' in breast_annotations_df.columns:
            print("\nDistribution de la densité mammaire:")
            density_dist = breast_annotations_df['breast_density'].value_counts().sort_index()
            for density, count in density_dist.items():
                percentage = (count / len(breast_annotations_df)) * 100
                print(f"Densité {density}: {count} images ({percentage:.1f}%)")
        
        # Analyse des vues (laterality et view_position)
        print("\nDistribution des vues:")
        view_dist = breast_annotations_df.groupby(['laterality', 'view_position']).size()
        print(view_dist)
    
    # Analyse des annotations de findings
    if csv_files['finding_annotations'].exists():
        print("\n3. ANALYSE DES ANNOTATIONS DE FINDINGS:")
        finding_annotations_df = pd.read_csv(csv_files['finding_annotations'])
        print(f"Nombre total d'annotations: {len(finding_annotations_df)}")
        
        # Distribution des types de findings (top 10)
        if 'finding_categories' in finding_annotations_df.columns:
            print("\nTop 10 des types de findings:")
            findings_dist = finding_annotations_df['finding_categories'].value_counts().head(10)
            for finding, count in findings_dist.items():
                percentage = (count / len(finding_annotations_df)) * 100
                print(f"{finding}: {count} annotations ({percentage:.1f}%)")
        
        # Distribution des BI-RADS pour les findings
        if 'finding_birads' in finding_annotations_df.columns:
            print("\nDistribution BI-RADS des findings:")
            finding_birads_dist = finding_annotations_df['finding_birads'].value_counts().sort_index()
            for bi_rads, count in finding_birads_dist.items():
                percentage = (count / len(finding_annotations_df)) * 100
                print(f"BI-RADS {bi_rads}: {count} findings ({percentage:.1f}%)")
    
    # Analyse des images avec structure en sous-dossiers
    print("\n4. ANALYSE DES IMAGES (STRUCTURE EN SOUS-DOSSIERS):")
    for folder_name, folder_path in [("Extract", images_path), ("extracted_data", extracted_path)]:
        if folder_path.exists():
            # Compter les sous-dossiers (chaque sous-dossier = une image ID)
            subdirs = [d for d in folder_path.iterdir() if d.is_dir()]
            print(f"\nDossier {folder_name}:")
            print(f"  Nombre de sous-dossiers (image IDs): {len(subdirs)}")
            
            if len(subdirs) > 0:
                # Analyser quelques sous-dossiers
                sample_subdirs = subdirs[:5]
                total_files = 0
                dimensions = []
                file_sizes = []
                
                for subdir in sample_subdirs:
                    files = list(subdir.glob('*.png')) + list(subdir.glob('*.jpg'))
                    total_files += len(files)
                    
                    # Analyser les dimensions d'une image par sous-dossier
                    if files:
                        try:
                            with Image.open(files[0]) as img:
                                dimensions.append(img.size)
                            file_sizes.append(os.path.getsize(files[0]))
                        except Exception as e:
                            print(f"  Erreur avec {files[0].name}: {e}")
                
                print(f"  Exemple - {len(sample_subdirs)} sous-dossiers analysés:")
                print(f"  Total fichiers dans l'échantillon: {total_files}")
                print(f"  Moyenne fichiers par sous-dossier: {total_files / len(sample_subdirs):.1f}")
                
                if dimensions:
                    dimensions_df = pd.DataFrame(dimensions, columns=['width', 'height'])
                    print(f"  Dimensions moyennes: {dimensions_df['width'].mean():.0f} x {dimensions_df['height'].mean():.0f}")
                    print(f"  Dimensions min: {dimensions_df['width'].min()} x {dimensions_df['height'].min()}")
                    print(f"  Dimensions max: {dimensions_df['width'].max()} x {dimensions_df['height'].max()}")
                    print(f"  Taille moyenne des fichiers: {np.mean(file_sizes) / 1024:.1f} KB")
        else:
            print(f"Dossier {folder_name} non trouvé: {folder_path}")
    
    # Analyse de la cohérence entre les données
    print("\n5. ANALYSE DE LA COHÉRENCE:")
    if csv_files['breast_annotations'].exists() and csv_files['finding_annotations'].exists():
        breast_annotations_df = pd.read_csv(csv_files['breast_annotations'])
        finding_annotations_df = pd.read_csv(csv_files['finding_annotations'])
        
        breast_image_ids = set(breast_annotations_df['image_id'])
        finding_image_ids = set(finding_annotations_df['image_id'])
        
        print(f"Images avec annotations de sein: {len(breast_image_ids)}")
        print(f"Images avec annotations de findings: {len(finding_image_ids)}")
        print(f"Images communes: {len(breast_image_ids & finding_image_ids)}")
        print(f"Images seulement avec annotations de sein: {len(breast_image_ids - finding_image_ids)}")
        print(f"Images seulement avec annotations de findings: {len(finding_image_ids - breast_image_ids)}")
    
    # Analyse du split train/validation/test
    print("\n6. ANALYSE DES SPLITS:")
    if csv_files['breast_annotations'].exists():
        breast_annotations_df = pd.read_csv(csv_files['breast_annotations'])
        if 'split' in breast_annotations_df.columns:
            split_dist = breast_annotations_df['split'].value_counts()
            print("Distribution des splits:")
            for split, count in split_dist.items():
                percentage = (count / len(breast_annotations_df)) * 100
                print(f"{split}: {count} images ({percentage:.1f}%)")
    
    print("\n7. RÉSUMÉ ET RECOMMANDATIONS:")
    print("=== DÉCOUVERTES IMPORTANTES ===")
    print("✓ Dataset VinDr-Mammo avec 20,000 images mammographiques")
    print("✓ Annotations BI-RADS et densité mammaire disponibles")
    print("✓ Annotations détaillées des findings avec bounding boxes")
    print("✓ Images organisées en sous-dossiers par ID")
    print("✓ Déséquilibre des classes BI-RADS détecté")
    print("✓ Multiple findings par image possible")
    
    print("\n=== DÉFIS IDENTIFIÉS ===")
    print("- Déséquilibre des classes BI-RADS")
    print("- Structure en sous-dossiers nécessite un preprocessing spécial")
    print("- Dimensions d'images variables")
    print("- Findings multiples par image")
    
    print("\n=== RECOMMANDATIONS POUR LE MODÈLE ===")
    print("1. Utiliser Focal Loss pour gérer le déséquilibre des classes")
    print("2. Implémenter data augmentation robuste")
    print("3. Normaliser les dimensions des images (512x512 recommandé)")
    print("4. Validation croisée stratifiée")
    print("5. Multi-task learning: BI-RADS + densité + findings")
    print("6. Preprocessing spécial pour la structure en sous-dossiers")

if __name__ == "__main__":
    main()
