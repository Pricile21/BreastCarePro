"""
User model
"""

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    """
    User model for authentication
    """
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=True)  # Phone number for mobile users
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    user_type = Column(String, default="patient")  # "patient" or "professional"
    professional_id = Column(String, ForeignKey("professionals.id"), nullable=True)  # NULL pour les patients mobiles
    
    # Relationships
    patients = relationship("Patient", back_populates="user")
    analyses = relationship("MammographyAnalysis", back_populates="user")
    professional = relationship("Professional", foreign_keys=[professional_id])
    risk_assessments = relationship("RiskAssessment", back_populates="user")
