"""
Risk assessment schemas
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class RiskAssessmentRequest(BaseModel):
    """
    Request schema for risk assessment
    """
    age: int
    family_history: str  # None, 1st_degree, 2nd_degree, multiple
    genetic_mutations: Optional[str] = None  # None, BRCA1, BRCA2, other
    previous_biopsy: Optional[str] = None  # never, benign, atypical, malignant
    hormone_use: Optional[str] = None  # never, current, past
    lifestyle_factors: Optional[Dict[str, Any]] = None


class RiskAssessmentResponse(BaseModel):
    """
    Response schema for risk assessment
    """
    risk_score: float
    risk_level: str  # low, moderate, high
    risk_factors: Dict[str, float]  # Factor name and contribution
    recommendations: list[str]
    next_screening_date: Optional[str]
    urgency: str  # low, medium, high
