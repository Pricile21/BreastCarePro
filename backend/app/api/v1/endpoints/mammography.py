"""
Mammography analysis endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.mammography import MammographyAnalysisResponse, MammographyUploadRequest
from app.services.mammography_service_simple import MammographyService

router = APIRouter()


@router.post("/analyze", response_model=MammographyAnalysisResponse)
async def analyze_mammography(
    files: List[UploadFile] = File(...),
    patient_id: Optional[str] = Form(None),
    patient_name: Optional[str] = Form(None),
    patient_age: Optional[str] = Form(None),
    patient_notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze mammography images and return BI-RADS classification
    """
    print(f"🔍 Analyse demandée - Patient ID: {patient_id}, Fichiers: {len(files)}")
    print(f"   Informations patient: name={patient_name}, age={patient_age}")
    
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # Validate file types
    for file in files:
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail=f"File {file.filename} is not an image"
            )
    
    try:
        # Créer ou mettre à jour le patient si les informations sont fournies
        from app.models.patient import Patient
        from app.services.patient_service import PatientService
        
        if patient_id and (patient_name or patient_age):
            patient_service = PatientService(db)
            
            # Vérifier si le patient existe déjà
            existing_patient = patient_service.get_patient_by_patient_id(patient_id)
            
            if existing_patient:
                # Mettre à jour le patient existant
                print(f"🔄 Mise à jour du patient existant: {patient_id}")
                if patient_name:
                    existing_patient.full_name = patient_name
                if patient_age:
                    existing_patient.age = int(patient_age) if patient_age.isdigit() else None
                if patient_notes:
                    existing_patient.notes = patient_notes
                db.commit()
            else:
                # Créer un nouveau patient
                print(f"➕ Création d'un nouveau patient: {patient_id}")
                from app.schemas.patient import PatientCreate
                
                patient_data = PatientCreate(
                    patient_id=patient_id,
                    full_name=patient_name or f"Patient {patient_id}",
                    age=int(patient_age) if patient_age and patient_age.isdigit() else None,
                    notes=patient_notes
                )
                patient_service.create_patient(patient_data, user_id=current_user.id)
                print(f"✅ Patient créé: {patient_id}")
        
        mammography_service = MammographyService(db)
        result = await mammography_service.analyze_mammography(files, patient_id, current_user.id)
        return result
    except HTTPException as e:
        # HTTPException est déjà correctement formatée, la relancer telle quelle
        raise e
    except Exception as e:
        # Pour les autres exceptions, retourner une erreur 500
        print(f"❌ Erreur inattendue lors de l'analyse: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/image/{file_path:path}")
async def get_image(file_path: str):
    """
    Serve uploaded images
    """
    try:
        # Sécuriser le chemin pour éviter les accès non autorisés
        if ".." in file_path or file_path.startswith("/"):
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        full_path = os.path.join(os.getcwd(), file_path)
        
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="Image not found")
        
        return FileResponse(full_path, media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving image: {str(e)}")


@router.get("/analysis/{analysis_id}")
async def get_analysis_result(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analysis result by ID
    """
    try:
        print(f"🔍 Recherche de l'analyse: {analysis_id}")
        mammography_service = MammographyService(db)
        result = mammography_service.get_analysis_result(analysis_id)
        
        if not result:
            print(f"❌ Analyse non trouvée: {analysis_id}")
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        print(f"✅ Analyse trouvée: {result.get('id', 'N/A')}")
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error retrieving analysis: {str(e)}")


@router.get("/history/{patient_id}")
async def get_patient_analysis_history(
    patient_id: str,
    db: Session = Depends(get_db)
):
    """
    Get analysis history for a patient
    """
    mammography_service = MammographyService(db)
    history = mammography_service.get_patient_history(patient_id)
    return {"patient_id": patient_id, "analyses": history}


@router.post("/analysis/{analysis_id}/validate")
async def validate_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Validate an analysis by updating its status to VALIDATED
    """
    try:
        print(f"🔍 Validation de l'analyse: {analysis_id}")
        mammography_service = MammographyService(db)
        
        # Check if analysis exists
        analysis_result = mammography_service.get_analysis_result(analysis_id)
        if not analysis_result:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        # Validate the analysis
        success = mammography_service.validate_analysis(analysis_id)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to validate analysis")
        
        # Return updated analysis
        updated_analysis = mammography_service.get_analysis_result(analysis_id)
        return {
            "message": "Analysis validated successfully",
            "analysis": updated_analysis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la validation: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error validating analysis: {str(e)}")