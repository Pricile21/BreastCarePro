"""
Authentication service
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.auth import UserCreate, MobileUserCreate


class AuthService:
    """
    Service for authentication operations
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        print(f"🔍 Authenticate_user appelé pour email: {email}")
        user = self.get_user_by_email(email)
        if not user:
            print(f"❌ Aucun utilisateur trouvé avec l'email: {email}")
            return None
        
        print(f"✅ Utilisateur trouvé: {user.email} (ID: {user.id}, Type: {user.user_type})")
        password_valid = verify_password(password, user.hashed_password)
        print(f"🔑 Vérification du mot de passe: {'✅ VALIDE' if password_valid else '❌ INVALIDE'}")
        
        if not password_valid:
            print(f"❌ Mot de passe incorrect pour l'utilisateur: {user.email}")
            return None
        
        print(f"✅ Authentification réussie pour: {user.email} (ID: {user.id})")
        return user
    
    def create_user(self, user_in: UserCreate) -> User:
        """Create new user"""
        hashed_password = get_password_hash(user_in.password)
        user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hashed_password,
            is_active=user_in.is_active
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def create_mobile_user(self, user_in: MobileUserCreate) -> User:
        """Create new mobile user"""
        hashed_password = get_password_hash(user_in.password)
        import uuid
        user = User(
            id=f"user-{uuid.uuid4()}",
            email=user_in.email,
            full_name=user_in.name,
            phone=user_in.phone,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False,
            user_type="patient"  # Mobile users are patients
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
