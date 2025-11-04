"""
Mammography analysis service
"""

import uuid
import time
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.models.mammography import MammographyAnalysis, BI_RADS_Category, AnalysisStatus
from app.schemas.mammography import MammographyAnalysisResponse
from app.ml.inference_service_simple import MedSigLIPInferenceService


class MammographyService:
    """
    Service for mammography analysis operations
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.ml_model = MedSigLIPInferenceService()
    
    async def analyze_mammography(
        self, 
        files: List[UploadFile], 
        patient_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> MammographyAnalysisResponse:
        """
        Analyze mammography images and return BI-RADS classification
        """
        analysis_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Save uploaded files
            file_paths = await self._save_uploaded_files(files, analysis_id)
            
            # Run ML analysis
            analysis_result = await self._run_ml_analysis(file_paths)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create analysis record
            analysis = MammographyAnalysis(
                id=str(uuid.uuid4()),
                analysis_id=analysis_id,
                patient_id=patient_id,
                user_id=user_id or "system",  # Use provided user_id or default to system
                bi_rads_category=analysis_result["bi_rads_category"],
                confidence_score=analysis_result["confidence_score"],
                breast_density=analysis_result.get("breast_density"),
                findings=analysis_result.get("findings"),
                recommendations=analysis_result.get("recommendations"),
                processing_time=processing_time,
                status=AnalysisStatus.COMPLETED,
                original_files=file_paths,
                model_version="1.0.0"
            )
            
            self.db.add(analysis)
            self.db.commit()
            self.db.refresh(analysis)
            
            return MammographyAnalysisResponse.from_orm(analysis)
            
        except Exception as e:
            # Create failed analysis record
            analysis = MammographyAnalysis(
                id=str(uuid.uuid4()),
                analysis_id=analysis_id,
                patient_id=patient_id,
                user_id=user_id or "system",
                status=AnalysisStatus.FAILED,
                processing_time=time.time() - start_time,
                notes=f"Analysis failed: {str(e)}"
            )
            
            self.db.add(analysis)
            self.db.commit()
            
            raise e
    
    async def _save_uploaded_files(
        self, 
        files: List[UploadFile], 
        analysis_id: str
    ) -> List[str]:
        """
        Save uploaded files to disk and return file paths
        """
        file_paths = []
        
        for file in files:
            # Create unique filename
            file_extension = file.filename.split('.')[-1]
            filename = f"{analysis_id}_{file.filename}"
            file_path = f"uploads/{filename}"
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            file_paths.append(file_path)
        
        return file_paths
    
    async def _run_ml_analysis(self, file_paths: List[str]) -> dict:
        """
        Run ML analysis on the mammography images using MedSigLIP
        """
        try:
            # Utiliser le modèle MedSigLIP pour prédire
            results = self.ml_model.predict_batch(file_paths)
            
            if not results:
                raise Exception("Aucune prédiction obtenue")
            
            # Prendre la première image comme référence
            first_result = results[0]
            
            if 'error' in first_result:
                raise Exception(f"Erreur de prédiction: {first_result['error']}")
            
            # Extraire les prédictions
            bi_rads_pred = first_result['bi_rads']['prediction']
            density_pred = first_result['density']['prediction']
            bi_rads_confidence = first_result['bi_rads']['confidence']
            density_confidence = first_result['density']['confidence']
            
            # Convertir BI-RADS en enum
            bi_rads_mapping = {
                'BI-RADS 1': BI_RADS_Category.CATEGORY_1,
                'BI-RADS 2': BI_RADS_Category.CATEGORY_2,
                'BI-RADS 3': BI_RADS_Category.CATEGORY_3,
                'BI-RADS 4': BI_RADS_Category.CATEGORY_4,
                'BI-RADS 5': BI_RADS_Category.CATEGORY_5
            }
            
            bi_rads_category = bi_rads_mapping.get(bi_rads_pred, BI_RADS_Category.CATEGORY_2)
            
            # Générer des recommandations basées sur BI-RADS
            recommendations = self._generate_recommendations(bi_rads_pred, bi_rads_confidence)
            
            # Générer des findings
            findings = self._generate_findings(bi_rads_pred, density_pred, bi_rads_confidence)
            
            return {
                "bi_rads_category": bi_rads_category,
                "confidence_score": bi_rads_confidence,
                "breast_density": density_pred.replace('DENSITY ', ''),
                "findings": findings,
                "recommendations": recommendations,
                "model_version": "MedSigLIP-448",
                "raw_predictions": {
                    "bi_rads": first_result['bi_rads'],
                    "density": first_result['density']
                }
            }
            
        except Exception as e:
            # En cas d'erreur, retourner des valeurs par défaut
            return {
                "bi_rads_category": BI_RADS_Category.CATEGORY_2,
                "confidence_score": 0.5,
                "breast_density": "B",
                "findings": f"Erreur d'analyse: {str(e)}",
                "recommendations": "Consultation médicale recommandée",
                "model_version": "MedSigLIP-448",
                "error": str(e)
            }
    
    def _generate_recommendations(self, bi_rads_pred: str, confidence: float) -> str:
        """Générer des recommandations basées sur BI-RADS"""
        recommendations = {
            'BI-RADS 1': "Examen normal. Suivi de routine dans 1 an.",
            'BI-RADS 2': "Examen bénin. Suivi de routine dans 1 an.",
            'BI-RADS 3': f"Probablement bénin (confiance: {confidence:.1%}). Suivi à 6 mois recommandé.",
            'BI-RADS 4': f"Suspicion de malignité (confiance: {confidence:.1%}). Biopsie recommandée.",
            'BI-RADS 5': f"Très suspect de malignité (confiance: {confidence:.1%}). Biopsie urgente recommandée."
        }
        return recommendations.get(bi_rads_pred, "Consultation médicale recommandée.")
    
    def _generate_findings(self, bi_rads_pred: str, density_pred: str, confidence: float) -> str:
        """Générer des findings basés sur les prédictions"""
        findings = []
        
        # Findings basés sur BI-RADS
        if bi_rads_pred in ['BI-RADS 1', 'BI-RADS 2']:
            findings.append("Aucune anomalie détectée")
        elif bi_rads_pred == 'BI-RADS 3':
            findings.append("Lésion probablement bénigne détectée")
        elif bi_rads_pred in ['BI-RADS 4', 'BI-RADS 5']:
            findings.append("Lésion suspecte détectée")
        
        # Findings basés sur la densité
        density_level = density_pred.replace('DENSITY ', '')
        findings.append(f"Densité mammaire: {density_level}")
        
        # Confiance
        if confidence < 0.7:
            findings.append("Confiance modérée - consultation médicale recommandée")
        
        return ". ".join(findings) + "."
    
    def get_analysis_result(self, analysis_id: str) -> Optional[MammographyAnalysis]:
        """
        Get analysis result by ID
        """
        return self.db.query(MammographyAnalysis).filter(
            MammographyAnalysis.analysis_id == analysis_id
        ).first()
    
    def get_patient_history(self, patient_id: str) -> List[MammographyAnalysis]:
        """
        Get analysis history for a patient
        """
        return self.db.query(MammographyAnalysis).filter(
            MammographyAnalysis.patient_id == patient_id
        ).order_by(MammographyAnalysis.created_at.desc()).all()
