"""
Healthcare professional model
"""

from sqlalchemy import Column, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Professional(BaseModel):
    """
    Healthcare professional model
    """
    __tablename__ = "professionals"
    
    full_name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)  # radiology, oncology, etc.
    license_number = Column(String, unique=True, nullable=False)
    phone_number = Column(String)
    email = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    consultation_fee = Column(Float)
    languages = Column(Text)  # JSON string of spoken languages
    
    # Status fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
