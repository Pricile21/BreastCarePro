"""
Appointment schemas
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer


class AppointmentBase(BaseModel):
    """Base appointment schema"""
    center_id: str
    patient_name: str
    patient_phone: str
    patient_email: Optional[str] = None
    appointment_date: str  # ISO format string
    appointment_time: str
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    """Appointment creation schema"""
    pass


class AppointmentUpdate(BaseModel):
    """Appointment update schema"""
    patient_name: Optional[str] = None
    patient_phone: Optional[str] = None
    patient_email: Optional[str] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    """Appointment response schema"""
    id: str
    user_id: Optional[str] = None
    status: str
    confirmation_code: Optional[str] = None
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @field_serializer('created_at', 'updated_at', 'cancelled_at')
    def serialize_datetime(self, value: datetime | None, _info) -> str | None:
        """Convert datetime to ISO format string"""
        if value is None:
            return None
        return value.isoformat()
    
    class Config:
        from_attributes = True


class AppointmentListResponse(BaseModel):
    """Response schema for list of appointments"""
    appointments: list[AppointmentResponse]
    total: int
    skip: int
    limit: int

