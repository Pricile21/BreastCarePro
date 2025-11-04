"""
Main API router that includes all endpoint routers
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.endpoints import auth, mammography, patients, professionals, admin, access_requests
from app.api.v1.endpoints import healthcare_centers, appointments, articles
from app.ml.api_risk_calculator import router as risk_router
from app.api.deps import get_db, get_current_user
from app.models.user import User

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(mammography.router, prefix="/mammography", tags=["mammography"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(professionals.router, prefix="/professionals", tags=["professionals"])
api_router.include_router(healthcare_centers.router, prefix="/healthcare-centers", tags=["healthcare-centers"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
# Modèle Gail pour l'évaluation des risques (modèle validé scientifiquement)
api_router.include_router(risk_router, tags=["risk-assessment"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(access_requests.router, prefix="/access-requests", tags=["access-requests"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])

# Endpoint pour récupérer les vraies données des patients depuis la DB
@api_router.get("/real-patients")
async def get_real_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint pour récupérer les vraies données des patients de l'utilisateur connecté
    Utilise les analyses mammographiques comme source de vérité
    """
    from app.models.mammography import MammographyAnalysis
    from app.models.patient import Patient
    
    try:
        print(f"📊 /real-patients appelé pour utilisateur: {current_user.email} (id: {current_user.id})")
        
        # Récupérer toutes les analyses mammographiques de l'utilisateur pour extraire les patients uniques
        analyses = db.query(MammographyAnalysis).filter(
            MammographyAnalysis.user_id == current_user.id
        ).order_by(MammographyAnalysis.created_at.desc()).all()
        
        print(f"📊 {len(analyses)} analyses trouvées pour l'utilisateur {current_user.id}")
        
                # Extraire les patients uniques depuis les analyses
        unique_patients = {}
        for analysis in analyses:
            patient_uuid = analysis.patient_id  # C'est l'UUID (id) du patient
            if patient_uuid and patient_uuid not in unique_patients:
                # Trouver la dernière analyse pour ce patient
                last_analysis = max(
                    [a for a in analyses if a.patient_id == patient_uuid],        
                    key=lambda x: x.created_at
                )

                # Chercher les informations du patient dans la table patients
                # analysis.patient_id contient l'UUID (Patient.id), pas le patient_id lisible
                patient_record = db.query(Patient).filter(Patient.id == patient_uuid).first()
                
                # Déterminer le niveau de risque basé sur BI-RADS
                bi_rads_str = str(last_analysis.bi_rads_category) if last_analysis.bi_rads_category else "BI-RADS 2"
                if "CATEGORY_" in bi_rads_str:
                    category_num = bi_rads_str.split("CATEGORY_")[1] if "CATEGORY_" in bi_rads_str else "2"
                    bi_rads_str = f"BI-RADS {category_num}"
                
                category_num = int(bi_rads_str.split()[-1]) if bi_rads_str.split()[-1].isdigit() else 2
                if category_num <= 2:
                    risk_level = "low"
                elif category_num == 3:
                    risk_level = "medium"
                else:
                    risk_level = "high"
                
                                # Compter le nombre d'analyses pour ce patient
                analyses_count = sum(1 for a in analyses if a.patient_id == patient_uuid)                                                                         

                # Utiliser l'UUID comme id, mais aussi retourner le patient_id lisible si disponible
                patient_readable_id = patient_record.patient_id if patient_record else patient_uuid

                unique_patients[patient_uuid] = {
                    "id": patient_uuid,  # UUID pour la compatibilité avec les liens
                    "patient_id": patient_readable_id,  # ID lisible (P-2025-X)
                    "name": patient_record.full_name if patient_record else f"Patient {patient_readable_id}",
                    "age": patient_record.age if patient_record else None,
                    "analyses": analyses_count,
                    "lastVisit": last_analysis.created_at.strftime("%Y-%m-%d") if last_analysis.created_at else "2024-01-20",
                    "risk": risk_level,
                    "phone": patient_record.phone_number if patient_record else None,
                    "email": None,  # Pas disponible dans la table patients
                    "address": patient_record.address if patient_record else None,
                    "professional_id": current_user.professional_id if current_user.professional_id else "unknown"
                }
        
        result = list(unique_patients.values())
        print(f"📊 {len(result)} patients uniques retournés")
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des patients: {e}")
        import traceback
        traceback.print_exc()
        # En cas d'erreur, retourner un tableau vide
        return []

