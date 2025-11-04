"""
Healthcare Center model for medical facilities offering breast cancer screening
"""

from sqlalchemy import Column, String, Float, Text, Boolean, Integer, JSON
from app.models.base import BaseModel


class HealthcareCenter(BaseModel):
    """
    Healthcare center (hospital, clinic) model for breast cancer screening facilities
    """
    __tablename__ = "healthcare_centers"
    
    # Basic Information
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)  # hospital, clinic, center, etc.
    
    # Location
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)  # Cotonou, Porto-Novo, etc.
    department = Column(String)  # Département du Bénin
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Contact
    phone_number = Column(String)
    email = Column(String)
    website = Column(String)
    
    # Services & Equipment
    services = Column(JSON)  # ["Mammographie", "Échographie", "Biopsie", etc.]
    equipment = Column(JSON)  # ["Mammographe numérique", etc.]
    specialties = Column(JSON)  # ["Oncologie", "Radiologie", "Gynécologie", etc.]
    
    # Operating Hours (JSON format: {"monday": "8h-17h", ...})
    operating_hours = Column(JSON)
    
    # Additional Information
    description = Column(Text)
    languages_spoken = Column(JSON)  # ["Français", "Fon", "Yoruba", etc.]
    
    # Ratings & Reviews (can be calculated from booking/review system)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    # Availability & Status
    is_available = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Verified by admin
    accepts_appointments = Column(Boolean, default=True)
    
    # Capacity (for booking management)
    max_appointments_per_day = Column(Integer, default=20)

