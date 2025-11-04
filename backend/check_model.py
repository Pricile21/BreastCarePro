"""Script rapide pour vérifier l'état du modèle"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

print("Vérification du chargement du modèle...")

try:
    from app.ml.inference_service_simple import MedSigLIPInferenceService
    
    service = MedSigLIPInferenceService()
    
    print("\n=== ÉTAT DU MODÈLE ===")
    print(f"Checkpoint chargé: {service.checkpoint is not None}")
    print(f"use_direct_classifiers: {getattr(service, 'use_direct_classifiers', False)}")
    print(f"bi_rads_classifier chargé: {hasattr(service, 'bi_rads_classifier') and service.bi_rads_classifier is not None}")
    print(f"density_classifier chargé: {hasattr(service, 'density_classifier') and service.density_classifier is not None}")
    
    if service.checkpoint and isinstance(service.checkpoint, dict):
        print(f"\nClés du checkpoint: {list(service.checkpoint.keys())[:10]}")
        
except Exception as e:
    print(f"Erreur: {e}")
    import traceback
    traceback.print_exc()

