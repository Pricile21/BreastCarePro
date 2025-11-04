"""
Risk assessment service
"""

from typing import Dict, Any
from sqlalchemy.orm import Session

from app.schemas.risk_assessment import RiskAssessmentRequest, RiskAssessmentResponse


class RiskAssessmentService:
    """
    Service for breast cancer risk assessment
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def calculate_risk(self, request: RiskAssessmentRequest) -> RiskAssessmentResponse:
        """
        Calculate personalized breast cancer risk score
        """
        risk_factors = {}
        total_score = 0
        
        # Age factor
        age_score = self._calculate_age_risk(request.age)
        risk_factors["age"] = age_score
        total_score += age_score
        
        # Family history factor
        family_score = self._calculate_family_history_risk(request.family_history)
        risk_factors["family_history"] = family_score
        total_score += family_score
        
        # Genetic mutations factor
        if request.genetic_mutations:
            genetic_score = self._calculate_genetic_risk(request.genetic_mutations)
            risk_factors["genetic_mutations"] = genetic_score
            total_score += genetic_score
        
        # Previous biopsy factor
        if request.previous_biopsy:
            biopsy_score = self._calculate_biopsy_risk(request.previous_biopsy)
            risk_factors["previous_biopsy"] = biopsy_score
            total_score += biopsy_score
        
        # Hormone use factor
        if request.hormone_use:
            hormone_score = self._calculate_hormone_risk(request.hormone_use)
            risk_factors["hormone_use"] = hormone_score
            total_score += hormone_score
        
        # Lifestyle factors
        if request.lifestyle_factors:
            lifestyle_score = self._calculate_lifestyle_risk(request.lifestyle_factors)
            risk_factors["lifestyle"] = lifestyle_score
            total_score += lifestyle_score
        
        # Determine risk level and recommendations
        risk_level, recommendations, urgency = self._determine_risk_level(total_score)
        
        return RiskAssessmentResponse(
            risk_score=min(total_score, 100),  # Cap at 100%
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommendations=recommendations,
            next_screening_date=self._calculate_next_screening_date(total_score),
            urgency=urgency
        )
    
    def _calculate_age_risk(self, age: int) -> float:
        """Calculate age-based risk"""
        if age < 30:
            return 5.0
        elif age < 40:
            return 10.0
        elif age < 50:
            return 20.0
        elif age < 60:
            return 25.0
        else:
            return 30.0
    
    def _calculate_family_history_risk(self, family_history: str) -> float:
        """Calculate family history risk"""
        risk_map = {
            "none": 0.0,
            "1st_degree": 15.0,
            "2nd_degree": 8.0,
            "multiple": 25.0
        }
        return risk_map.get(family_history.lower(), 0.0)
    
    def _calculate_genetic_risk(self, mutations: str) -> float:
        """Calculate genetic mutation risk"""
        risk_map = {
            "none": 0.0,
            "brca1": 40.0,
            "brca2": 35.0,
            "other": 20.0
        }
        return risk_map.get(mutations.lower(), 0.0)
    
    def _calculate_biopsy_risk(self, biopsy: str) -> float:
        """Calculate previous biopsy risk"""
        risk_map = {
            "never": 0.0,
            "benign": 5.0,
            "atypical": 15.0,
            "malignant": 30.0
        }
        return risk_map.get(biopsy.lower(), 0.0)
    
    def _calculate_hormone_risk(self, hormone_use: str) -> float:
        """Calculate hormone use risk"""
        risk_map = {
            "never": 0.0,
            "current": 10.0,
            "past": 5.0
        }
        return risk_map.get(hormone_use.lower(), 0.0)
    
    def _calculate_lifestyle_risk(self, lifestyle: Dict[str, Any]) -> float:
        """Calculate lifestyle risk factors"""
        score = 0.0
        
        # Exercise factor
        if lifestyle.get("exercise") == "none":
            score += 5.0
        elif lifestyle.get("exercise") == "light":
            score += 2.0
        
        # Diet factor
        if lifestyle.get("diet") == "unhealthy":
            score += 3.0
        
        # Alcohol factor
        if lifestyle.get("alcohol") == "heavy":
            score += 8.0
        elif lifestyle.get("alcohol") == "moderate":
            score += 3.0
        
        # Smoking factor
        if lifestyle.get("smoking") == "current":
            score += 10.0
        elif lifestyle.get("smoking") == "past":
            score += 5.0
        
        return score
    
    def _determine_risk_level(self, score: float) -> tuple[str, list[str], str]:
        """Determine risk level, recommendations, and urgency"""
        if score < 20:
            return (
                "low",
                [
                    "Continue monthly self-examinations",
                    "Maintain healthy lifestyle",
                    "Schedule routine screening in 1-2 years"
                ],
                "low"
            )
        elif score < 40:
            return (
                "moderate",
                [
                    "Consult with healthcare provider for screening schedule",
                    "Consider mammography within 6-12 months",
                    "Maintain regular follow-up appointments"
                ],
                "medium"
            )
        else:
            return (
                "high",
                [
                    "Schedule immediate consultation with specialist",
                    "Consider genetic counseling",
                    "Plan comprehensive screening (mammography + ultrasound)",
                    "Do not delay medical consultation"
                ],
                "high"
            )
    
    def _calculate_next_screening_date(self, score: float) -> str:
        """Calculate recommended next screening date"""
        if score < 20:
            return "1-2 years"
        elif score < 40:
            return "6-12 months"
        else:
            return "Immediately"
