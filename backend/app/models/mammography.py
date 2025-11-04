"""
Mammography analysis model
"""

from sqlalchemy import Column, String, Float, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class BI_RADS_Category(enum.Enum):
    """
    BI-RADS categories for mammography classification
    """
    CATEGORY_1 = "1"
    CATEGORY_2 = "2"
    CATEGORY_3 = "3"
    CATEGORY_4 = "4"
    CATEGORY_5 = "5"


class AnalysisStatus(enum.Enum):
    """
    Analysis status enumeration
    """
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    VALIDATED = "validated"
    FAILED = "failed"


class MammographyAnalysis(BaseModel):
    """
    Mammography analysis model
    """
    __tablename__ = "mammography_analyses"
    
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    analysis_id = Column(String, unique=True, index=True, nullable=False)
    
    # Analysis results
    bi_rads_category = Column(Enum(BI_RADS_Category))
    confidence_score = Column(Float)
    breast_density = Column(String)
    
    # Technical details
    model_version = Column(String)
    processing_time = Column(Float)
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    
    # File information
    original_files = Column(JSON)  # List of file paths
    processed_images = Column(JSON)  # List of processed image paths
    annotations = Column(JSON)  # Bounding boxes and findings
    
    # Clinical information
    findings = Column(Text)
    recommendations = Column(Text)
    notes = Column(Text)
    
    # Relationships - utiliser des strings pour éviter les imports circulaires
    patient = relationship("Patient", back_populates="analyses", lazy="select")
    user = relationship("User", back_populates="analyses", lazy="select")
