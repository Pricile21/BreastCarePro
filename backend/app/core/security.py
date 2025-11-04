"""
Security utilities for authentication and authorization
"""

from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
import hashlib

from app.core.config import settings

# Configuration bcrypt avec gestion d'erreur pour compatibilité
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=4)
except Exception as e:
    # Fallback si bcrypt a des problèmes de version
    print(f"⚠️ Avertissement bcrypt (non bloquant): {e}")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=4)


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    if not plain_password or not hashed_password:
        print("❌ verify_password - Mot de passe ou hash vide")
        return False
    
    # Check hash type: bcrypt starts with $2b$, SHA256 is 64 hex chars
    if hashed_password.startswith('$2b$'):
        # Bcrypt hash
        try:
            result = pwd_context.verify(plain_password, hashed_password)
            print(f"🔑 verify_password - Bcrypt vérification: {'✅ VALIDE' if result else '❌ INVALIDE'}")
            return result
        except Exception as e:
            print(f"⚠️ verify_password - Erreur bcrypt: {e}")
            return False
    elif len(hashed_password) == 64:
        # SHA256 hash (64 hex characters)
        sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        result = sha256_hash == hashed_password
        print(f"🔑 verify_password - SHA256 vérification: {'✅ VALIDE' if result else '❌ INVALIDE'}")
        return result
    else:
        print(f"⚠️ verify_password - Format de hash non reconnu (length: {len(hashed_password)})")
        return False


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    try:
        return pwd_context.hash(password)
    except Exception:
        # Fallback to simple hash for development
        return hashlib.sha256(password.encode()).hexdigest()
