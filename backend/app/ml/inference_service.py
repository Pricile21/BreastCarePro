#!/usr/bin/env python3
"""
Service d'inference pour le modèle MedSigLIP entraîné
Utilise le modèle best_medsiglip_model.pth pour la prédiction
"""

import torch
import torch.nn as nn
import numpy as np
import cv2
from PIL import Image
import os
from pathlib import Path
from transformers import AutoProcessor, AutoModel
import warnings
warnings.filterwarnings("ignore")

class MedSigLIPInferenceService:
    """
    Service d'inference pour MedSigLIP
    """
    
    def __init__(self, model_path="model/best_medsiglip_model.pth", device="cpu"):
        self.device = device
        self.model_path = model_path
        self.model = None
        self.processor = None
        self.bi_rads_classes = ['BI-RADS 1', 'BI-RADS 2', 'BI-RADS 3', 'BI-RADS 4', 'BI-RADS 5']
        self.density_classes = ['DENSITY A', 'DENSITY B', 'DENSITY C', 'DENSITY D']
        
        print("=== MEDSIGLIP INFERENCE SERVICE ===")
        print("Chargement du modèle MedSigLIP...")
        self.load_model()
    
    def load_model(self):
        """Charger le modèle MedSigLIP entraîné"""
        try:
            # Charger le modèle PyTorch
            if os.path.exists(self.model_path):
                self.model = torch.load(self.model_path, map_location=self.device)
                self.model.eval()
                print(f"✅ Modèle chargé: {self.model_path}")
            else:
                print(f"❌ Modèle non trouvé: {self.model_path}")
                return False
            
            # Charger le processeur MedSigLIP
            # Utiliser la variable d'environnement HF_TOKEN ou le token en cache
            hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")
            self.processor = AutoProcessor.from_pretrained("google/medsiglip-448", token=hf_token)
            print("✅ Processeur MedSigLIP chargé")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def preprocess_image(self, image_path):
        """Préprocesser une image pour MedSigLIP"""
        try:
            # Charger l'image
            if isinstance(image_path, str):
                image = Image.open(image_path).convert('RGB')
            else:
                image = image_path
            
            # Redimensionner à 448x448 (taille MedSigLIP)
            image = image.resize((448, 448))
            
            # Convertir en array numpy
            image_array = np.array(image)
            
            return image_array
            
        except Exception as e:
            print(f"❌ Erreur préprocessing: {e}")
            return None
    
    def predict_single_image(self, image_path):
        """Prédire sur une seule image"""
        try:
            # Préprocesser l'image
            image_array = self.preprocess_image(image_path)
            if image_array is None:
                return None
            
            # Traiter avec MedSigLIP
            inputs = self.processor(images=image_array, return_tensors="pt")
            
            # Déplacer vers le device
            for key in inputs:
                inputs[key] = inputs[key].to(self.device)
            
            # Prédiction
            with torch.no_grad():
                # Extraire les embeddings
                vision_outputs = self.model.model.vision_model(**inputs)
                embeddings = vision_outputs.pooler_output
                
                # Prédictions
                bi_rads_logits = self.model.bi_rads_classifier(embeddings)
                density_logits = self.model.density_classifier(embeddings)
                
                # Probabilités
                bi_rads_probs = torch.softmax(bi_rads_logits, dim=-1)
                density_probs = torch.softmax(density_logits, dim=-1)
                
                # Classes prédites
                bi_rads_pred = torch.argmax(bi_rads_probs, dim=-1).item()
                density_pred = torch.argmax(density_probs, dim=-1).item()
                
                # Confiance
                bi_rads_confidence = bi_rads_probs[0][bi_rads_pred].item()
                density_confidence = density_probs[0][density_pred].item()
            
            # Résultats
            results = {
                'bi_rads': {
                    'prediction': self.bi_rads_classes[bi_rads_pred],
                    'confidence': bi_rads_confidence,
                    'probabilities': {
                        class_name: prob.item() 
                        for class_name, prob in zip(self.bi_rads_classes, bi_rads_probs[0])
                    }
                },
                'density': {
                    'prediction': self.density_classes[density_pred],
                    'confidence': density_confidence,
                    'probabilities': {
                        class_name: prob.item() 
                        for class_name, prob in zip(self.density_classes, density_probs[0])
                    }
                }
            }
            
            return results
            
        except Exception as e:
            print(f"❌ Erreur prédiction: {e}")
            return None
    
    def predict_batch(self, image_paths):
        """Prédire sur un batch d'images"""
        results = []
        
        for i, image_path in enumerate(image_paths):
            print(f"📊 Traitement image {i+1}/{len(image_paths)}: {os.path.basename(image_path)}")
            
            result = self.predict_single_image(image_path)
            if result:
                result['image_path'] = image_path
                results.append(result)
            else:
                results.append({
                    'image_path': image_path,
                    'error': 'Erreur de traitement'
                })
        
        return results
    
    def get_model_info(self):
        """Obtenir les informations du modèle"""
        if self.model is None:
            return None
        
        info = {
            'model_type': 'MedSigLIP-448',
            'device': self.device,
            'model_path': self.model_path,
            'bi_rads_classes': self.bi_rads_classes,
            'density_classes': self.density_classes,
            'model_loaded': True
        }
        
        return info

def main():
    """Test du service d'inference"""
    print("=== TEST MEDSIGLIP INFERENCE SERVICE ===")
    
    # Créer le service
    service = MedSigLIPInferenceService()
    
    # Vérifier que le modèle est chargé
    if service.model is None:
        print("❌ Impossible de charger le modèle")
        return
    
    # Informations du modèle
    info = service.get_model_info()
    print(f"📊 Modèle: {info['model_type']}")
    print(f"📊 Device: {info['device']}")
    print(f"📊 Classes BI-RADS: {len(info['bi_rads_classes'])}")
    print(f"📊 Classes Density: {len(info['density_classes'])}")
    
    # Test avec une image (si disponible)
    test_image = "extracted_data/images/sample.jpg"  # Remplacer par une vraie image
    if os.path.exists(test_image):
        print(f"\n🧪 Test avec: {test_image}")
        result = service.predict_single_image(test_image)
        if result:
            print(f"✅ BI-RADS: {result['bi_rads']['prediction']} (confiance: {result['bi_rads']['confidence']:.3f})")
            print(f"✅ Density: {result['density']['prediction']} (confiance: {result['density']['confidence']:.3f})")
        else:
            print("❌ Erreur de prédiction")
    else:
        print("⚠️  Aucune image de test trouvée")
    
    print("\n🎉 Service d'inference prêt !")

if __name__ == "__main__":
    main()
