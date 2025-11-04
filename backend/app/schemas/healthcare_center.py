"""
Healthcare Center schemas
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer


class HealthcareCenterBase(BaseModel):
    """Base healthcare center schema"""
    name: str
    type: str
    address: str
    city: str
    department: Optional[str] = None
    latitude: float
    longitude: float
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    services: Optional[List[str]] = []
    equipment: Optional[List[str]] = []
    specialties: Optional[List[str]] = []
    operating_hours: Optional[dict] = {}
    description: Optional[str] = None
    languages_spoken: Optional[List[str]] = []
    is_available: bool = True
    accepts_appointments: bool = True


class HealthcareCenterCreate(HealthcareCenterBase):
    """Healthcare center creation schema"""
    pass


class HealthcareCenterUpdate(BaseModel):
    """Healthcare center update schema"""
    name: Optional[str] = None
    type: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    department: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    services: Optional[List[str]] = None
    equipment: Optional[List[str]] = None
    specialties: Optional[List[str]] = None
    operating_hours: Optional[dict] = None
    description: Optional[str] = None
    languages_spoken: Optional[List[str]] = None
    is_available: Optional[bool] = None
    accepts_appointments: Optional[bool] = None


class HealthcareCenterResponse(HealthcareCenterBase):
    """Healthcare center response schema"""
    id: str
    rating: float = 0.0
    total_reviews: int = 0
    is_verified: bool = False
    max_appointments_per_day: int = 20
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime, _info) -> str:
        """Convert datetime to ISO format string"""
        if value is None:
            return None
        return value.isoformat()
    
    class Config:
        from_attributes = True


class HealthcareCenterListResponse(BaseModel):
    """Response schema for list of centers"""
    centers: List[HealthcareCenterResponse]
    total: int
    skip: int
    limit: int

