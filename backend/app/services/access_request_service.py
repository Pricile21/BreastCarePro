"""
Service for managing access requests
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.access_request import AccessRequest
from app.models.user import User
from app.schemas.access_request import AccessRequestCreate, AccessRequestUpdate
from app.core.security import get_password_hash
import uuid


class AccessRequestService:
    def __init__(self, db: Session):
        self.db = db

    def create_access_request(self, request_data: AccessRequestCreate) -> AccessRequest:
        """Create a new access request"""
        access_request = AccessRequest(
            id=str(uuid.uuid4()),
            full_name=request_data.full_name,
            email=request_data.email,
            phone_number=request_data.phone_number,
            license_number=request_data.license_number,
            specialty=request_data.specialty,
            hospital_clinic=request_data.hospital_clinic,
            experience_years=request_data.experience_years,
            password=get_password_hash(request_data.password),
            motivation=request_data.motivation,
            additional_info=request_data.additional_info,
            status="pending"
        )
        
        self.db.add(access_request)
        self.db.commit()
        self.db.refresh(access_request)
        
        return access_request

    def get_access_requests(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[AccessRequest]:
        """Get access requests with optional status filter"""
        query = self.db.query(AccessRequest)
        
        if status:
            query = query.filter(AccessRequest.status == status)
        
        return query.offset(skip).limit(limit).all()

    def get_access_request(self, request_id: str) -> Optional[AccessRequest]:
        """Get a specific access request by ID"""
        return self.db.query(AccessRequest).filter(AccessRequest.id == request_id).first()

    def update_access_request(self, request_id: str, request_data: AccessRequestUpdate) -> Optional[AccessRequest]:
        """Update an access request"""
        access_request = self.get_access_request(request_id)
        if not access_request:
            return None
        
        update_data = request_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(access_request, field, value)
        
        self.db.commit()
        self.db.refresh(access_request)
        
        return access_request

    def approve_request(self, request_id: str, admin_user_id: str, admin_notes: str = None) -> Optional[AccessRequest]:
        """Approve an access request and create user account"""
        from app.models.professional import Professional
        
        access_request = self.get_access_request(request_id)
        if not access_request:
            return None
        
        print(f"🔧 Approbation de la demande d'accès pour {access_request.email}")
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = self.db.query(User).filter(User.email == access_request.email).first()
        if existing_user:
            # L'utilisateur existe déjà, mettre à jour le type si nécessaire
            print(f"✅ Utilisateur existe déjà pour {access_request.email}")
            if existing_user.user_type != "professional":
                existing_user.user_type = "professional"
                self.db.commit()
            # Marquer la demande comme approuvée
            access_request.status = "approved"
            access_request.reviewed_by = admin_user_id
            access_request.reviewed_at = datetime.utcnow()
            access_request.admin_notes = admin_notes
        else:
            # Vérifier si le professionnel existe déjà
            existing_professional = self.db.query(Professional).filter(Professional.email == access_request.email).first()
            professional = existing_professional
            
            if not existing_professional:
                # Créer le professionnel
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
            
            # Créer un nouvel utilisateur avec user_type="professional"
            new_user = User(
                id=f"user-{uuid.uuid4().hex[:8]}",
                email=access_request.email,
                full_name=access_request.full_name,
                hashed_password=access_request.password,  # Le mot de passe est déjà hashé
                is_active=True,
                is_verified=True,
                user_type="professional",
                professional_id=professional.id if professional else None
            )
            self.db.add(new_user)
            print(f"✅ Utilisateur créé pour {access_request.email} (Type: professional)")
            
            # Marquer la demande comme approuvée
            access_request.status = "approved"
            access_request.reviewed_by = admin_user_id
            access_request.reviewed_at = datetime.utcnow()
            access_request.admin_notes = admin_notes
        
        self.db.commit()
        self.db.refresh(access_request)
        print(f"✅ Demande d'accès approuvée pour {access_request.email}")
        
        return access_request

    def reject_request(self, request_id: str, admin_user_id: str, admin_notes: str = None) -> Optional[AccessRequest]:
        """Reject an access request"""
        access_request = self.get_access_request(request_id)
        if not access_request:
            return None
        
        access_request.status = "rejected"
        access_request.reviewed_by = admin_user_id
        access_request.reviewed_at = datetime.utcnow()
        access_request.admin_notes = admin_notes
        
        self.db.commit()
        self.db.refresh(access_request)
        
        return access_request

    def get_pending_requests_count(self) -> int:
        """Get count of pending requests"""
        return self.db.query(AccessRequest).filter(AccessRequest.status == "pending").count()