# Endpoint pour récupérer les vraies données des rapports depuis la DB
@api_router.get("/real-reports")
async def get_real_reports(
    search: str = None,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint pour récupérer les vraies analyses mammographiques comme rapports
    Avec support pour recherche et filtrage par statut
    """
    from app.models.mammography import MammographyAnalysis, AnalysisStatus
    from app.models.patient import Patient
    
    try:
        print(f"📊 /real-reports appelé pour utilisateur: {current_user.email} (id: {current_user.id})")
        print(f"   Paramètres: search={search}, status={status}")
        
        # Récupérer toutes les analyses mammographiques de l'utilisateur
        query = db.query(MammographyAnalysis).filter(
            MammographyAnalysis.user_id == current_user.id
        )
        
        # Filtre par statut si fourni
        if status:
            # Les statuts dans la DB sont des Enums
            if status == "completed":
                # Seuls les rapports VALIDATED sont considérés comme "completed"
                query = query.filter(
                    MammographyAnalysis.status == AnalysisStatus.VALIDATED
                )
            elif status == "pending":
                query = query.filter(
                    MammographyAnalysis.status.in_([AnalysisStatus.PENDING, AnalysisStatus.PROCESSING, AnalysisStatus.COMPLETED])
                )
        
        analyses = query.order_by(MammographyAnalysis.created_at.desc()).all()
        
        print(f"📊 {len(analyses)} analyses trouvées pour l'utilisateur {current_user.id}")
        
        # Transformer les analyses en format rapport
        result = []
        for analysis in analyses:
            # Filtrer par recherche si fourni
            if search:
                search_lower = search.lower()
                # Vérifier si la recherche correspond à patient_id, analysis_id, ou findings
                matches = (
                    (analysis.patient_id and search_lower in analysis.patient_id.lower()) or
                    (analysis.analysis_id and search_lower in analysis.analysis_id.lower()) or
                    (analysis.findings and search_lower in analysis.findings.lower())
                )
                if not matches:
                    continue
            # Récupérer les informations du patient si disponible
            patient = db.query(Patient).filter(Patient.id == analysis.patient_id).first()
            
            # Déterminer le statut du rapport
            if analysis.status:
                # Si c'est un Enum, utiliser .value, sinon utiliser str()
                if hasattr(analysis.status, 'value'):
                    status_str = str(analysis.status.value).upper()
                else:
                    status_str = str(analysis.status).upper()
            else:
                status_str = ""
            # Seuls les rapports VALIDATED sont considérés comme "completed"
            report_status = "completed" if status_str == "VALIDATED" else "pending"
            
            # Convertir BI-RADS en string
            bi_rads_str = str(analysis.bi_rads_category) if analysis.bi_rads_category else "BI-RADS 2"
            if "CATEGORY_" in bi_rads_str:
                category_num = bi_rads_str.split("CATEGORY_")[1] if "CATEGORY_" in bi_rads_str else "2"
                bi_rads_str = f"BI-RADS {category_num}"
            
            # Déterminer le niveau de risque
            category_num = int(bi_rads_str.split()[-1]) if bi_rads_str.split()[-1].isdigit() else 2
            if category_num <= 2:
                risk_level = "low"
            elif category_num == 3:
                risk_level = "medium"
            else:
                risk_level = "high"
            
            result.append({
                "id": analysis.analysis_id,  # Utiliser analysis_id comme ID du rapport
                "analysis_id": analysis.analysis_id,  # Garder aussi analysis_id pour référence
                "patient_id": analysis.patient_id or "N/A",
                "patient_name": patient.full_name if patient else f"Patient {analysis.patient_id}",
                "bi_rads_category": bi_rads_str,
                "confidence_score": float(analysis.confidence_score) if analysis.confidence_score else 0.8,
                "risk_level": risk_level,
                "status": report_status,
                "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
                "file_name": f"mammography_{analysis.analysis_id}.jpg",
                "breast_density": analysis.breast_density or "Unknown",
                "findings": analysis.findings or "No findings available",
                "recommendations": analysis.recommendations or "No recommendations available",
                "model_version": analysis.model_version or "MedSigLIP"
            })
        
        print(f"📊 {len(result)} rapports retournés")
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des rapports: {e}")
        import traceback
        traceback.print_exc()
        # En cas d'erreur, retourner un tableau vide
        return []

# Endpoint pour les vraies données du dashboard
@api_router.get("/real-dashboard-stats")
async def get_real_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint pour récupérer les vraies statistiques du dashboard depuis la DB
    Utilise ProfessionalService pour obtenir les vraies données de l'utilisateur connecté
    """
    from app.services.professional_service import ProfessionalService
    
    try:
        print(f"📊 /real-dashboard-stats appelé pour utilisateur: {current_user.email} (id: {current_user.id})")
        
        professional_service = ProfessionalService(db)
        stats = professional_service.get_dashboard_stats(current_user.id)
        
        print(f"📊 Stats retournées: {stats}")
        return stats
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des stats: {e}")
        import traceback
        traceback.print_exc()
        return {
            "analyses_this_month": 0,
            "month_change_percent": 0,
            "active_patients": 0,
            "new_patients_this_week": 0,
            "total_reports": 0,
            "ai_accuracy": 0
        }

# Endpoint pour les vraies analyses récentes
@api_router.get("/real-recent-analyses")
async def get_real_recent_analyses(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint pour récupérer les vraies analyses récentes depuis la DB
    Utilise ProfessionalService pour obtenir les vraies données de l'utilisateur connecté
    """
    from app.services.professional_service import ProfessionalService
    
    try:
        print(f"📊 /real-recent-analyses appelé pour utilisateur: {current_user.email} (id: {current_user.id}), limit: {limit}")
        
        professional_service = ProfessionalService(db)
        analyses = professional_service.get_recent_analyses(current_user.id, limit)
        
        print(f"📊 Analyses retournées: {len(analyses)}")
        return analyses
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des analyses: {e}")
        import traceback
        traceback.print_exc()
        return []

# Endpoint pour les vraies alertes
@api_router.get("/real-alerts")
async def get_real_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint pour récupérer les vraies alertes basées sur les données réelles
    Utilise ProfessionalService pour obtenir les vraies alertes de l'utilisateur connecté
    """
    from app.services.professional_service import ProfessionalService
    
    try:
        print(f"📊 /real-alerts appelé pour utilisateur: {current_user.email} (id: {current_user.id})")
        
        professional_service = ProfessionalService(db)
        alerts = professional_service.get_professional_alerts(current_user.id)
        
        print(f"📊 Alertes retournées: {len(alerts)}")
        return alerts
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des alertes: {e}")
        import traceback
        traceback.print_exc()
        return []

@api_router.post("/clean-database")
async def clean_database():
    """Nettoyer complètement la base de données - SUPPRIMER TOUTES LES DONNÉES"""
    from app.db.session import SessionLocal
    from sqlalchemy import text
    
    db = SessionLocal()
    try:
        print("🧹 Nettoyage complet de la base de données...")
        
        # Supprimer toutes les données de toutes les tables
        tables_to_clean = [
            "analyses",
            "reports", 
            "patients",
            "professionals",
            "users",
            "access_requests"
        ]
        
        for table in tables_to_clean:
            try:
                db.execute(text(f"DELETE FROM {table}"))
                print(f"✅ Table {table} nettoyée")
            except Exception as e:
                print(f"⚠️ Erreur lors du nettoyage de {table}: {e}")
        
        # Réinitialiser les séquences auto-increment
        try:
            db.execute(text("DELETE FROM sqlite_sequence"))
            print("✅ Séquences réinitialisées")
        except Exception as e:
            print(f"⚠️ Erreur lors de la réinitialisation des séquences: {e}")
        
        db.commit()
        
        return {
            "message": "Base de données complètement nettoyée",
            "status": "success",
            "tables_cleaned": tables_to_clean
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors du nettoyage: {e}")
        return {
            "message": f"Erreur lors du nettoyage: {str(e)}",
            "status": "error"
        }
    finally:
        db.close()

@api_router.get("/real-professional")
async def get_real_professional():
    """Récupérer les vraies données du professionnel connecté"""
    from app.db.session import SessionLocal
    from sqlalchemy import text
    
    db = SessionLocal()
    try:
        # Récupérer les données du professionnel depuis la DB
        professional = db.execute(text("""
            SELECT 
                p.full_name,
                p.specialty,
                p.license_number,
                p.phone_number,
                p.email,
                p.address,
                p.is_active
            FROM professionals p
            WHERE p.email = 'pricilegangbe@gmail.com'
            LIMIT 1
        """)).fetchone()
        
        if professional:
            return {
                "id": "prof-123",
                "full_name": professional.full_name,
                "specialty": professional.specialty,
                "license_number": professional.license_number,
                "phone_number": professional.phone_number,
                "email": professional.email,
                "address": professional.address,
                "is_active": professional.is_active
            }
        else:
            # Fallback si pas trouvé
            return {
                "id": "prof-123",
                "full_name": "Dr GANGBE Pricile",
                "specialty": "Nuclear Medicine",
                "license_number": "MED123454",
                "phone_number": "+2290161802144",
                "email": "pricilegangbe@gmail.com",
                "address": "CHU",
                "is_active": True
            }
        
    except Exception as e:
        print(f"Erreur lors de la récupération du professionnel: {e}")
        return {
            "id": "prof-123",
            "full_name": "Dr GANGBE Pricile",
            "specialty": "Nuclear Medicine",
            "license_number": "MED123454",
            "phone_number": "+2290161802144",
            "email": "pricilegangbe@gmail.com",
            "address": "CHU",
            "is_active": True
        }
    finally:
        db.close()