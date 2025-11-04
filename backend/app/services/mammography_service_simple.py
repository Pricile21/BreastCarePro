"""
Simplified mammography service without MedSigLIP dependencies
"""

from typing import List, Optional
from datetime import datetime
import uuid
import os
import cv2
import numpy as np
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from app.models.mammography import MammographyAnalysis, BI_RADS_Category, AnalysisStatus
from app.schemas.mammography import MammographyAnalysisResponse
from app.ml.inference_service_simple import MedSigLIPInferenceService
from app.models.patient import Patient


class MammographyService:
    """
    Simplified service for mammography analysis operations
    """
    
    def __init__(self, db: Session):
        self.db = db
        print("🔧 Initialisation du MammographyService...")
        self.ml_model = MedSigLIPInferenceService() # Now using the real MedSigLIP model
        
        # VÉRIFICATION CRITIQUE: Le modèle DOIT être chargé, sinon erreur au démarrage
        if not self.ml_model:
            raise RuntimeError("❌ ERREUR CRITIQUE: Le modèle ML n'a pas pu être initialisé. Le backend ne peut pas fonctionner sans le modèle.")
        
        if not self.ml_model.checkpoint:
            raise RuntimeError(
                "❌ ERREUR CRITIQUE: Le checkpoint du modèle (best_medsiglip_model.pth) n'est pas chargé. "
                "Vérifiez que le fichier existe dans backend/app/ml/model/best_medsiglip_model.pth"
            )
        
        if not self.ml_model.use_direct_classifiers or self.ml_model.bi_rads_classifier is None:
            raise RuntimeError(
                "❌ ERREUR CRITIQUE: Vos classificateurs entraînés ne sont pas chargés. "
                "Vérifiez que best_medsiglip_model.pth contient bien les classificateurs (bi_rads_classifier, density_classifier)."
            )
        
        print(f"✅✅✅ VOTRE MODÈLE BEST EST CHARGÉ ET PRÊT!")
        print(f"🔧 État du modèle après initialisation:")
        print(f"   - ml_model existe: {self.ml_model is not None}")
        print(f"   - use_direct_classifiers: {self.ml_model.use_direct_classifiers}")
        print(f"   - bi_rads_classifier chargé: {self.ml_model.bi_rads_classifier is not None}")
        print(f"   - density_classifier chargé: {self.ml_model.density_classifier is not None}")
        print(f"   - full_model chargé: {self.ml_model.full_model is not None}")
        print(f"   - checkpoint chargé: {self.ml_model.checkpoint is not None}")
        self.start_time = datetime.now() # Initialize start_time here
    
    async def analyze_mammography(
        self, 
        files: List[UploadFile], 
        patient_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> MammographyAnalysisResponse:
        """
        Analyze mammography images (simplified version)
        """
        try:
            # Generate analysis ID
            analysis_id = str(uuid.uuid4())
            
            # Save uploaded files and get file data with view types
            file_data = await self._save_uploaded_files(files, analysis_id)
            file_paths = [file_info["path"] for file_info in file_data]
            
            # Si pas de patient_id fourni, créer un patient par défaut
            if not patient_id:
                patient_id = f"P-{analysis_id[:8].upper()}"
            
            # Si pas de user_id fourni, utiliser un utilisateur par défaut
            if not user_id:
                user_id = "user-001"  # Utilisateur Dr GANGBE
            
            # Récupérer l'UUID du patient depuis la table patients
            # La contrainte de clé étrangère utilise patients(id), pas patients(patient_id)
            patient = self.db.query(Patient).filter(Patient.patient_id == patient_id).first()
            if not patient:
                raise HTTPException(
                    status_code=404,
                    detail=f"Patient avec patient_id='{patient_id}' non trouvé dans la base de données"
                )
            # Utiliser l'UUID du patient (id) au lieu de patient_id pour la contrainte FK
            patient_uuid = patient.id
            
            # Run simplified ML analysis
            # IMPORTANT: Cette méthode peut lever une ValueError si des images sont invalides
            # Cette exception sera capturée et transformée en HTTPException sans créer d'enregistrement
            analysis_result = await self._run_ml_analysis(file_paths)
            
            # Create analysis record
            analysis = MammographyAnalysis(
                id=str(uuid.uuid4()),
                analysis_id=analysis_id,
                patient_id=patient_uuid,  # Utiliser l'UUID du patient (id) pour la FK
                user_id=user_id,
                bi_rads_category=analysis_result["bi_rads_category"],
                confidence_score=analysis_result["confidence_score"],
                breast_density=analysis_result["breast_density"],
                model_version=analysis_result["model_version"],
                processing_time=1.5,  # Simulated
                status=AnalysisStatus.COMPLETED,
                original_files=file_data,
                processed_images=file_data,
                annotations={},
                findings=analysis_result["findings"],
                recommendations=analysis_result["recommendations"],
                notes="Analyse MedSigLIP - Votre modèle best"
            )
            
            self.db.add(analysis)
            self.db.commit()
            self.db.refresh(analysis)
            
            return MammographyAnalysisResponse.from_orm(analysis)
            
        except ValueError as e:
            # Pour les erreurs de validation d'images (images invalides), ne PAS créer d'enregistrement
            # et lever l'exception directement pour que le frontend reçoive une erreur claire
            print(f"🚨 Erreur de validation - Analyse annulée: {str(e)}")
            print(f"🚨 Aucun enregistrement ne sera créé pour cette analyse")
            # Relancer l'exception telle quelle pour que l'endpoint la transforme en HTTPException
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            # Pour les autres erreurs (erreurs techniques), créer un enregistrement FAILED
            print(f"❌ Erreur technique lors de l'analyse: {str(e)}")
            import traceback
            traceback.print_exc()
            
            analysis = MammographyAnalysis(
                id=str(uuid.uuid4()),
                analysis_id=str(uuid.uuid4()),
                patient_id=patient_uuid if 'patient_uuid' in locals() else None,
                user_id=user_id if 'user_id' in locals() else None,
                bi_rads_category=BI_RADS_Category.CATEGORY_2,
                confidence_score=0.0,
                breast_density="Unknown",
                model_version="MedSigLIP-Best-v1.0 (En cas d'erreur)",
                processing_time=0.0,
                status=AnalysisStatus.FAILED,
                original_files=[],
                processed_images=[],
                annotations={},
                findings=f"Erreur d'analyse: {str(e)}",
                recommendations="Veuillez réessayer ou consulter un radiologue",
                notes=f"Erreur technique: {str(e)}"
            )
            
            try:
                self.db.add(analysis)
                self.db.commit()
            except:
                self.db.rollback()
            
            # Relancer l'exception pour que l'endpoint la transforme en HTTPException
            raise HTTPException(
                status_code=500,
                detail=f"Erreur technique lors de l'analyse: {str(e)}"
            )
    
    async def _save_uploaded_files(
        self, 
        files: List[UploadFile], 
        analysis_id: str
    ) -> List[dict]:
        """
        Save uploaded files to disk and return file data with view type
        """
        file_data = []
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        for file in files:
            # Create unique filename
            file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
            filename = f"{analysis_id}_{file.filename}"
            file_path = f"uploads/{filename}"
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Infer view type from image content using basic computer vision
            view_type = self._detect_mammography_view(file_path)
            
            file_data.append({
                "path": file_path,
                "view_type": view_type,
                "original_filename": file.filename
            })
        
        return file_data
    
    def _detect_mammography_view(self, image_path: str) -> str:
        """
        Detect mammography view type and side using computer vision analysis
        Robust algorithm with validation and fallback mechanisms
        Returns: CC_LEFT, CC_RIGHT, MLO_LEFT, MLO_RIGHT, or UNKNOWN
        """
        try:
            print(f"🔍 Analyse de l'image: {os.path.basename(image_path)}")
            
            # Load image
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                print("❌ Impossible de charger l'image")
                return "UNKNOWN"
            
            # Validate image quality
            if not self._validate_image_quality(image):
                print("⚠️ Qualité d'image insuffisante")
                return "UNKNOWN"
            
            # Get image dimensions
            height, width = image.shape
            print(f"📐 Dimensions: {width}x{height}")
            
            # Calculate aspect ratio
            aspect_ratio = width / height
            
            # Calculate image center and analyze symmetry
            center_x, center_y = width // 2, height // 2
            
            # Analyze left and right halves for side detection
            left_half = image[:, :center_x]
            right_half = image[:, center_x:]
            
            # Analyze top and bottom halves
            top_half = image[:center_y, :]
            bottom_half = image[center_y:, :]
            
            # Calculate brightness distribution
            left_brightness = np.mean(left_half)
            right_brightness = np.mean(right_half)
            top_brightness = np.mean(top_half)
            bottom_brightness = np.mean(bottom_half)
            
            # Calculate horizontal and vertical symmetry
            horizontal_symmetry = abs(left_brightness - right_brightness)
            vertical_symmetry = abs(top_brightness - bottom_brightness)
            
            # Analyze edge density (MLO views typically have more diagonal edges)
            edges = cv2.Canny(image, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            # Detect side (left vs right) based on breast tissue distribution
            side = self._detect_breast_side(image, left_brightness, right_brightness)
            
            # Detect view type (CC vs MLO)
            view_type = self._detect_view_type(aspect_ratio, horizontal_symmetry, vertical_symmetry, edge_density)
            
            # Validate the result
            result = f"{view_type}_{side}"
            if self._validate_detection_result(result, aspect_ratio, horizontal_symmetry, vertical_symmetry):
                print(f"✅ Vue détectée: {result}")
                return result
            else:
                print(f"⚠️ Résultat non validé, utilisation du fallback")
                return self._get_fallback_view(aspect_ratio)
                    
        except Exception as e:
            print(f"❌ Erreur lors de la détection de vue: {e}")
            return "UNKNOWN"
    
    def _validate_image_quality(self, image: np.ndarray) -> bool:
        """Validate that the image has sufficient quality for analysis"""
        try:
            height, width = image.shape
            
            # Check minimum dimensions
            if height < 100 or width < 100:
                return False
            
            # Check if image is not too dark or too bright
            mean_brightness = np.mean(image)
            if mean_brightness < 10 or mean_brightness > 245:
                return False
            
            # Check for sufficient contrast
            std_brightness = np.std(image)
            if std_brightness < 5:
                return False
            
            return True
        except:
            return False
    
    def _validate_detection_result(self, result: str, aspect_ratio: float, 
                                 horizontal_symmetry: float, vertical_symmetry: float) -> bool:
        """Validate the detection result based on consistency checks"""
        try:
            view_type, side = result.split('_')
            
            # Basic consistency checks
            if view_type not in ['CC', 'MLO'] or side not in ['LEFT', 'RIGHT']:
                return False
            
            # Check if aspect ratio is consistent with view type
            if view_type == 'CC' and (aspect_ratio > 1.4 or aspect_ratio < 0.6):
                return False
            elif view_type == 'MLO' and (0.9 <= aspect_ratio <= 1.1):
                return False
            
            return True
        except:
            return False
    
    def _get_fallback_view(self, aspect_ratio: float) -> str:
        """Get a fallback view based on aspect ratio only"""
        try:
            # Simple fallback based on aspect ratio
            if aspect_ratio > 1.2 or aspect_ratio < 0.8:
                return "MLO_LEFT"  # Default to MLO for elongated images
            else:
                return "CC_LEFT"   # Default to CC for square images
        except:
            return "CC_LEFT"
    
    def _detect_breast_side(self, image: np.ndarray, left_brightness: float, right_brightness: float) -> str:
        """
        Detect if the breast is left or right side
        Improved algorithm based on VinDr-Mammo dataset analysis
        """
        try:
            height, width = image.shape
            
            # Analyze nipple position (typically more towards one side)
            # For left breast: nipple tends to be more on the right side of the image
            # For right breast: nipple tends to be more on the left side of the image
            
            # Find the brightest region (often corresponds to nipple area)
            blurred = cv2.GaussianBlur(image, (15, 15), 0)
            max_val = np.max(blurred)
            bright_threshold = max_val * 0.8
            
            # Find bright regions
            bright_regions = np.where(blurred > bright_threshold)
            
            if len(bright_regions[1]) > 0:  # If bright regions found
                avg_x = np.mean(bright_regions[1])
                center_x = width // 2
                
                # More precise threshold based on VinDr-Mammo analysis
                if avg_x > center_x * 1.15:  # More towards right side
                    return "LEFT"  # Left breast (nipple on right side of image)
                elif avg_x < center_x * 0.85:  # More towards left side
                    return "RIGHT"  # Right breast (nipple on left side of image)
            
            # Fallback: use brightness distribution with improved thresholds
            brightness_diff = abs(left_brightness - right_brightness)
            brightness_ratio = left_brightness / right_brightness if right_brightness > 0 else 1
            
            if brightness_diff > 5:  # Significant brightness difference
                if brightness_ratio > 1.1:  # Left side brighter
                    return "RIGHT"  # More tissue on left side = right breast
                elif brightness_ratio < 0.9:  # Right side brighter
                    return "LEFT"   # More tissue on right side = left breast
            
            # Additional analysis: check tissue distribution patterns
            # Analyze the central region for tissue density patterns
            center_region = image[height//4:3*height//4, width//4:3*width//4]
            center_brightness = np.mean(center_region)
            
            if center_brightness > np.mean(image) * 1.05:  # Denser center
                # Check which side has more tissue
                if left_brightness > right_brightness * 1.05:
                    return "RIGHT"
                else:
                    return "LEFT"
            
            # Default fallback based on brightness
            if left_brightness > right_brightness:
                return "RIGHT"  # More tissue on left side = right breast
            else:
                return "LEFT"   # More tissue on right side = left breast
                         
        except Exception as e:
            print(f"Erreur lors de la détection du côté: {e}")
            return "LEFT"  # Default fallback
    
    def _detect_view_type(self, aspect_ratio: float, horizontal_symmetry: float, 
                         vertical_symmetry: float, edge_density: float) -> str:
        """
        Detect view type (CC vs MLO) based on image characteristics
        Robust algorithm with adaptive thresholds and confidence scoring
        """
        try:
            print(f"🔍 Analyse des caractéristiques: aspect_ratio={aspect_ratio:.2f}, h_sym={horizontal_symmetry:.2f}, v_sym={vertical_symmetry:.2f}, edges={edge_density:.3f}")
            
            # Robust algorithm with adaptive thresholds
            # CC views: more symmetric horizontally, more square aspect ratio
            # MLO views: less symmetric, more elongated, more diagonal content
            
            cc_score = 0
            mlo_score = 0
            confidence_factors = []
            
            # 1. Aspect ratio analysis with adaptive thresholds
            aspect_ratio_score = self._analyze_aspect_ratio(aspect_ratio)
            cc_score += aspect_ratio_score['cc']
            mlo_score += aspect_ratio_score['mlo']
            confidence_factors.append(aspect_ratio_score['confidence'])
            
            # 2. Symmetry analysis with relative thresholds
            symmetry_score = self._analyze_symmetry(horizontal_symmetry, vertical_symmetry)
            cc_score += symmetry_score['cc']
            mlo_score += symmetry_score['mlo']
            confidence_factors.append(symmetry_score['confidence'])
            
            # 3. Edge density analysis with adaptive thresholds
            edge_score = self._analyze_edge_density(edge_density)
            cc_score += edge_score['cc']
            mlo_score += edge_score['mlo']
            confidence_factors.append(edge_score['confidence'])
            
            # Calculate overall confidence
            overall_confidence = np.mean(confidence_factors)
            
            print(f"📊 Scores: CC={cc_score}, MLO={mlo_score}, Confidence={overall_confidence:.2f}")
            
            # Decision with stricter confidence thresholds
            score_diff = abs(cc_score - mlo_score)
            
            print(f"    🎯 Decision logic: score_diff={score_diff}, confidence={overall_confidence:.2f}")
            
            if overall_confidence > 0.8 and score_diff > 3:  # Very high confidence decision
                if mlo_score > cc_score:
                    print(f"    ✅ Very high confidence -> MLO")
                    return "MLO"
                else:
                    print(f"    ✅ Very high confidence -> CC")
                    return "CC"
            elif overall_confidence > 0.6 and score_diff > 2:  # High confidence decision
                if mlo_score > cc_score:
                    print(f"    ✅ High confidence -> MLO")
                    return "MLO"
                else:
                    print(f"    ✅ High confidence -> CC")
                    return "CC"
            elif overall_confidence > 0.4 and score_diff > 1:  # Medium confidence decision
                if mlo_score > cc_score:
                    print(f"    ✅ Medium confidence -> MLO")
                    return "MLO"
                else:
                    print(f"    ✅ Medium confidence -> CC")
                    return "CC"
            else:  # Low confidence - use conservative fallback
                print("    ⚠️ Faible confiance, utilisation de l'aspect ratio comme critère principal")
                if aspect_ratio > 1.3 or aspect_ratio < 0.7:  # Very elongated/square
                    print(f"    🔄 Fallback: aspect_ratio={aspect_ratio:.2f} -> MLO")
                    return "MLO"
                else:
                    print(f"    🔄 Fallback: aspect_ratio={aspect_ratio:.2f} -> CC")
                    return "CC"
                    
        except Exception as e:
            print(f"Erreur lors de la détection du type de vue: {e}")
            return "CC"  # Default fallback
    
    def _analyze_aspect_ratio(self, aspect_ratio: float) -> dict:
        """Analyze aspect ratio with stricter thresholds"""
        try:
            print(f"    📐 Aspect ratio analysis: {aspect_ratio:.3f}")
            
            # Stricter thresholds - CC views are typically more square
            if 0.9 <= aspect_ratio <= 1.1:  # Very square (strong CC indicator)
                print(f"    ✅ Very square -> CC +3")
                return {'cc': 3, 'mlo': 0, 'confidence': 0.9}
            elif 0.8 <= aspect_ratio <= 1.2:  # Moderately square
                print(f"    ✅ Moderately square -> CC +2")
                return {'cc': 2, 'mlo': 0, 'confidence': 0.7}
            elif 0.7 <= aspect_ratio <= 1.3:  # Neutral range
                print(f"    ⚖️ Neutral range -> CC +1, MLO +1")
                return {'cc': 1, 'mlo': 1, 'confidence': 0.4}
            elif aspect_ratio > 1.4 or aspect_ratio < 0.6:  # Very elongated/square (strong MLO)
                print(f"    ✅ Very elongated -> MLO +3")
                return {'cc': 0, 'mlo': 3, 'confidence': 0.8}
            else:  # Moderately elongated/square
                print(f"    ✅ Moderately elongated -> MLO +2")
                return {'cc': 0, 'mlo': 2, 'confidence': 0.6}
        except:
            return {'cc': 1, 'mlo': 1, 'confidence': 0.3}
    
    def _analyze_symmetry(self, horizontal_symmetry: float, vertical_symmetry: float) -> dict:
        """Analyze symmetry with stricter thresholds"""
        try:
            print(f"    🔄 Symmetry analysis: h_sym={horizontal_symmetry:.3f}, v_sym={vertical_symmetry:.3f}")
            
            if vertical_symmetry == 0:
                return {'cc': 1, 'mlo': 1, 'confidence': 0.3}
            
            symmetry_ratio = horizontal_symmetry / vertical_symmetry
            print(f"    📊 Symmetry ratio: {symmetry_ratio:.3f}")
            
            # Stricter thresholds - CC views are more horizontally symmetric
            if symmetry_ratio < 0.4:  # Much more horizontally symmetric (strong CC)
                print(f"    ✅ Much more horizontally symmetric -> CC +3")
                return {'cc': 3, 'mlo': 0, 'confidence': 0.8}
            elif symmetry_ratio < 0.6:  # Moderately horizontally symmetric
                print(f"    ✅ Moderately horizontally symmetric -> CC +2")
                return {'cc': 2, 'mlo': 0, 'confidence': 0.6}
            elif symmetry_ratio < 0.8:  # Slightly horizontally symmetric
                print(f"    ✅ Slightly horizontally symmetric -> CC +1")
                return {'cc': 1, 'mlo': 0, 'confidence': 0.4}
            elif symmetry_ratio > 2.0:  # Much less horizontally symmetric (strong MLO)
                print(f"    ✅ Much less horizontally symmetric -> MLO +3")
                return {'cc': 0, 'mlo': 3, 'confidence': 0.8}
            elif symmetry_ratio > 1.5:  # Less horizontally symmetric
                print(f"    ✅ Less horizontally symmetric -> MLO +2")
                return {'cc': 0, 'mlo': 2, 'confidence': 0.7}
            else:  # Neutral
                print(f"    ⚖️ Neutral symmetry -> CC +1, MLO +1")
                return {'cc': 1, 'mlo': 1, 'confidence': 0.3}
        except:
            return {'cc': 1, 'mlo': 1, 'confidence': 0.3}
    
    def _analyze_edge_density(self, edge_density: float) -> dict:
        """Analyze edge density with stricter thresholds"""
        try:
            print(f"    📈 Edge density analysis: {edge_density:.4f}")
            
            # Stricter thresholds - MLO views have more complex diagonal structures
            if edge_density > 0.20:  # Very high edge density (strong MLO)
                print(f"    ✅ Very high edge density -> MLO +3")
                return {'cc': 0, 'mlo': 3, 'confidence': 0.8}
            elif edge_density > 0.15:  # High edge density
                print(f"    ✅ High edge density -> MLO +2")
                return {'cc': 0, 'mlo': 2, 'confidence': 0.6}
            elif edge_density > 0.10:  # Medium-high edge density
                print(f"    ✅ Medium-high edge density -> MLO +1")
                return {'cc': 0, 'mlo': 1, 'confidence': 0.4}
            elif edge_density > 0.06:  # Medium edge density (neutral)
                print(f"    ⚖️ Medium edge density -> CC +1, MLO +1")
                return {'cc': 1, 'mlo': 1, 'confidence': 0.4}
            elif edge_density > 0.03:  # Low edge density (CC)
                print(f"    ✅ Low edge density -> CC +2")
                return {'cc': 2, 'mlo': 0, 'confidence': 0.6}
            else:  # Very low edge density
                print(f"    ✅ Very low edge density -> CC +3")
                return {'cc': 3, 'mlo': 0, 'confidence': 0.7}
        except:
            return {'cc': 1, 'mlo': 1, 'confidence': 0.3}
    
    async def _run_ml_analysis(self, file_paths: List[str]) -> dict:
        """
        Run ML analysis using the real MedSigLIP model
        PAS DE MODE DÉMO - Le modèle doit être chargé
        """
        try:
            print(f"🤖 Démarrage de l'analyse MedSigLIP pour {len(file_paths)} images")
            
            # VÉRIFICATION CRITIQUE: Le modèle doit être chargé, sinon erreur
            if not self.ml_model:
                raise ValueError("Le modèle ML n'est pas initialisé. Redémarrez le backend.")
            
            if not self.ml_model.checkpoint:
                raise ValueError("Le checkpoint du modèle (best_medsiglip_model.pth) n'est pas chargé. Vérifiez que le fichier existe dans app/ml/model/")
            
            if not self.ml_model.use_direct_classifiers or self.ml_model.bi_rads_classifier is None:
                raise ValueError("Vos classificateurs entraînés ne sont pas chargés. Vérifiez que best_medsiglip_model.pth contient bien les classificateurs (bi_rads_classifier, density_classifier).")
            
            # Votre modèle best est disponible et chargé
            print("✅✅✅ VOTRE MODÈLE BEST EST CHARGÉ ET PRÊT")
            print("✅✅✅ UTILISATION DE VOTRE MODÈLE BEST (classificateurs directs)")
            if self.ml_model.full_model is not None:
                print("   ✅ Modèle de base MedSigLIP chargé - embeddings réels seront utilisés")
            else:
                print("   ⚠️ Modèle de base non chargé - extracteur de features local sera utilisé")
            
            # Compteur global pour les images rejetées
            rejected_images = 0
            total_images = len(file_paths)
            
            # PRIORITÉ 1: Utiliser directement vos classificateurs entraînés (VOTRE MODÈLE BEST)
            if self.ml_model and self.ml_model.use_direct_classifiers and self.ml_model.bi_rads_classifier is not None:
                print("🎯🎯🎯 MODE ACTIF: Classificateurs directs (VOTRE MODÈLE BEST)")
                print("   ✅ Vos classificateurs BI-RADS et Densité seront utilisés")
                
                # Analyser chaque image avec vos classificateurs séquentiellement
                # NOTE: Traitement séquentiel car PyTorch n'est pas thread-safe
                # Le modèle ML ne peut pas être utilisé en parallèle sans risques de conflits
                all_predictions = []
                detected_regions = []
                
                for i, image_path in enumerate(file_paths):
                    print(f"🔍 Analyse de l'image {i+1}/{len(file_paths)} avec VOTRE modèle: {os.path.basename(image_path)}")
                    
                    try:
                        # Charger l'image et utiliser _predict_with_model directement
                        image_array = self.ml_model._load_and_preprocess_image(image_path)
                        if image_array is None:
                            # ARRÊTER IMMÉDIATEMENT si une image est invalide
                            print(f"\n   🚨🚨🚨 ARRÊT IMMÉDIAT DE L'ANALYSE")
                            print(f"   ❌ Image {i+1}/{total_images} rejetée - ne semble pas être une mammographie valide")
                            print(f"   🚨 L'analyse est annulée pour éviter des résultats incorrects")
                            raise ValueError(
                                f"Analyse annulée: L'image {i+1} (sur {total_images}) a été rejetée car elle ne semble pas être une mammographie valide. "
                                f"Toutes les images doivent être des mammographies valides pour effectuer l'analyse. "
                                f"Veuillez uploader uniquement des images de mammographie."
                            )
                        
                        bi_rads_pred, bi_rads_conf, density_pred, density_conf = self.ml_model._predict_with_model(image_array)
                        
                        # Chercher les zones d'intérêt si disponible
                        image_id = self.ml_model._extract_image_id_from_path(image_path)
                        regions = self.ml_model._get_regions_from_annotations(image_id, image_path)
                        
                        # Formater comme attendu
                        all_predictions.append({
                            'bi_rads': {
                                'prediction': bi_rads_pred,
                                'confidence': bi_rads_conf
                            },
                            'density': {
                                'prediction': density_pred,
                                'confidence': density_conf
                            },
                            'view': {
                                'prediction': 'CC_L',  # Par défaut, peut être amélioré
                                'confidence': 0.8
                            },
                            'detected_regions': regions
                        })
                        print(f"   ✅ Image {i+1}/{len(file_paths)} analysée avec succès")
                    except ValueError:
                        # Relancer les ValueError (erreurs de validation d'images)
                        raise
                    except Exception as e:
                        print(f"   ⚠️ Erreur lors du traitement de l'image {i+1}: {e}")
                        # Continuer avec les autres images si une seule échoue
            
            # Note: Le mode 2 (modèle standard) ne devrait jamais être atteint si votre modèle est correctement chargé
            # car nous avons vérifié que use_direct_classifiers est True
            else:
                # Ce cas ne devrait jamais se produire si votre modèle est chargé
                raise ValueError(
                    "Le modèle n'est pas dans un état valide pour l'analyse. "
                    f"État: use_direct_classifiers={self.ml_model.use_direct_classifiers}, "
                    f"bi_rads_classifier={'OK' if self.ml_model.bi_rads_classifier else 'MANQUANT'}, "
                    f"checkpoint={'OK' if self.ml_model.checkpoint else 'MANQUANT'}. "
                    "Veuillez redémarrer le backend pour recharger le modèle."
                )
            
            # Agrégation des prédictions (pour les deux modes)
            bi_rads_scores = []
            density_scores = []
            confidences = []
            
            for pred in all_predictions:
                if pred and 'bi_rads' in pred and 'prediction' in pred['bi_rads']:
                    bi_rads_scores.append(pred['bi_rads']['prediction'])
                    confidences.append(pred['bi_rads'].get('confidence', 0.5))
                
                if pred and 'density' in pred and 'prediction' in pred['density']:
                    density_scores.append(pred['density']['prediction'])
            
            # Use the most severe BI-RADS prediction
            if bi_rads_scores:
                bi_rads_pred = max(bi_rads_scores, key=lambda x: int(x.split()[-1]))
                bi_rads_confidence = max(confidences) if confidences else 0.8
                print(f"📊 Résultats de votre modèle: {bi_rads_pred} (confiance: {bi_rads_confidence:.2f})")
            else:
                bi_rads_pred = 'BI-RADS 2'
                bi_rads_confidence = 0.5
                print("⚠️ Aucune prédiction BI-RADS obtenue")
            
            # Use the most common density prediction
            if density_scores:
                from collections import Counter
                density_pred = Counter(density_scores).most_common(1)[0][0]
            else:
                density_pred = 'DENSITY B'
            
            # Vérifier si des images ont été rejetées
            if rejected_images > 0:
                accepted_images = total_images - rejected_images
                print(f"\n   ⚠️ ATTENTION: {rejected_images}/{total_images} images ont été rejetées")
                print(f"   ✅ {accepted_images} image(s) valide(s) analysée(s)")
                if rejected_images / total_images > 0.3:  # Plus de 30% rejetées
                    print(f"   ⚠️ Beaucoup d'images rejetées - les résultats peuvent être moins fiables")
            
            print(f"📊 Résultats finaux: {bi_rads_pred} (confiance: {bi_rads_confidence:.2%}), Densité: {density_pred}")
            
            # Si aucune prédiction n'a été obtenue, vérifier la raison
            if not all_predictions:
                print("⚠️⚠️⚠️ AUCUNE PRÉDICTION OBTENUE!")
                print("   Raisons possibles:")
                print("   1. Les images uploadées ne sont pas des mammographies valides")
                print("   2. Les images ont été rejetées par la validation")
                print("   3. Le modèle n'est pas disponible")
                
                # Ne pas utiliser le mode démo - retourner une erreur explicite
                raise ValueError(
                    "Impossible d'analyser les images. "
                    "Assurez-vous que les images uploadées sont des mammographies valides. "
                    "Les images non-mammographiques sont automatiquement rejetées pour garantir la précision des résultats."
                )
            
            # Convert BI-RADS to enum
            bi_rads_mapping = {
                'BI-RADS 1': BI_RADS_Category.CATEGORY_1,
                'BI-RADS 2': BI_RADS_Category.CATEGORY_2,
                'BI-RADS 3': BI_RADS_Category.CATEGORY_3,
                'BI-RADS 4': BI_RADS_Category.CATEGORY_4,
                'BI-RADS 5': BI_RADS_Category.CATEGORY_5
            }
            
            bi_rads_category = bi_rads_mapping.get(bi_rads_pred, BI_RADS_Category.CATEGORY_2)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(bi_rads_pred, bi_rads_confidence)
            
            # Generate findings
            findings = self._generate_findings(bi_rads_pred, density_pred, bi_rads_confidence)
            
            # Déterminer la version du modèle utilisée (votre modèle best est TOUJOURS utilisé)
            if not self.ml_model.use_direct_classifiers or self.ml_model.bi_rads_classifier is None:
                raise ValueError("Vos classificateurs ne sont pas disponibles - le modèle doit être rechargé")
            
            model_version = "MedSigLIP-Best-v1.0 (Votre modèle entraîné)"
            if self.ml_model.full_model is not None:
                model_version += " - avec embeddings MedSigLIP réels"
            else:
                model_version += " - avec extracteur de features local"
            
            print(f"📊 Version du modèle utilisée: {model_version}")
            
            return {
                "bi_rads_category": bi_rads_category,
                "confidence_score": bi_rads_confidence,
                "breast_density": density_pred.replace('DENSITY ', ''),
                "findings": findings,
                "recommendations": recommendations,
                "model_version": model_version,
                "detected_regions": detected_regions if 'detected_regions' in locals() else []
            }
            
        except ValueError as e:
            # Les erreurs ValueError (modèle non chargé, images invalides) doivent être propagées
            print(f"🚨 Erreur de validation: {e}")
            raise e
        except Exception as e:
            # Pour les autres erreurs techniques, lever une exception plutôt que de retourner un résultat en mode démo
            print(f"❌ Erreur technique lors de l'analyse ML: {e}")
            import traceback
            traceback.print_exc()
            
            # Ne PAS retourner de résultat en mode démo - lever une exception
            raise HTTPException(
                status_code=500,
                detail=f"Erreur technique lors de l'analyse: {str(e)}. Le modèle MedSigLIP n'a pas pu analyser les images. Veuillez réessayer ou contacter le support."
            )
    
    def _generate_recommendations(self, bi_rads_pred: str, confidence: float) -> str:
        """
        Generate recommendations based on BI-RADS category
        Conforme aux recommandations ACR (American College of Radiology) BI-RADS
        """
        recommendations_map = {
            'BI-RADS 0': "Examen incomplet. Images supplémentaires requises pour évaluation complète.",
            'BI-RADS 1': "Examen normal. Aucune anomalie détectée. Dépistage de routine recommandé dans 12 mois.",
            'BI-RADS 2': "Examen bénin. Lésions bénignes identifiées (kystes simples, calcifications bénignes). Dépistage de routine recommandé dans 12 mois.",
            'BI-RADS 3': "Probablement bénin (< 2% de probabilité de malignité). Suivi à court terme recommandé dans 6 mois pour évaluation de stabilité.",
            'BI-RADS 4': "Suspicion de malignité. Biopsie recommandée pour évaluation histologique. Le résultat nécessite une corrélation clinique.",
            'BI-RADS 5': "Très suspect de malignité (≥ 95% de probabilité). Biopsie fortement recommandée en urgence. Prise en charge oncologique à considérer.",
            'BI-RADS 6': "Cancer confirmé par biopsie. Prise en charge oncologique requise."
        }
        
        base_recommendation = recommendations_map.get(bi_rads_pred, "Consultation radiologique recommandée pour évaluation complète.")
        
        # Ajouter un avertissement si la confiance du modèle est limitée
        if confidence < 0.7:
            base_recommendation += " Note: Confiance du modèle limitée - Validation par un radiologue expérimenté fortement recommandée."
        elif confidence < 0.85:
            base_recommendation += " Note: Confiance modérée - Revue par un radiologue recommandée."
        
        return base_recommendation
    
    def _generate_findings(self, bi_rads_pred: str, density_pred: str, confidence: float) -> str:
        """
        Generate findings based on analysis results
        Conforme aux standards BI-RADS (ACR)
        """
        findings_map = {
            'BI-RADS 0': "Examen incomplet. Évaluation limitée par absence d'images supplémentaires.",
            'BI-RADS 1': "Aucune anomalie détectée. Tissu mammaire normal. Symétrie bilatérale normale.",
            'BI-RADS 2': "Lésions bénignes identifiées (kystes simples, calcifications bénignes, ganglions intramammaires).",
            'BI-RADS 3': "Lésion probablement bénigne détectée. Probabilité de malignité < 2%. Stabilité à documenter par suivi.",
            'BI-RADS 4': "Lésion suspecte détectée. Probabilité de malignité 2-95%. Subdivision recommandée (4a: faible suspicion, 4b: suspicion modérée, 4c: suspicion élevée).",
            'BI-RADS 5': "Lésion très suspecte de malignité. Probabilité de malignité ≥ 95%. Caractéristiques typiques du cancer du sein présentes.",
            'BI-RADS 6': "Cancer confirmé histologiquement par biopsie."
        }
        
        base_finding = findings_map.get(bi_rads_pred, "Analyse en cours.")
        
        # Ajouter la densité mammaire selon la classification ACR
        density_letter = density_pred.replace('DENSITY ', '')
        density_descriptions = {
            'A': 'Presque entièrement graisseux',
            'B': 'Zones dispersées de densité fibroglandulaire',
            'C': 'Densité hétérogène (peut masquer les petites masses)',
            'D': 'Extrêmement dense (peut masquer les masses)'
        }
        density_full = density_descriptions.get(density_letter, density_letter)
        density_info = f" Densité mammaire: {density_letter} ({density_full})."
        
        # Informations de confiance du modèle
        confidence_info = f" Niveau de confiance du modèle d'IA: {confidence:.1%}."
        
        return base_finding + density_info + confidence_info
    
    def get_analysis_result(self, analysis_id: str):
        """Get analysis result by analysis_id (UUID)"""
        try:
            # Try to find by analysis_id first (the UUID)
            analysis = self.db.query(MammographyAnalysis).filter(
                MammographyAnalysis.analysis_id == analysis_id
            ).first()

            # If not found, try by id (primary key) for backward compatibility
            if not analysis:
                analysis = self.db.query(MammographyAnalysis).filter(
                    MammographyAnalysis.id == analysis_id
                ).first()

            if not analysis:
                return None

            # Récupérer le patient_id lisible depuis la table patients
            # analysis.patient_id contient l'UUID (id), pas le patient_id lisible
            patient_readable_id = None
            if analysis.patient_id:
                patient = self.db.query(Patient).filter(Patient.id == analysis.patient_id).first()
                if patient:
                    patient_readable_id = patient.patient_id  # Le patient_id lisible (P-2025-1)

            # Si pas trouvé, utiliser l'UUID comme fallback
            if not patient_readable_id:
                patient_readable_id = analysis.patient_id

            return {
                "id": analysis.id,
                "analysis_id": analysis.analysis_id,
                "patient_id": patient_readable_id,  # Utiliser le patient_id lisible
                "user_id": str(analysis.user_id) if analysis.user_id else None,
                "bi_rads_category": str(analysis.bi_rads_category.value) if analysis.bi_rads_category else "CATEGORY_2",
                "confidence_score": analysis.confidence_score or 0.0,
                "breast_density": analysis.breast_density or "Unknown",
                "model_version": analysis.model_version or "Unknown",
                "processing_time": analysis.processing_time or 0.0,
                "status": analysis.status.value if analysis.status else "pending",
                "findings": analysis.findings or "No findings available",
                "recommendations": analysis.recommendations or "No recommendations available",
                "notes": analysis.notes or "No notes available",
                "original_files": analysis.original_files if analysis.original_files else [],
                "processed_images": analysis.processed_images if analysis.processed_images else [],
                "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
                "updated_at": analysis.updated_at.isoformat() if analysis.updated_at else None
            }
        except Exception as e:
            print(f"Erreur lors de la récupération de l'analyse: {e}")
            return None
    
    def get_patient_history(self, patient_id: str):
        """Get analysis history for a patient"""
        try:
            analyses = self.db.query(MammographyAnalysis).filter(
                MammographyAnalysis.patient_id == patient_id
            ).order_by(MammographyAnalysis.created_at.desc()).all()
            
            return [
                {
                    "id": analysis.id,
                    "analysis_id": analysis.analysis_id,
                    "bi_rads_category": analysis.bi_rads_category,
                    "confidence_score": analysis.confidence_score,
                    "status": analysis.status,
                    "created_at": analysis.created_at.isoformat() if analysis.created_at else None
                }
                for analysis in analyses
            ]
        except Exception as e:
            print(f"Erreur lors de la récupération de l'historique: {e}")
            return []

    def validate_analysis(self, analysis_id: str) -> bool:
        """
        Validate an analysis by updating its status to VALIDATED
        """
        try:
            # Try to find by analysis_id first (the UUID)
            analysis = self.db.query(MammographyAnalysis).filter(
                MammographyAnalysis.analysis_id == analysis_id
            ).first()

            # If not found, try by id (primary key) for backward compatibility
            if not analysis:
                analysis = self.db.query(MammographyAnalysis).filter(
                    MammographyAnalysis.id == analysis_id
                ).first()

            if not analysis:
                print(f"❌ Analyse non trouvée: {analysis_id}")
                return False

            # Update status to VALIDATED
            analysis.status = AnalysisStatus.VALIDATED
            self.db.commit()
            self.db.refresh(analysis)

            print(f"✅ Analyse validée: {analysis_id}")
            return True

        except Exception as e:
            print(f"❌ Erreur lors de la validation de l'analyse: {e}")
            self.db.rollback()
            return False