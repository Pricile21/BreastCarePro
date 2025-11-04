"""
Appointment model for booking appointments with healthcare centers
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Appointment(BaseModel):
    """
    Appointment model for booking appointments at healthcare centers
    """
    __tablename__ = "appointments"
    
    # Foreign Keys
    center_id = Column(String, ForeignKey("healthcare_centers.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)  # Optional if anonymous booking
    
    # Patient Information
    patient_name = Column(String, nullable=False)
    patient_phone = Column(String, nullable=False)
    patient_email = Column(String, nullable=True)
    
    # Appointment Details
    appointment_date = Column(DateTime, nullable=False)
    appointment_time = Column(String, nullable=False)  # "08:00", "14:00", etc.
    
    # Additional Information
    notes = Column(Text, nullable=True)
    
    # Status
    status = Column(String, nullable=False, default="pending")  # pending, confirmed, cancelled, completed
    confirmation_code = Column(String, nullable=True)  # Unique code for patient reference
    
    # Cancellation
    cancelled_at = Column(DateTime, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    
    # Relationships
    center = relationship("HealthcareCenter", backref="appointments")
    user = relationship("User", backref="appointments")

