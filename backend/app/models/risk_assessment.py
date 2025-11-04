"""
Risk Assessment model
"""

from sqlalchemy import Column, String, Float, Text, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
import uuid

from app.models.base import BaseModel


class RiskLevel(enum.Enum):
    """
    Risk level enumeration
    """
    LOW = "Faible"
    MODERATE = "Modéré"
    HIGH = "Élevé"
    VERY_HIGH = "Très élevé"


class RiskAssessment(BaseModel):
    """
    Risk assessment model for breast cancer risk calculations
    """
    __tablename__ = "risk_assessments"
    
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    assessment_id = Column(String, unique=True, index=True, nullable=False, default=lambda: f"risk-{uuid.uuid4()}")
    
    # Risk calculation results
    risk_5_years = Column(Float, nullable=False, comment="Risk percentage for 5 years")
    risk_lifetime = Column(Float, comment="Lifetime risk percentage")
    risk_level = Column(Enum(RiskLevel), nullable=False)
    risk_category = Column(String, nullable=False)
    
    # Input data
    input_data = Column(JSON, nullable=False, comment="Original risk factors used in calculation")
    
    # Calculated metrics
    risk_relative = Column(Float, comment="Risk relative to average")
    average_risk_for_age = Column(Float, comment="Average risk for same age group")
    
    # Clinical information
    clinical_significance = Column(String)
    significance_explanation = Column(Text)
    recommendations = Column(JSON, comment="List of recommendations")
    educational_message = Column(JSON, comment="List of educational messages")
    critical_warnings = Column(JSON, comment="List of critical warnings")
    lifestyle_insights = Column(JSON, comment="Lifestyle factor insights")
    
    # Model information
    model_used = Column(String)
    estimated_accuracy = Column(String)
    disclaimer = Column(Text)
    
    # Additional notes
    notes = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="risk_assessments", lazy="select")


