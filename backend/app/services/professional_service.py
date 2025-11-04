"""
Healthcare professional service
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc

from app.models.professional import Professional
from app.models.mammography import MammographyAnalysis
from app.models.patient import Patient
from app.schemas.professional import ProfessionalCreate, ProfessionalUpdate


class ProfessionalService:
    """
    Service for healthcare professional operations
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_professional(self, professional_in: ProfessionalCreate) -> Professional:
        """Create new healthcare professional"""
        professional = Professional(
            id=str(uuid.uuid4()),
            full_name=professional_in.full_name,
            specialty=professional_in.specialty,
            license_number=professional_in.license_number,
            phone_number=professional_in.phone_number,
            email=professional_in.email,
            address=professional_in.address,
            latitude=professional_in.latitude,
            longitude=professional_in.longitude,
            consultation_fee=professional_in.consultation_fee,
            languages=professional_in.languages
        )
        
        self.db.add(professional)
        self.db.commit()
        self.db.refresh(professional)
        return professional
    
    def get_professional(self, professional_id: str) -> Optional[Professional]:
        """Get professional by ID"""
        return self.db.query(Professional).filter(Professional.id == professional_id).first()
    
    def update_professional(
        self, 
        professional_id: str, 
        professional_update: ProfessionalUpdate
    ) -> Optional[Professional]:
        """Update professional information"""
        professional = self.get_professional(professional_id)
        if not professional:
            return None
        
        update_data = professional_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(professional, field, value)
        
        self.db.commit()
        self.db.refresh(professional)
        return professional
    
    def list_professionals(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        specialty: Optional[str] = None
    ) -> List[Professional]:
        """List professionals with optional filtering"""
        query = self.db.query(Professional)
        
        if specialty:
            query = query.filter(Professional.specialty.ilike(f"%{specialty}%"))
        
        return query.offset(skip).limit(limit).all()
    
    def find_nearby_professionals(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: int = 50,
        specialty: str = "radiology"
    ) -> List[Professional]:
        """Find nearby professionals using geolocation"""
        # Using Haversine formula for distance calculation
        # This is a simplified version - in production, use PostGIS or similar
        
        query = self.db.query(Professional).filter(
            Professional.latitude.isnot(None),
            Professional.longitude.isnot(None),
            Professional.specialty.ilike(f"%{specialty}%")
        )
        
        # For now, return all professionals in the specialty
        # TODO: Implement proper geolocation filtering
        return query.limit(20).all()
    
    def get_dashboard_stats(self, user_id: str) -> Dict[str, Any]:
        """Get professional dashboard statistics"""
        
        print(f"📊 get_dashboard_stats appelé avec user_id: {user_id}")
        
        # SOLUTION : Chercher par professional_id au lieu de user_id
        from app.models.user import User
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            print(f"❌ Utilisateur non trouvé avec user_id: {user_id}")
            return {"analyses_this_month": 0, "month_change_percent": 0, "active_patients": 0, "new_patients_this_week": 0, "total_reports": 0, "ai_accuracy": 0}
        
        print(f"✅ Utilisateur trouvé: {user.email} (id: {user.id}, professional_id: {user.professional_id})")
        
        if not user.professional_id:
            # Si pas de professional_id, chercher par email
            from app.models.professional import Professional
            professional = self.db.query(Professional).filter(Professional.email == user.email).first()
            if not professional:
                print(f"❌ Professionnel non trouvé pour email: {user.email}")
                return {"analyses_this_month": 0, "month_change_percent": 0, "active_patients": 0, "new_patients_this_week": 0, "total_reports": 0, "ai_accuracy": 0}
            professional_id = professional.id
            print(f"✅ Professionnel trouvé par email: {professional_id}")
        else:
            professional_id = user.professional_id
        
        # Vérifier toutes les analyses existantes (pour debug)
        all_analyses = self.db.query(MammographyAnalysis).all()
        print(f"📋 Total analyses dans la DB: {len(all_analyses)}")
        
        # Vérifier les analyses pour ce user_id
        user_analyses = self.db.query(MammographyAnalysis).filter(
            MammographyAnalysis.user_id == user_id
        ).all()
        print(f"📋 Analyses pour user_id={user_id}: {len(user_analyses)}")
        if user_analyses:
            print(f"   Exemples de user_id dans les analyses: {[a.user_id for a in user_analyses[:3]]}")
        
        # Analyses this month
        today = datetime.now().date()
        month_start = today.replace(day=1)
        analyses_this_month = self.db.query(MammographyAnalysis).filter(
            and_(
                MammographyAnalysis.user_id == user_id,
                func.date(MammographyAnalysis.created_at) >= month_start
            )
        ).count()
        print(f"📅 Analyses ce mois (depuis {month_start}): {analyses_this_month}")
        
        # Analyses last month for comparison
        last_month_start = (month_start - timedelta(days=1)).replace(day=1)
        analyses_last_month = self.db.query(MammographyAnalysis).filter(
            and_(
                MammographyAnalysis.user_id == user_id,
                func.date(MammographyAnalysis.created_at) >= last_month_start,
                func.date(MammographyAnalysis.created_at) < month_start
            )
        ).count()
        
        # Calculate percentage change
        if analyses_last_month > 0:
            month_change = ((analyses_this_month - analyses_last_month) / analyses_last_month) * 100
        else:
            month_change = 0
        
        # Active patients (unique patients with analyses)
        active_patients = self.db.query(MammographyAnalysis.patient_id).filter(
            MammographyAnalysis.user_id == user_id
        ).distinct().count()
        
        # New patients this week
        week_start = today - timedelta(days=today.weekday())
        new_patients_this_week = self.db.query(MammographyAnalysis.patient_id).filter(
            and_(
                MammographyAnalysis.user_id == user_id,
                func.date(MammographyAnalysis.created_at) >= week_start
            )
        ).distinct().count()
        
        # Total reports generated
        total_reports = self.db.query(MammographyAnalysis).filter(
            MammographyAnalysis.user_id == user_id
        ).count()
        print(f"📊 Total rapports: {total_reports}")
        
        # AI accuracy (average confidence score)
        avg_confidence = self.db.query(func.avg(MammographyAnalysis.confidence_score)).filter(
            MammographyAnalysis.user_id == user_id
        ).scalar() or 0
        print(f"📊 Confiance moyenne: {avg_confidence}")
        
        result = {
            "analyses_this_month": analyses_this_month,
            "month_change_percent": round(month_change, 1),
            "active_patients": active_patients,
            "new_patients_this_week": new_patients_this_week,
            "total_reports": total_reports,
            "ai_accuracy": round(avg_confidence * 100, 1) if avg_confidence else 0
        }
        print(f"📊 Résultat final: {result}")
        return result
    
    def get_recent_analyses(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent analyses for the professional"""
        
        # SOLUTION : Chercher par professional_id au lieu de user_id
        from app.models.user import User
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.professional_id:
            # Si pas de professional_id, chercher par email
            from app.models.professional import Professional
            professional = self.db.query(Professional).filter(Professional.email == user.email).first()
            if not professional:
                return []
            professional_id = professional.id
        else:
            professional_id = user.professional_id
        
        analyses = self.db.query(MammographyAnalysis).filter(
            MammographyAnalysis.user_id == user_id
        ).order_by(desc(MammographyAnalysis.created_at)).limit(limit).all()
        
        results = []
        for analysis in analyses:
            # Determine risk level based on BI-RADS
            risk_level = "low"
            if analysis.bi_rads_category in ["BI-RADS 4", "BI-RADS 5"]:
                risk_level = "high"
            elif analysis.bi_rads_category == "BI-RADS 3":
                risk_level = "medium"
            
            # Calculate time ago
            time_ago = datetime.now() - analysis.created_at
            if time_ago.days > 0:
                time_str = f"Il y a {time_ago.days} jour{'s' if time_ago.days > 1 else ''}"
            elif time_ago.seconds > 3600:
                hours = time_ago.seconds // 3600
                time_str = f"Il y a {hours} heure{'s' if hours > 1 else ''}"
            else:
                minutes = time_ago.seconds // 60
                time_str = f"Il y a {minutes} minute{'s' if minutes > 1 else ''}"
            
            results.append({
                "id": analysis.id,
                "patient_id": analysis.patient_id,
                "bi_rads_category": analysis.bi_rads_category,
                "confidence_score": analysis.confidence_score,
                "risk_level": risk_level,
                "created_at": analysis.created_at,
                "time_ago": time_str
            })
        
        return results
    
    def get_professional_alerts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get alerts and notifications for the professional"""
        
        # SOLUTION : Chercher par professional_id au lieu de user_id
        from app.models.user import User
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.professional_id:
            # Si pas de professional_id, chercher par email
            from app.models.professional import Professional
            professional = self.db.query(Professional).filter(Professional.email == user.email).first()
            if not professional:
                return []
            professional_id = professional.id
        else:
            professional_id = user.professional_id
        
        alerts = []
        
        # High risk cases requiring attention
        from app.models.mammography import BI_RADS_Category, AnalysisStatus
        high_risk_analyses = self.db.query(MammographyAnalysis).filter(
            and_(
                MammographyAnalysis.user_id == user_id,
                or_(
                    MammographyAnalysis.bi_rads_category == BI_RADS_Category.CATEGORY_4,
                    MammographyAnalysis.bi_rads_category == BI_RADS_Category.CATEGORY_5
                )
            )
        ).order_by(desc(MammographyAnalysis.created_at)).limit(5).all()
        
        for analysis in high_risk_analyses:
            # Convertir BI-RADS pour affichage
            bi_rads_display = str(analysis.bi_rads_category)
            if hasattr(analysis.bi_rads_category, 'value'):
                bi_rads_display = f"BI-RADS {analysis.bi_rads_category.value}"
            elif "CATEGORY_" in bi_rads_display:
                category_num = bi_rads_display.split("CATEGORY_")[-1]
                bi_rads_display = f"BI-RADS {category_num}"
            
            alerts.append({
                "id": f"alert-{analysis.id}",
                "type": "high_risk",
                "title": f"Patient {analysis.patient_id} - {bi_rads_display}",
                "message": "Anomalie suspecte détectée. Validation requise.",
                "severity": "high",
                "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
                "analysis_id": analysis.analysis_id,
                "patient_id": analysis.patient_id
            })
        
        # Pending reports
        pending_reports = self.db.query(MammographyAnalysis).filter(
            and_(
                MammographyAnalysis.user_id == user_id,
                MammographyAnalysis.status == AnalysisStatus.COMPLETED
            )
        ).count()
        
        if pending_reports > 0:
            alerts.append({
                "id": "pending-reports",
                "type": "pending_reports",
                "title": f"{pending_reports} rapport{'s' if pending_reports > 1 else ''} en attente",
                "message": "Rapports prêts à être validés et envoyés",
                "severity": "medium",
                "created_at": datetime.now().isoformat()
            })
        
        # System updates
        alerts.append({
            "id": "system-update",
            "type": "system",
            "title": "Mise à jour système",
            "message": "Nouvelle version du modèle IA disponible",
            "severity": "low",
            "created_at": datetime.now().isoformat()
        })
        
        return alerts
    
    def get_professional_reports(
        self, 
        user_id: str, 
        skip: int = 0, 
        limit: int = 50, 
        search: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get professional reports with optional filtering"""
        
        # Importer MammographyAnalysis ici pour éviter les imports circulaires
        from app.models.mammography import MammographyAnalysis
        
        # SOLUTION : Chercher par professional_id au lieu de user_id
        # D'abord, récupérer l'utilisateur pour obtenir son professional_id
        from app.models.user import User
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.professional_id:
            # Si pas de professional_id, chercher par email
            from app.models.professional import Professional
            professional = self.db.query(Professional).filter(Professional.email == user.email).first()
            if not professional:
                return []
            professional_id = professional.id
        else:
            professional_id = user.professional_id
        
        # Chercher les analyses par user_id (le modèle n'a pas de professional_id)
        query = self.db.query(MammographyAnalysis).filter(
            MammographyAnalysis.user_id == user_id
        )
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    MammographyAnalysis.patient_id.ilike(search_term),
                    MammographyAnalysis.id.ilike(search_term)
                )
            )
        
        # Apply status filter
        if status:
            if status == "pending":
                query = query.filter(MammographyAnalysis.status == "PENDING")
            elif status == "completed":
                query = query.filter(MammographyAnalysis.status == "COMPLETED")
        
        # Order by creation date (newest first)
        analyses = query.order_by(desc(MammographyAnalysis.created_at)).offset(skip).limit(limit).all()
        
        results = []
        for analysis in analyses:
            # Format date
            date_str = analysis.created_at.strftime("%Y-%m-%d")

            # Determine status
            status_display = "En attente" if analysis.status == "PENDING" else "Complété"

            # Récupérer le patient_id lisible depuis la table patients
            patient_readable_id = "N/A"
            if analysis.patient_id:
                patient = self.db.query(Patient).filter(Patient.id == analysis.patient_id).first()
                if patient:
                    patient_readable_id = patient.patient_id  # Le patient_id lisible (P-2025-1)
                else:
                    # Fallback: utiliser les 4 derniers caractères de l'UUID si patient non trouvé
                    patient_readable_id = f"P-{analysis.created_at.strftime('%Y')}-{analysis.patient_id[-4:]}"

            results.append({
                "id": f"R-{analysis.created_at.strftime('%Y')}-{analysis.id[-4:]}",
                "analysis_id": analysis.id,
                "patient_id": patient_readable_id,
                "date": date_str,
                "bi_rads": analysis.bi_rads_category,
                "status": "pending" if analysis.status == "PENDING" else "completed",
                "status_display": status_display,
                "confidence_score": analysis.confidence_score,
                "created_at": analysis.created_at
            })
        
        return results
    
    def get_professional_report(self, report_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific professional report"""
        
        # Extract analysis ID from report ID (format: R-YYYY-XXXX)
        try:
            analysis_id = report_id.split('-')[-1]
            # Find the full analysis ID
            analysis = self.db.query(MammographyAnalysis).filter(
                and_(
                    MammographyAnalysis.user_id == user_id,
                    MammographyAnalysis.id.like(f"%{analysis_id}")
                )
            ).first()
            
            if not analysis:
                return None
            
            # Récupérer le patient_id lisible depuis la table patients
            patient_readable_id = "N/A"
            if analysis.patient_id:
                patient = self.db.query(Patient).filter(Patient.id == analysis.patient_id).first()
                if patient:
                    patient_readable_id = patient.patient_id  # Le patient_id lisible (P-2025-1)
                else:
                    # Fallback: utiliser les 4 derniers caractères de l'UUID si patient non trouvé
                    patient_readable_id = f"P-{analysis.created_at.strftime('%Y')}-{analysis.patient_id[-4:]}"
            
            return {
                "id": report_id,
                "analysis_id": analysis.id,
                "patient_id": patient_readable_id,
                "date": analysis.created_at.strftime("%Y-%m-%d"),
                "bi_rads": analysis.bi_rads_category,
                "status": "pending" if analysis.status == "PENDING" else "completed",
                "confidence_score": analysis.confidence_score,
                "breast_density": analysis.breast_density,
                "findings": analysis.findings,
                "recommendations": analysis.recommendations,
                "notes": analysis.notes,
                "created_at": analysis.created_at,
                "updated_at": analysis.updated_at
            }
        except Exception:
            return None
    
    def download_report(self, report_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Download a professional report"""
        
        report = self.get_professional_report(report_id, user_id)
        if not report:
            return None
        
        # Generate report content (in a real app, this would be a PDF or formatted document)
        report_content = {
            "report_id": report["id"],
            "patient_id": report["patient_id"],
            "date": report["date"],
            "bi_rads_category": report["bi_rads"],
            "confidence_score": report["confidence_score"],
            "breast_density": report["breast_density"],
            "findings": report["findings"],
            "recommendations": report["recommendations"],
            "notes": report["notes"],
            "generated_at": datetime.now().isoformat()
        }
        
        return report_content
