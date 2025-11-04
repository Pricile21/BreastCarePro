"""
Patient service
"""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    """
    Service for patient operations
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_patient(self, patient_in: PatientCreate, user_id: str = "system") -> Patient:
        """Create new patient"""
        # Utiliser le patient_id fourni ou en générer un nouveau
        patient_id = patient_in.patient_id if patient_in.patient_id else f"P-{str(uuid.uuid4())[:8].upper()}"
        
        patient = Patient(
            id=str(uuid.uuid4()),
            patient_id=patient_id,
            user_id=user_id,
            full_name=patient_in.full_name,
            date_of_birth=patient_in.date_of_birth,
            age=patient_in.age,
            phone_number=patient_in.phone_number,
            address=patient_in.address,
            emergency_contact=patient_in.emergency_contact,
            medical_history=patient_in.medical_history,
            family_history=patient_in.family_history,
            notes=patient_in.notes
        )
        
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Get patient by ID"""
        return self.db.query(Patient).filter(Patient.id == patient_id).first()
    
    def get_patient_by_patient_id(self, patient_id: str) -> Optional[Patient]:
        """Get patient by patient ID"""
        return self.db.query(Patient).filter(Patient.patient_id == patient_id).first()
    
    def update_patient(self, patient_id: str, patient_update: PatientUpdate) -> Optional[Patient]:
        """Update patient information"""
        patient = self.get_patient(patient_id)
        if not patient:
            return None
        
        update_data = patient_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(patient, field, value)
        
        self.db.commit()
        self.db.refresh(patient)
        return patient
    
    def list_patients(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        """List patients with pagination"""
        return self.db.query(Patient).offset(skip).limit(limit).all()
