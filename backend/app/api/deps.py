"""
Common dependencies for API endpoints
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.db.session import SessionLocal
from app.models.user import User
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_db() -> Generator:
    """
    Database dependency
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Get current authenticated user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        print(f"🔍 get_current_user - Token décodé, user_id: {user_id}")
        if user_id is None:
            print("❌ get_current_user - user_id est None dans le token")
            raise credentials_exception
    except JWTError as e:
        print(f"❌ get_current_user - Erreur de décodage JWT: {e}")
        raise credentials_exception
    
    auth_service = AuthService(db)
    user = auth_service.get_user(user_id)
    if user is None:
        print(f"❌ get_current_user - Aucun utilisateur trouvé avec ID: {user_id}")
        raise credentials_exception
    
    print(f"✅ get_current_user - Utilisateur trouvé: {user.email} (ID: {user.id}, Type: {user.user_type})")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    """
    Get current active user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
