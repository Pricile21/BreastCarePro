"""
Patient schemas
"""

from typing import Optional
from datetime import date
from pydantic import BaseModel


class PatientBase(BaseModel):
    """
    Base patient schema
    """
    full_name: str
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: Optional[str] = None
    family_history: Optional[str] = None
    notes: Optional[str] = None


class PatientCreate(PatientBase):
    """
    Patient creation schema
    """
    patient_id: Optional[str] = None
    age: Optional[int] = None


class PatientUpdate(PatientBase):
    """
    Patient update schema
    """
    full_name: Optional[str] = None


class PatientResponse(PatientBase):
    """
    Patient response schema
    """
    id: str
    patient_id: str
    user_id: str
    age: Optional[int] = None
    
    class Config:
        from_attributes = True
