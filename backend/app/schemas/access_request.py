"""
Pydantic schemas for access requests
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class AccessRequestBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    license_number: str
    specialty: str
    hospital_clinic: str
    experience_years: str
    password: str
    motivation: str
    additional_info: Optional[str] = None


class AccessRequestCreate(AccessRequestBase):
    pass


class AccessRequestUpdate(BaseModel):
    status: str  # approved, rejected
    admin_notes: Optional[str] = None


class AccessRequest(AccessRequestBase):
    id: str
    status: str
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
