"""
Modèle MedSigLIP-448 pour l'analyse de mammographies avec de meilleures performances
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoProcessor, AutoModel
from PIL import Image
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class MedSigLIPMammographyModel:
    """
    Modèle MedSigLIP-448 spécialisé pour l'analyse de mammographies
    """
    
    def __init__(self, 
                 num_bi_rads_classes: int = 5,
                 num_density_classes: int = 4,
                 num_view_classes: int = 4,
                 num_finding_classes: int = 5,
                 device: str = "auto"):
        """
        Initialize MedSigLIP model for mammography analysis
        
        Args:
            num_bi_rads_classes: Number of BI-RADS classes
            num_density_classes: Number of density classes
            num_view_classes: Number of view classes (CC_L, CC_R, MLO_L, MLO_R)
            num_finding_classes: Number of finding classes (Mass, Calcification, etc.)
            device: Device to run on ("auto", "cuda", "cpu")
        """
        self.num_bi_rads_classes = num_bi_rads_classes
        self.num_density_classes = num_density_classes
        self.num_view_classes = num_view_classes
        self.num_finding_classes = num_finding_classes
        
        # Setup device
        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        print(f"Using device: {self.device}")
        
        # Load MedSigLIP model and processor
        print("[DEBUG] About to load MedSigLIP model...")
        self.load_medsiglip_model()
        print("[DEBUG] Model loaded, creating classification heads...")
        
        # Create classification heads
        self.create_classification_heads()
        print("[DEBUG] Classification heads created!")
        
    def load_medsiglip_model(self):
        """Load MedSigLIP-448 model and processor"""
        import sys
        print("Loading MedSigLIP-448 model with your token...")
        print("[INFO] This may take a few minutes on first run (model is ~2GB)...")
        
        try:
            # Load MedSigLIP model and processor with token from environment or cache
            # Utiliser la variable d'environnement HF_TOKEN ou le token en cache
            import os
            hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")
            print(f"Attempting to load google/medsiglip-448...")
            
            # Try loading from cache first, then download if needed
            print("[INFO] Attempting to load from cache...")
            sys.stdout.flush()
            
            # Load processor (will use cache if available)
            print("[INFO] Loading processor...")
            sys.stdout.flush()
            
            # Force garbage collection before loading to release any file locks
            import gc
            gc.collect()
            sys.stdout.flush()
            
            # Load with explicit cache directory
            import os
            cache_dir = os.path.expanduser('~/.cache/huggingface')
            
            print("[DEBUG] About to call AutoProcessor.from_pretrained...")
            sys.stdout.flush()
            
            # Don't use local_files_only - let HuggingFace handle caching automatically
            self.processor = AutoProcessor.from_pretrained(
                "google/medsiglip-448", 
                token=hf_token,
                cache_dir=cache_dir,
                trust_remote_code=False,
                force_download=False,
                local_files_only=False
            )
            
            print("[OK] Processor loaded!")
            sys.stdout.flush()
            
            # Load model (will use cache if available)
            print("[INFO] Loading model...")
            sys.stdout.flush()
            self.model = AutoModel.from_pretrained(
                "google/medsiglip-448", 
                token=hf_token
            )
            print("[OK] Model loaded!")
            sys.stdout.flush()
            
            print("[OK] MedSigLIP-448 model and processor loaded successfully!")
            sys.stdout.flush()
            
            # Move model to device for inference
            self.model = self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode
            print(f"[INFO] Model moved to device: {self.device} and set to eval mode")
            sys.stdout.flush()
            
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Error loading MedSigLIP model: {e}")
            print(f"Error type: {type(e).__name__}")
            import traceback
            print("\nFull traceback:")
            traceback.print_exc()
            print("\nPossible solutions:")
            print("1. Check if the Hugging Face token is valid")
            print("2. Check your internet connection")
            print("3. Verify that 'google/medsiglip-448' is available")
            print("4. Try: huggingface-cli login --token YOUR_TOKEN")
            print("5. Check available RAM (model needs ~4GB)")
            raise
    
    def create_classification_heads(self):
        """Create classification heads for BI-RADS, density, and view detection"""
        # Get embedding dimension from model
        # For SigLIP, use projection_dim or hidden_size
        # For ResNet, use num_channels
        embedding_dim = getattr(self.model.config, 'projection_dim', 
                               getattr(self.model.config, 'hidden_size', 
                               getattr(self.model.config, 'num_channels', 2048)))
        
        # BI-RADS classification head
        self.bi_rads_classifier = nn.Sequential(
            nn.Linear(embedding_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, self.num_bi_rads_classes)
        ).to(self.device)
        
        # Density classification head
        self.density_classifier = nn.Sequential(
            nn.Linear(embedding_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, self.num_density_classes)
        ).to(self.device)
        
        # View classification head (CC_L, CC_R, MLO_L, MLO_R)
        self.view_classifier = nn.Sequential(
            nn.Linear(embedding_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, self.num_view_classes)
        ).to(self.device)
        
        # Finding classification head (Mass, Calcification, Asymmetry, etc.)
        self.finding_classifier = nn.Sequential(
            nn.Linear(embedding_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, self.num_finding_classes)
        ).to(self.device)
        
        print("Classification heads created successfully!")
        print(f"  - BI-RADS classes: {self.num_bi_rads_classes}")
        print(f"  - Density classes: {self.num_density_classes}")
        print(f"  - View classes: {self.num_view_classes}")
        print(f"  - Finding classes: {self.num_finding_classes}")
    
    def preprocess_image(self, image_path: str) -> torch.Tensor:
        """
        Preprocess mammography image for MedSigLIP
        
        Args:
            image_path: Path to image file
            
        Returns:
            Preprocessed image tensor
        """
        try:
            # Load image
            image = Image.open(image_path).convert("RGB")
            
            # Resize to 448x448 (MedSigLIP input size)
            image = image.resize((448, 448))
            
            # Process with MedSigLIP processor
            inputs = self.processor(images=[image], return_tensors="pt")
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            return inputs
            
        except Exception as e:
            print(f"Error preprocessing image {image_path}: {e}")
            return None
    
    def get_image_embedding(self, image_path: str) -> torch.Tensor:
        """
        Get image embedding from MedSigLIP
        
        Args:
            image_path: Path to image file
            
        Returns:
            Image embedding tensor
        """
        try:
            # Preprocess image
            inputs = self.preprocess_image(image_path)
            if inputs is None:
                return None
            
            # Get image embedding
            with torch.no_grad():
                outputs = self.model(**inputs)
                image_embedding = outputs.image_embeds
            
            return image_embedding
            
        except Exception as e:
            print(f"Error getting image embedding: {e}")
            return None
    
    def predict_single_image(self, image_path: str) -> Dict[str, np.ndarray]:
        """
        Predict BI-RADS, density, and view for a single image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with predictions and probabilities
        """
        try:
            # Get image embedding
            image_embedding = self.get_image_embedding(image_path)
            if image_embedding is None:
                return None
            
            # Get predictions from classification heads
            bi_rads_logits = self.bi_rads_classifier(image_embedding)
            density_logits = self.density_classifier(image_embedding)
            view_logits = self.view_classifier(image_embedding)
            finding_logits = self.finding_classifier(image_embedding)
            
            # Convert to probabilities
            bi_rads_probs = F.softmax(bi_rads_logits, dim=-1)
            density_probs = F.softmax(density_logits, dim=-1)
            view_probs = F.softmax(view_logits, dim=-1)
            finding_probs = F.softmax(finding_logits, dim=-1)
            
            # Get predictions
            bi_rads_pred = torch.argmax(bi_rads_probs, dim=-1)
            density_pred = torch.argmax(density_probs, dim=-1)
            view_pred = torch.argmax(view_probs, dim=-1)
            finding_pred = torch.argmax(finding_probs, dim=-1)
            
            # Convert view prediction to string
            view_classes = ['CC_L', 'CC_R', 'MLO_L', 'MLO_R']
            view_pred_str = view_classes[view_pred.cpu().numpy()[0]]
            
            # Convert finding prediction to string
            finding_classes = ['No Finding', 'Mass', 'Calcification', 'Asymmetry', 'Architectural Distortion']
            finding_pred_str = finding_classes[finding_pred.cpu().numpy()[0]]
            
            return {
                'bi_rads_prediction': bi_rads_pred.cpu().numpy()[0],
                'density_prediction': density_pred.cpu().numpy()[0],
                'view_prediction': view_pred_str,
                'finding_prediction': finding_pred_str,
                'bi_rads_probabilities': bi_rads_probs.cpu().numpy()[0],
                'density_probabilities': density_probs.cpu().numpy()[0],
                'view_probabilities': view_probs.cpu().numpy()[0],
                'finding_probabilities': finding_probs.cpu().numpy()[0]
            }
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None
    
    def predict_multi_view(self, image_paths: Dict[str, str]) -> Dict[str, np.ndarray]:
        """
        Predict BI-RADS and density for multi-view mammography
        
        Args:
            image_paths: Dictionary with view names as keys and paths as values
            Expected keys: 'CC_L', 'CC_R', 'MLO_L', 'MLO_R'
            
        Returns:
            Dictionary with predictions and probabilities
        """
        try:
            # Get embeddings for all views
            embeddings = {}
            for view, path in image_paths.items():
                embedding = self.get_image_embedding(path)
                if embedding is not None:
                    embeddings[view] = embedding
            
            if len(embeddings) == 0:
                print("No valid images found!")
                return None
            
            # Combine embeddings (simple average)
            combined_embedding = torch.mean(torch.stack(list(embeddings.values())), dim=0)
            
            # Get predictions from classification heads
            bi_rads_logits = self.bi_rads_classifier(combined_embedding)
            density_logits = self.density_classifier(combined_embedding)
            
            # Convert to probabilities
            bi_rads_probs = F.softmax(bi_rads_logits, dim=-1)
            density_probs = F.softmax(density_logits, dim=-1)
            
            # Get predictions
            bi_rads_pred = torch.argmax(bi_rads_probs, dim=-1)
            density_pred = torch.argmax(density_probs, dim=-1)
            
            return {
                'bi_rads_prediction': bi_rads_pred.cpu().numpy()[0],
                'density_prediction': density_pred.cpu().numpy()[0],
                'bi_rads_probabilities': bi_rads_probs.cpu().numpy()[0],
                'density_probabilities': density_probs.cpu().numpy()[0],
                'views_processed': list(embeddings.keys())
            }
            
        except Exception as e:
            print(f"Error in multi-view prediction: {e}")
            return None
    
    def save_model(self, path: str):
        """Save the complete model"""
        try:
            torch.save({
                'bi_rads_classifier': self.bi_rads_classifier.state_dict(),
                'density_classifier': self.density_classifier.state_dict(),
                'view_classifier': self.view_classifier.state_dict(),
                'finding_classifier': self.finding_classifier.state_dict(),
                'num_bi_rads_classes': self.num_bi_rads_classes,
                'num_density_classes': self.num_density_classes,
                'num_view_classes': self.num_view_classes,
                'num_finding_classes': self.num_finding_classes
            }, path)
            print(f"Model saved to {path}")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self, path: str):
        """Load a saved model"""
        try:
            checkpoint = torch.load(path, map_location=self.device)
            self.bi_rads_classifier.load_state_dict(checkpoint['bi_rads_classifier'])
            self.density_classifier.load_state_dict(checkpoint['density_classifier'])
            
            # Load view classifier if it exists in the checkpoint
            if 'view_classifier' in checkpoint:
                self.view_classifier.load_state_dict(checkpoint['view_classifier'])
                print("View classifier loaded successfully!")
            else:
                print("Warning: View classifier not found in checkpoint. Using random initialization.")
            
            # Load finding classifier if it exists in the checkpoint
            if 'finding_classifier' in checkpoint:
                self.finding_classifier.load_state_dict(checkpoint['finding_classifier'])
                print("Finding classifier loaded successfully!")
            else:
                print("Warning: Finding classifier not found in checkpoint. Using random initialization.")
            
            print(f"Model loaded from {path}")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def detect_regions_from_annotations(self, image_path: str, study_id: str = None) -> list:
        """
        Detect regions of interest based on VinDr-Mammo annotations
        This replaces placeholder regions with real annotated regions
        """
        try:
            import pandas as pd
            
            # Load finding annotations if not already loaded
            if not hasattr(self, 'finding_annotations'):
                self.finding_annotations = pd.read_csv('finding_annotations (1).csv')
            
            # Extract image_id from path if study_id not provided
            if study_id is None:
                image_filename = os.path.basename(image_path)
                # Try to match with annotations (this is a simplified approach)
                # In practice, you'd need a mapping between filenames and image_ids
                return []
            
            # Find annotations for this study
            study_annotations = self.finding_annotations[
                self.finding_annotations['study_id'] == study_id
            ]
            
            regions = []
            for _, annotation in study_annotations.iterrows():
                # Parse finding categories
                finding_categories = eval(annotation['finding_categories']) if isinstance(annotation['finding_categories'], str) else annotation['finding_categories']
                
                # Get bounding box coordinates
                bbox = {
                    'xmin': int(annotation['xmin']),
                    'ymin': int(annotation['ymin']),
                    'xmax': int(annotation['xmax']),
                    'ymax': int(annotation['ymax'])
                }
                
                # Determine region type and confidence
                finding_type = finding_categories[0] if finding_categories else 'Unknown'
                bi_rads_level = annotation['finding_birads']
                
                # Calculate confidence based on BI-RADS level
                confidence_map = {
                    'BI-RADS 3': 0.7,
                    'BI-RADS 4': 0.85,
                    'BI-RADS 5': 0.95
                }
                confidence = confidence_map.get(bi_rads_level, 0.6)
                
                # Get description
                description = self._get_finding_description(finding_type, bi_rads_level)
                
                regions.append({
                    'id': f"region_{len(regions)+1}",
                    'type': finding_type.lower().replace(' ', '_'),
                    'confidence': confidence,
                    'bbox': bbox,
                    'bi_rads': bi_rads_level,
                    'description': description,
                    'finding_categories': finding_categories
                })
            
            return regions
            
        except Exception as e:
            print(f"Error detecting regions from annotations: {e}")
            return []
    
    def _get_finding_description(self, finding_type: str, bi_rads_level: str) -> str:
        """Get description for detected finding based on type and BI-RADS level"""
        descriptions = {
            'Mass': {
                'BI-RADS 3': 'Masse probablement bénigne nécessitant un suivi',
                'BI-RADS 4': 'Masse suspecte nécessitant une évaluation histologique',
                'BI-RADS 5': 'Masse hautement suspecte de malignité'
            },
            'Calcification': {
                'BI-RADS 3': 'Calcifications probablement bénignes',
                'BI-RADS 4': 'Calcifications suspectes nécessitant une évaluation',
                'BI-RADS 5': 'Calcifications très suspectes de malignité'
            },
            'Global Asymmetry': {
                'BI-RADS 3': 'Asymétrie globale probablement bénigne',
                'BI-RADS 4': 'Asymétrie suspecte nécessitant une évaluation',
                'BI-RADS 5': 'Asymétrie très suspecte de malignité'
            },
            'Architectural Distortion': {
                'BI-RADS 3': 'Distorsion architecturale probablement bénigne',
                'BI-RADS 4': 'Distorsion architecturale suspecte',
                'BI-RADS 5': 'Distorsion architecturale très suspecte de malignité'
            }
        }
        
        return descriptions.get(finding_type, {}).get(bi_rads_level, f"{finding_type} détecté")
    
    def get_model_info(self):
        """Get model information"""
        total_params = sum(p.numel() for p in self.model.parameters())
        classifier_params = sum(p.numel() for p in self.bi_rads_classifier.parameters()) + \
                           sum(p.numel() for p in self.density_classifier.parameters()) + \
                           sum(p.numel() for p in self.view_classifier.parameters()) + \
                           sum(p.numel() for p in self.finding_classifier.parameters())
        
        return {
            'medsiglip_params': total_params,
            'classifier_params': classifier_params,
            'total_params': total_params + classifier_params,
            'device': self.device,
            'bi_rads_classes': self.num_bi_rads_classes,
            'density_classes': self.num_density_classes,
            'view_classes': self.num_view_classes,
            'finding_classes': self.num_finding_classes
        }


def test_medsiglip_model():
    """Test the MedSigLIP model"""
    print("Testing MedSigLIP Mammography Model...")
    
    try:
        # Create model
        model = MedSigLIPMammographyModel()
        
        # Get model info
        info = model.get_model_info()
        print(f"Model info: {info}")
        
        # Test with dummy image paths (replace with real paths)
        dummy_paths = {
            'CC_L': 'dummy_path_cc_l.png',
            'CC_R': 'dummy_path_cc_r.png',
            'MLO_L': 'dummy_path_mlo_l.png',
            'MLO_R': 'dummy_path_mlo_r.png'
        }
        
        print("Model created successfully!")
        print("Note: To test with real images, provide valid image paths")
        
    except Exception as e:
        print(f"Error testing model: {e}")


if __name__ == "__main__":
    test_medsiglip_model()
