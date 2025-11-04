"""
Access request model for professional access requests
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.sql import func

from app.models.base import BaseModel


class AccessRequest(BaseModel):
    """
    Professional access request model
    """
    __tablename__ = "access_requests"
    
    # Personal information
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String)
    license_number = Column(String, nullable=False)
    
    # Professional information
    specialty = Column(String, nullable=False)
    hospital_clinic = Column(String, nullable=False)
    experience_years = Column(String, nullable=False)
    
    # Security
    password = Column(String, nullable=False)  # hashed password
    
    # Request details
    motivation = Column(Text, nullable=False)
    additional_info = Column(Text)
    
    # Status tracking
    status = Column(String, default="pending")  # pending, approved, rejected
    reviewed_by = Column(String)  # admin user ID who reviewed
    reviewed_at = Column(DateTime)
    admin_notes = Column(Text)  # admin notes about the decision
