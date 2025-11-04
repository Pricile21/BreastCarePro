"""
Main API router that includes all endpoint routers
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, mammography, patients, professionals, risk_assessment, admin, access_requests

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(mammography.router, prefix="/mammography", tags=["mammography"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(professionals.router, prefix="/professionals", tags=["professionals"])
api_router.include_router(risk_assessment.router, prefix="/risk", tags=["risk-assessment"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(access_requests.router, prefix="/access-requests", tags=["access-requests"])

# Endpoint de test ultra-simple
@api_router.get("/test-reports")
def test_reports():
    return [
        {
            "id": "test-1",
            "patient_id": "TEST-001",
            "patient_name": "Test Patient",
            "bi_rads_category": "BI-RADS 1",
            "confidence_score": 0.95,
            "risk_level": "low",
            "status": "completed",
            "created_at": "2024-01-15T10:30:00Z",
            "file_name": "test.jpg"
        }
    ]

# Endpoint pour les vraies données des patients
@api_router.get("/real-patients")
def get_real_patients():
    """
    Endpoint pour récupérer les vraies données des patients
    Chaque professionnel voit seulement ses propres patients
    """
    # Pour l'instant, retourner les patients du Dr GANGBE Pricile
    # Dans une vraie application, on filtrerait par professional_id
    return [
        {
            "id": "P-2024-0001",
            "name": "Marie KOUASSI",
            "age": 45,
            "analyses": 2,
            "lastVisit": "2024-01-20",
            "risk": "medium",
            "phone": "+229 XX XX XX XX",
            "email": "marie.kouassi@email.com",
            "address": "Cotonou, Bénin",
            "professional_id": "prof-123"  # Dr GANGBE Pricile
        },
        {
            "id": "P-2024-0002", 
            "name": "Fatou TRAORE",
            "age": 52,
            "analyses": 3,
            "lastVisit": "2024-01-18",
            "risk": "high",
            "phone": "+229 XX XX XX XX",
            "email": "fatou.traore@email.com",
            "address": "Porto-Novo, Bénin",
            "professional_id": "prof-123"  # Dr GANGBE Pricile
        },
        {
            "id": "P-2024-0003",
            "name": "Aminata DIALLO",
            "age": 38,
            "analyses": 1,
            "lastVisit": "2024-01-15",
            "risk": "low",
            "phone": "+229 XX XX XX XX",
            "email": "aminata.diallo@email.com",
            "address": "Abomey-Calavi, Bénin",
            "professional_id": "prof-123"  # Dr GANGBE Pricile
        },
        {
            "id": "P-2024-0004",
            "name": "Grace ADJOVI",
            "age": 49,
            "analyses": 4,
            "lastVisit": "2024-01-12",
            "risk": "medium",
            "phone": "+229 XX XX XX XX",
            "email": "grace.adjovi@email.com",
            "address": "Parakou, Bénin",
            "professional_id": "prof-123"  # Dr GANGBE Pricile
        },
        {
            "id": "P-2024-0005",
            "name": "Claire ZINSOU",
            "age": 41,
            "analyses": 2,
            "lastVisit": "2024-01-10",
            "risk": "low",
            "phone": "+229 XX XX XX XX",
            "email": "claire.zinsou@email.com",
            "address": "Natitingou, Bénin",
            "professional_id": "prof-123"  # Dr GANGBE Pricile
        }
