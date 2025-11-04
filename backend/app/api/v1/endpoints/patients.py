"""
Patient management endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from app.services.patient_service import PatientService

router = APIRouter()


@router.post("/", response_model=PatientResponse)
async def create_patient(
    patient_in: PatientCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new patient
    """
    patient_service = PatientService(db)
    patient = patient_service.create_patient(patient_in)
    return patient


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):
    """
    Get patient by ID (UUID or patient_id readable format like P-2025-1)
    """
    print(f"🔍 GET /api/v1/patients/{patient_id} appelé")
    patient_service = PatientService(db)
    
    # Try to find by UUID first
    patient = patient_service.get_patient(patient_id)
    print(f"📋 Recherche par UUID: {patient is not None}")
    
    # If not found, try to find by patient_id (readable format)
    if not patient:
        patient = patient_service.get_patient_by_patient_id(patient_id)
        print(f"📋 Recherche par patient_id lisible: {patient is not None}")

    if not patient:
        print(f"❌ Patient non trouvé: {patient_id}")
        raise HTTPException(status_code=404, detail="Patient not found")

    print(f"✅ Patient trouvé: {patient.patient_id}, {patient.full_name}, {patient.age} ans")
    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: str,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db)
):
    """
    Update patient information
    """
    patient_service = PatientService(db)
    patient = patient_service.update_patient(patient_id, patient_update)
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient


@router.get("/", response_model=List[PatientResponse])
async def list_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all patients with pagination
    """
    patient_service = PatientService(db)
    patients = patient_service.list_patients(skip=skip, limit=limit)
    return patients
