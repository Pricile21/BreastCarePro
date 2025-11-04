"""
Risk assessment endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.risk_assessment import RiskAssessmentRequest, RiskAssessmentResponse
from app.services.risk_assessment_service import RiskAssessmentService

router = APIRouter()


@router.post("/calculate", response_model=RiskAssessmentResponse)
async def calculate_risk(
    request: RiskAssessmentRequest,
    db: Session = Depends(get_db)
):
    """
    Calculate personalized breast cancer risk score
    """
    try:
        risk_service = RiskAssessmentService(db)
        result = await risk_service.calculate_risk(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk calculation failed: {str(e)}")


@router.get("/factors")
async def get_risk_factors():
    """
    Get list of risk factors and their weights
    """
    return {
        "risk_factors": [
            {
                "name": "age",
                "description": "Patient age",
                "weight": "High",
                "categories": ["<30", "30-40", "40-50", "50-60", ">60"]
            },
            {
                "name": "family_history",
                "description": "Family history of breast cancer",
                "weight": "Very High",
                "categories": ["None", "1st degree", "2nd degree", "Multiple"]
            },
            {
                "name": "genetic_mutations",
                "description": "Known genetic mutations",
                "weight": "Very High",
                "categories": ["None", "BRCA1", "BRCA2", "Other"]
            },
            {
                "name": "previous_biopsy",
                "description": "Previous breast biopsy",
                "weight": "Medium",
                "categories": ["Never", "Benign", "Atypical", "Malignant"]
            },
            {
                "name": "hormone_use",
                "description": "Hormone replacement therapy",
                "weight": "Medium",
                "categories": ["Never", "Current", "Past"]
            },
            {
                "name": "lifestyle_factors",
                "description": "Lifestyle and environmental factors",
                "weight": "Low",
                "categories": ["Exercise", "Diet", "Alcohol", "Smoking"]
            }
        ]
    }
