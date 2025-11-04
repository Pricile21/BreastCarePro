"""
Patient model
"""

from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Patient(BaseModel):
    """
    Patient model for storing patient information
    """
    __tablename__ = "patients"
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    patient_id = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    age = Column(Integer)
    phone_number = Column(String)
    address = Column(Text)
    emergency_contact = Column(String)
    medical_history = Column(Text)
    family_history = Column(Text)
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="patients")
    analyses = relationship("MammographyAnalysis", back_populates="patient")
