"""
Healthcare professional schemas
"""

from typing import Optional
from pydantic import BaseModel


class ProfessionalBase(BaseModel):
    """
    Base professional schema
    """
    full_name: str
    specialty: str
    license_number: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    consultation_fee: Optional[float] = None
    languages: Optional[list[str]] = None


class ProfessionalCreate(ProfessionalBase):
    """
    Professional creation schema
    """
    pass


class ProfessionalUpdate(ProfessionalBase):
    """
    Professional update schema
    """
    full_name: Optional[str] = None
    specialty: Optional[str] = None
    license_number: Optional[str] = None


class ProfessionalResponse(ProfessionalBase):
    """
    Professional response schema
    """
    id: str
    
    class Config:
        from_attributes = True
