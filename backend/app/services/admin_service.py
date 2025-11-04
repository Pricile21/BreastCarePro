"""
Admin service for dashboard management
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc

from app.models.user import User
from app.models.professional import Professional
from app.models.patient import Patient
from app.models.mammography import MammographyAnalysis
from app.schemas.admin import (
    AdminDashboardStats,
    AccessRequestResponse,
    AccessRequestCreate,
    AccessRequestUpdate,
    UserManagementResponse,
    ProfessionalManagementResponse,
    SystemStatsResponse,
    RecentActivityResponse,
    AnalysisSummaryResponse
)


class AdminService:
    """Admin service for dashboard operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _parse_languages(self, languages_str: str) -> List[str]:
        """Parse languages from JSON string to list"""
        if not languages_str:
            return ["French"]
        
        if isinstance(languages_str, list):
            return languages_str
        
        try:
            import json
            return json.loads(languages_str)
        except (json.JSONDecodeError, TypeError):
            return ["French"]
    
    def get_dashboard_stats(self) -> AdminDashboardStats:
        """Get comprehensive dashboard statistics"""
        
        # Mobile users (patients) statistics
        total_mobile_users = self.db.query(User).filter(User.user_type == "patient").count()
        active_mobile_users = self.db.query(User).filter(
            User.user_type == "patient",
            User.is_active == True
        ).count()
        pending_mobile_users = self.db.query(User).filter(
            User.user_type == "patient",
            User.is_verified == False
        ).count()
        
        # Professional users statistics
        total_professional_users = self.db.query(User).filter(User.user_type == "professional").count()
        active_professional_users = self.db.query(User).filter(
            User.user_type == "professional",
            User.is_active == True
        ).count()
        pending_professional_users = self.db.query(User).filter(
            User.user_type == "professional",
            User.is_verified == False
        ).count()
        
        # Analysis statistics
        total_analyses = self.db.query(MammographyAnalysis).count()
        
        # Today's analyses
        today = datetime.now().date()
        analyses_today = self.db.query(MammographyAnalysis).filter(
            func.date(MammographyAnalysis.created_at) == today
        ).count()
        
        # This week's analyses
        week_start = today - timedelta(days=today.weekday())
        analyses_this_week = self.db.query(MammographyAnalysis).filter(
            func.date(MammographyAnalysis.created_at) >= week_start
        ).count()
        
        # This month's analyses
        month_start = today.replace(day=1)
        analyses_this_month = self.db.query(MammographyAnalysis).filter(
            func.date(MammographyAnalysis.created_at) >= month_start
        ).count()
        
        # High risk cases
        from app.models.mammography import BI_RADS_Category
        high_risk_cases = self.db.query(MammographyAnalysis).filter(
            or_(
                MammographyAnalysis.bi_rads_category == BI_RADS_Category.CATEGORY_4,
                MammographyAnalysis.bi_rads_category == BI_RADS_Category.CATEGORY_5
            )
        ).count()
        
        # Pending access requests (simulated - you might want to create an AccessRequest model)
        pending_access_requests = self.db.query(Professional).filter(
            Professional.is_verified == False
        ).count()
        
        return AdminDashboardStats(
            total_users=total_mobile_users,
            active_users=active_mobile_users,
            pending_users=pending_mobile_users,
            total_professionals=total_professional_users,
            active_professionals=active_professional_users,
            pending_professionals=pending_professional_users,
            total_analyses=total_analyses,
            analyses_today=analyses_today,
            analyses_this_week=analyses_this_week,
            analyses_this_month=analyses_this_month,
            high_risk_cases=high_risk_cases,
            pending_access_requests=pending_access_requests,
            system_uptime="99.9%",
            last_backup=datetime.now() - timedelta(hours=6)
        )
    
    def get_access_requests(
        self, 
        status: Optional[str] = None, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[AccessRequestResponse]:
        """Get access requests from access_requests table"""
        
        from app.models.access_request import AccessRequest
        
        query = self.db.query(AccessRequest)
        
        if status:
            query = query.filter(AccessRequest.status == status)
        
        access_requests = query.offset(skip).limit(limit).all()
        
        requests = []
        for req in access_requests:
            requests.append(AccessRequestResponse(
                id=req.id,
                professional_name=req.full_name,
                email=req.email,
                specialty=req.specialty,
                license_number=req.license_number,
                phone_number=req.phone_number,
                address=req.hospital_clinic,
                status=req.status,
                requested_at=req.created_at,
                reviewed_at=req.reviewed_at,
                reviewed_by=req.reviewed_by,
                rejection_reason=req.admin_notes,
                documents=[]
            ))
        
        return requests
    
    def _create_user_account(self, professional):
        """Créer un compte utilisateur pour un professionnel approuvé"""
        from app.models.user import User
        from app.core.security import get_password_hash
        import uuid
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = self.db.query(User).filter(User.email == professional.email).first()
        if existing_user:
            return existing_user
        
        # Créer un mot de passe temporaire (l'utilisateur devra le changer)
        temp_password = f"temp_{professional.license_number}_{uuid.uuid4().hex[:8]}"
        
        # Créer l'utilisateur
        user = User(
            id=f"user-{uuid.uuid4().hex[:8]}",
            email=professional.email,
            full_name=professional.full_name,
            hashed_password=get_password_hash(temp_password),
            is_active=True,
            is_verified=True,
            user_type="professional"
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # TODO: Envoyer un email avec le mot de passe temporaire
        print(f"Compte créé pour {professional.email} avec mot de passe temporaire: {temp_password}")
        
        return user
    
    def _create_user_account_from_request(self, access_request):
        """Créer un compte professionnel à partir d'une demande d'accès approuvée"""
        from app.models.professional import Professional
        from app.models.user import User
        import uuid
        
        print(f"🔧 Création du compte pour {access_request.email}")
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = self.db.query(User).filter(User.email == access_request.email).first()
        if existing_user:
            print(f"✅ Utilisateur existe déjà pour {access_request.email}")
            # Mettre à jour le user_type si nécessaire
            if existing_user.user_type != "professional":
                existing_user.user_type = "professional"
                self.db.commit()
            return existing_user
        
        # Vérifier si le professionnel existe déjà
        existing_professional = self.db.query(Professional).filter(Professional.email == access_request.email).first()
        professional = existing_professional
        
        if not existing_professional:
            # Créer le professionnel avec les informations de la demande
            professional = Professional(
                id=f"prof-{uuid.uuid4().hex[:8]}",
                full_name=access_request.full_name,
                specialty=access_request.specialty,
                license_number=access_request.license_number,
                phone_number=access_request.phone_number,
                email=access_request.email,
                address=access_request.hospital_clinic,
                is_active=True,
                is_verified=True
            )
            
            self.db.add(professional)
            self.db.commit()
            self.db.refresh(professional)
            print(f"✅ Professionnel créé: {professional.id}")
        else:
            print(f"✅ Professionnel existe déjà: {professional.id}")
        
        # Créer aussi un User pour l'authentification, lié au professionnel
        user = User(
            id=f"user-{uuid.uuid4().hex[:8]}",
            email=access_request.email,
            full_name=access_request.full_name,
            hashed_password=access_request.password,  # Le mot de passe est déjà hashé dans access_request
            is_active=True,
            is_verified=True,
            user_type="professional",
            professional_id=professional.id
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        print(f"✅ Compte utilisateur créé pour {access_request.email} (ID: {user.id}, Type: {user.user_type})")
        print(f"✅ Password hash utilisé (preview): {user.hashed_password[:30]}...")
        
        return professional
    
    def _create_user_account_simple(self, request_id):
        """Créer un compte utilisateur de manière simple"""
        try:
            # Récupérer les données de la demande
            result = self.db.execute(
                "SELECT full_name, email, password FROM access_requests WHERE id = ?",
                (request_id,)
            ).fetchone()
            
            if result:
                full_name, email, password = result
                
                # Vérifier si l'utilisateur existe déjà
                existing = self.db.execute(
                    "SELECT id FROM users WHERE email = ?",
                    (email,)
                ).fetchone()
                
                if not existing:
                    # Créer l'utilisateur
                    user_id = f"user-{request_id[:8]}"
                    self.db.execute(
                        "INSERT INTO users (id, email, full_name, hashed_password, is_active, is_verified, user_type, created_at, updated_at) VALUES (?, ?, ?, ?, 1, 1, 'professional', datetime('now'), datetime('now'))",
                        (user_id, email, full_name, password)
                    )
                    print(f"Compte créé pour {email}")
        except Exception as e:
            print(f"Erreur lors de la création du compte: {e}")
    
    def create_access_request(self, request_data: AccessRequestCreate) -> AccessRequestResponse:
        """Create a new access request"""
        
        # Check if professional already exists
        existing_prof = self.db.query(Professional).filter(
            Professional.email == request_data.email
        ).first()
        
        if existing_prof:
            raise ValueError("Professional with this email already exists")
        
        # Create new professional (pending verification)
        professional = Professional(
            id=f"prof-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            full_name=request_data.professional_name,
            email=request_data.email,
            specialty=request_data.specialty,
            license_number=request_data.license_number,
            phone_number=request_data.phone_number,
            address=request_data.address,
            is_active=False,
            is_verified=False,
            consultation_fee=0.0,
            languages=["French"]
        )
        
        self.db.add(professional)
        self.db.commit()
        self.db.refresh(professional)
        
        return AccessRequestResponse(
            id=professional.id,
            professional_name=professional.full_name,
            email=professional.email,
            specialty=professional.specialty,
            license_number=professional.license_number,
            phone_number=professional.phone_number,
            address=professional.address,
            status="pending",
            requested_at=professional.created_at,
            reviewed_at=None,
            reviewed_by=None,
            rejection_reason=None,
            documents=request_data.documents
        )
    
    def update_access_request(
        self, 
        request_id: str, 
        request_update: AccessRequestUpdate, 
        admin_id: str
    ) -> Optional[AccessRequestResponse]:
        """Update access request status using SQLAlchemy"""
        
        try:
            from app.models.access_request import AccessRequest
            
            # Récupérer la demande d'accès
            access_request = self.db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
            
            if not access_request:
                print(f"Demande d'accès non trouvée: {request_id}")
                return None
            
            # Mettre à jour le statut
            access_request.status = request_update.status
            access_request.reviewed_by = admin_id
            access_request.reviewed_at = datetime.now()
            access_request.admin_notes = request_update.admin_notes
            
            # Si approuvé, créer un compte utilisateur
            if request_update.status == "approved":
                self._create_user_account_from_request(access_request)
            
            self.db.commit()
            self.db.refresh(access_request)
            
            # Retourner la réponse mise à jour
            return AccessRequestResponse(
                id=access_request.id,
                professional_name=access_request.full_name,
                email=access_request.email,
                specialty=access_request.specialty,
                license_number=access_request.license_number,
                phone_number=access_request.phone_number,
                address=access_request.hospital_clinic,
                status=access_request.status,
                requested_at=access_request.created_at,
                reviewed_at=access_request.reviewed_at,
                reviewed_by=access_request.reviewed_by,
                rejection_reason=access_request.admin_notes,
                documents=[]
            )
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la demande: {e}")
            self.db.rollback()
            return None
    
    def get_users(
        self, 
        user_type: Optional[str] = None, 
        status: Optional[str] = None, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[UserManagementResponse]:
        """Get users with management information"""
        
        query = self.db.query(User)
        
        # Filtrer par type d'utilisateur
        if user_type == "patient":
            query = query.filter(User.user_type == "patient")
        elif user_type == "professional":
            query = query.filter(User.user_type == "professional")
        elif user_type == "admin":
            query = query.filter(User.user_type == "admin")
        
        # Filtrer par statut
        if status == "active":
            query = query.filter(User.is_active == True)
        elif status == "inactive":
            query = query.filter(User.is_active == False)
        elif status == "pending":
            query = query.filter(User.is_verified == False)
        
        users = query.offset(skip).limit(limit).all()
        
        user_responses = []
        for user in users:
            # Get analysis count for this user
            analysis_count = self.db.query(MammographyAnalysis).filter(
                MammographyAnalysis.user_id == user.id
            ).count()
            
            user_responses.append(UserManagementResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                user_type=user.user_type or "patient",  # Utiliser le champ user_type de la base
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at,
                last_login=user.updated_at,  # You might want to add a last_login field
                total_analyses=analysis_count,
                specialty=None
            ))
        
        return user_responses
    
    def update_user_status(self, user_id: str, is_active: bool, admin_id: str) -> bool:
        """Update user status"""
        
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return False
        
        user.is_active = is_active
        user.updated_at = datetime.now()
        self.db.commit()
        
        return True
    
    def get_professionals_management(
        self, 
        specialty: Optional[str] = None, 
        status: Optional[str] = None, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ProfessionalManagementResponse]:
        """Get professionals with management information"""
        
        query = self.db.query(Professional)
        
        if specialty:
            query = query.filter(Professional.specialty == specialty)
        
        if status == "active":
            query = query.filter(Professional.is_active == True)
        elif status == "inactive":
            query = query.filter(Professional.is_active == False)
        elif status == "pending":
            query = query.filter(Professional.is_verified == False)
        
        professionals = query.offset(skip).limit(limit).all()
        
        professional_responses = []
        for prof in professionals:
            # Get analysis count for this professional
            analysis_count = self.db.query(MammographyAnalysis).filter(
                MammographyAnalysis.user_id == prof.id
            ).count()
            
            professional_responses.append(ProfessionalManagementResponse(
                id=prof.id,
                full_name=prof.full_name,
                email=prof.email,
                specialty=prof.specialty,
                license_number=prof.license_number,
                phone_number=prof.phone_number,
                address=prof.address,
                is_active=prof.is_active,
                is_verified=prof.is_verified,
                created_at=prof.created_at,
                last_login=prof.updated_at,
                total_analyses=analysis_count,
                consultation_fee=prof.consultation_fee,
                languages=self._parse_languages(prof.languages)
            ))
        
        return professional_responses
    
    def get_system_stats(self, period: str) -> SystemStatsResponse:
        """Get system-wide statistics"""
        
        # Calculate date range based on period
        end_date = datetime.now()
        if period == "7d":
            start_date = end_date - timedelta(days=7)
        elif period == "30d":
            start_date = end_date - timedelta(days=30)
        elif period == "90d":
            start_date = end_date - timedelta(days=90)
        elif period == "1y":
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get statistics (exclure l'utilisateur admin)
        total_users = self.db.query(User).filter(User.email != "admin.cancer@data.gouv.bj").count()
        new_users = self.db.query(User).filter(
            User.created_at >= start_date,
            User.email != "admin.cancer@data.gouv.bj"
        ).count()
        
        total_analyses = self.db.query(MammographyAnalysis).count()
        new_analyses = self.db.query(MammographyAnalysis).filter(
            MammographyAnalysis.created_at >= start_date
        ).count()
        
        high_risk_detections = self.db.query(MammographyAnalysis).filter(
            and_(
                MammographyAnalysis.created_at >= start_date,
                or_(
                    MammographyAnalysis.bi_rads_category == "BI-RADS 4",
                    MammographyAnalysis.bi_rads_category == "BI-RADS 5"
                )
            )
        ).count()
        
        return SystemStatsResponse(
            period=period,
            total_users=total_users,
            new_users=new_users,
            total_analyses=total_analyses,
            new_analyses=new_analyses,
            high_risk_detections=high_risk_detections,
            system_performance={
                "cpu_usage": "45%",
                "memory_usage": "67%",
                "disk_usage": "23%",
                "response_time": "120ms"
            },
            storage_usage={
                "total_space": "500GB",
                "used_space": "150GB",
                "available_space": "350GB"
            },
            api_usage={
                "requests_today": 1250,
                "requests_this_week": 8750,
                "average_response_time": "95ms"
            }
        )
    
    def get_recent_activity(self, limit: int = 50) -> List[RecentActivityResponse]:
        """Get recent system activity"""
        
        # This is a simplified version - you might want to create an ActivityLog model
        activities = []
        
        # Get recent users
        recent_users = self.db.query(User).order_by(desc(User.created_at)).limit(10).all()
        for user in recent_users:
            activities.append(RecentActivityResponse(
                id=f"user-{user.id}",
                activity_type="user_registration",
                description=f"New user registered: {user.full_name}",
                user_id=user.id,
                user_name=user.full_name,
                timestamp=user.created_at,
                metadata={"email": user.email}
            ))
        
        # Get recent analyses
        recent_analyses = self.db.query(MammographyAnalysis).order_by(
            desc(MammographyAnalysis.created_at)
        ).limit(10).all()
        
        for analysis in recent_analyses:
            activities.append(RecentActivityResponse(
                id=f"analysis-{analysis.id}",
                activity_type="analysis_completed",
                description=f"Mammography analysis completed: {analysis.bi_rads_category}",
                user_id=analysis.user_id,
                user_name=None,
                timestamp=analysis.created_at,
                metadata={
                    "bi_rads_category": analysis.bi_rads_category,
                    "confidence_score": analysis.confidence_score
                }
            ))
        
        # Sort by timestamp and limit
        activities.sort(key=lambda x: x.timestamp, reverse=True)
        return activities[:limit]
    
    def get_analyses_summary(
        self, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> AnalysisSummaryResponse:
        """Get mammography analyses summary"""
        
        query = self.db.query(MammographyAnalysis)
        
        if start_date:
            query = query.filter(MammographyAnalysis.created_at >= start_date)
        if end_date:
            query = query.filter(MammographyAnalysis.created_at <= end_date)
        
        analyses = query.all()
        
        # Calculate statistics
        total_analyses = len(analyses)
        high_risk_cases = len([a for a in analyses if a.bi_rads_category in ["BI-RADS 4", "BI-RADS 5"]])
        medium_risk_cases = len([a for a in analyses if a.bi_rads_category == "BI-RADS 3"])
        low_risk_cases = len([a for a in analyses if a.bi_rads_category in ["BI-RADS 1", "BI-RADS 2"]])
        
        # BI-RADS distribution
        bi_rads_distribution = {}
        for analysis in analyses:
            category = analysis.bi_rads_category
            bi_rads_distribution[category] = bi_rads_distribution.get(category, 0) + 1
        
        # Density distribution
        density_distribution = {}
        for analysis in analyses:
            density = analysis.breast_density
            density_distribution[density] = density_distribution.get(density, 0) + 1
        
        # Average confidence
        if analyses:
            average_confidence = sum(a.confidence_score for a in analyses) / len(analyses)
        else:
            average_confidence = 0.0
        
        # Top findings (simplified)
        top_findings = [
            {"finding": "Mass detected", "count": high_risk_cases},
            {"finding": "Dense breast tissue", "count": len([a for a in analyses if "DENSE" in a.breast_density])},
            {"finding": "Normal findings", "count": low_risk_cases}
        ]
        
        return AnalysisSummaryResponse(
            total_analyses=total_analyses,
            high_risk_cases=high_risk_cases,
            medium_risk_cases=medium_risk_cases,
            low_risk_cases=low_risk_cases,
            bi_rads_distribution=bi_rads_distribution,
            density_distribution=density_distribution,
            average_confidence=average_confidence,
            top_findings=top_findings,
            period=f"{start_date or 'All time'} to {end_date or 'Now'}"
        )
    
    def export_reports(
        self, 
        report_type: str, 
        format: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Export system reports"""
        
        if report_type == "users":
            query = self.db.query(User)
        elif report_type == "professionals":
            query = self.db.query(Professional)
        elif report_type == "analyses":
            query = self.db.query(MammographyAnalysis)
        else:
            raise ValueError("Invalid report type")
        
        if start_date:
            query = query.filter(query.column.created_at >= start_date)
        if end_date:
            query = query.filter(query.column.created_at <= end_date)
        
        records = query.all()
        
        # Convert to dictionary format
        data = []
        for record in records:
            if hasattr(record, '__dict__'):
                data.append({k: v for k, v in record.__dict__.items() if not k.startswith('_')})
        
        return {
            "report_type": report_type,
            "format": format,
            "data": data,
            "generated_at": datetime.now(),
            "total_records": len(data)
        }
    
    def delete_user(self, user_id: str, admin_id: str) -> bool:
        """Delete user (soft delete)"""
        
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return False
        
        # Soft delete - mark as inactive
        user.is_active = False
        user.updated_at = datetime.now()
        self.db.commit()
        
        return True
    
    def reset_user_password(self, user_id: str, new_password: str, admin_id: str) -> bool:
        """Reset user password"""
        
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return False
        
        # Hash the new password
        from app.core.security import get_password_hash
        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.now()
        self.db.commit()
        
        return True
    
    def get_admin_notifications(self, unread_only: bool = False) -> List[Dict[str, Any]]:
        """Get admin notifications (simplified)"""
        
        notifications = [
            {
                "id": "notif-1",
                "title": "New Access Request",
                "message": "Dr. Marie Koffi has requested access to the platform",
                "type": "info",
                "is_read": False,
                "created_at": datetime.now() - timedelta(hours=2)
            },
            {
                "id": "notif-2",
                "title": "High Risk Case Detected",
                "message": "A BI-RADS 4 case has been detected and requires attention",
                "type": "warning",
                "is_read": False,
                "created_at": datetime.now() - timedelta(hours=4)
            },
            {
                "id": "notif-3",
                "title": "System Backup Completed",
                "message": "Daily backup has been completed successfully",
                "type": "success",
                "is_read": True,
                "created_at": datetime.now() - timedelta(hours=6)
            }
        ]
        
        if unread_only:
            notifications = [n for n in notifications if not n["is_read"]]
        
        return notifications
    
    def mark_notification_read(self, notification_id: str, admin_id: str) -> bool:
        """Mark notification as read"""
        
        # This is a simplified version - you might want to create a Notification model
        # For now, we'll just return True
        return True
