"""
Authentication endpoints
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import secrets

from app.api.deps import get_db, get_current_user
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.schemas.auth import Token, UserCreate, UserResponse, MobileUserCreate
from app.services.auth_service import AuthService


class LoginRequest(BaseModel):
    """Login request schema"""
    email: str  # Changed from username to email for consistency
    password: str
    source: Optional[str] = None  # Optionnel: 'mobile', 'admin', 'professional' pour bloquer les admins sur mobile


class ForgotPasswordRequest(BaseModel):
    """Forgot password request schema"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request schema"""
    token: str
    new_password: str

router = APIRouter()


@router.options("/login")
@router.options("/me")
async def options_handler():
    """Handle OPTIONS requests for CORS preflight"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    User login
    """
    print("=" * 80)
    print("🔐 ========== REQUÊTE LOGIN REÇUE ==========")
    print(f"📥 Méthode: {request.method}")
    print(f"📥 URL: {request.url}")
    print(f"📥 Headers: {dict(request.headers)}")
    
    # Lire le body directement depuis la requête
    try:
        body_bytes = await request.body()
        print(f"📦 Body brut (bytes): {body_bytes}")
        print(f"📦 Body length: {len(body_bytes)}")
        
        import json
        body_dict = json.loads(body_bytes)
        print(f"📦 Body parsé (dict): {body_dict}")
        
        # Créer LoginRequest depuis le dict
        login_data = LoginRequest(**body_dict)
        print(f"📥 Email: {login_data.email}")
        print(f"📥 Source: {login_data.source}")
        print(f"📥 Password length: {len(login_data.password) if login_data.password else 0}")
    except Exception as e:
        print(f"❌ ERREUR lors du parsing du body: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request body: {str(e)}"
        )
    
    print("=" * 80)
    
    try:
        print(f"🔐 Tentative de connexion")
        print(f"📥 Données reçues: email={login_data.email}, password={'*' * len(login_data.password) if login_data.password else 'VIDE'}")
        print(f"📋 LoginRequest validé avec email: {login_data.email}")
        
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(login_data.email, login_data.password)
    except AttributeError as e:
        print(f"❌ ERREUR AttributeError: {e}")
        print(f"📋 login_data contient: {login_data.dict() if hasattr(login_data, 'dict') else login_data}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request format: {str(e)}"
        )
    except Exception as e:
        print(f"❌ ERREUR inattendue: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    if not user:
        print(f"❌ Échec de l'authentification pour email: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Vérifier le type d'utilisateur - BLOQUER les admins sur la plateforme mobile
    user_type = getattr(user, 'user_type', None) or 'professional'
    # Récupérer source (Pydantic permet l'accès direct aux champs optionnels)
    source = login_data.source
    
    print(f"✅ Connexion réussie pour utilisateur: {user.email} (ID: {user.id}, Type: {user_type})")
    print(f"📱 Source de la requête: {source}")
    
    # BLOQUER les admins qui tentent de se connecter via la plateforme mobile
    # On bloque uniquement si source est explicitement 'mobile' ET que l'utilisateur est admin
    if source == 'mobile' and user_type == 'admin':
        print(f"🚫 ACCÈS REFUSÉ: Admin {user.email} tente de se connecter à la plateforme mobile")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Les administrateurs doivent se connecter via la plateforme admin (/admin/login)",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # CRITIQUE: S'assurer que le token contient le bon user.id
    print(f"🎫 Création du token pour user_id: {user.id} (email: {user.email})")
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    print(f"✅ Token créé avec succès pour user_id: {user.id}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user (for professionals)
    """
    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(user_in.email)
    
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    user = auth_service.create_user(user_in)
    return user


@router.post("/mobile-signup", response_model=UserResponse)
async def mobile_signup(
    user_in: MobileUserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new mobile user (for patients)
    """
    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(user_in.email)
    
    if user:
        raise HTTPException(
            status_code=400,
            detail="Un utilisateur avec cet email existe déjà.",
        )
    
    user = auth_service.create_mobile_user(user_in)
    return user


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user information - VERSION SIMPLIFIÉE
    """
    try:
        print(f"🔍 Endpoint /me appelé")
        print(f"👤 Utilisateur retourné par get_current_user:")
        print(f"   - ID: {current_user.id}")
        print(f"   - Email: {current_user.email}")
        print(f"   - Nom: {current_user.full_name}")
        print(f"   - Type: {current_user.user_type or 'professional'}")
        
        # SOLUTION SIMPLE: Retourner directement l'utilisateur sans requêtes complexes
        user_response = {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "is_active": current_user.is_active,
            "is_verified": current_user.is_verified,
            "professional_id": current_user.professional_id,
            "user_type": current_user.user_type or "professional"
        }
        
        print(f"✅ Réponse /me préparée: {user_response}")
        return user_response
        
    except Exception as e:
        print(f"❌ Erreur dans /me: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Store reset tokens in memory (in production, use Redis or database)
reset_tokens_store: dict[str, tuple[str, float]] = {}  # token -> (email, timestamp)


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Request password reset
    
    Si un service email est configuré, le token sera envoyé par email.
    Sinon, le token est retourné dans la réponse (à utiliser avec précaution en production).
    """
    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(request.email)
    
    # Always return success to prevent email enumeration attacks
    if user:
        # Generate a secure token
        reset_token = secrets.token_urlsafe(32)
        import time
        reset_tokens_store[reset_token] = (user.email, time.time())
        
        # Option 1: Si service email configuré, envoyer par email
        # TODO: Intégrer ici votre service d'envoi d'email (SendGrid, Mailgun, SMTP, etc.)
        # if settings.EMAIL_ENABLED:
        #     send_reset_email(user.email, reset_token)
        #     return {"message": "Si un compte existe avec cet email, vous recevrez un lien de réinitialisation."}
        
        # Option 2: Sans service email, retourner le token dans la réponse
        # ATTENTION: En production publique, c'est moins sécurisé (le token est visible)
        # Mais fonctionnel si vous préférez ne pas configurer d'email
        # Détermine l'URL du frontend depuis les origines CORS ou utilise localhost par défaut
        frontend_url = "http://localhost:3000"
        if settings.BACKEND_CORS_ORIGINS:
            # Prendre la première origine qui semble être un frontend
            for origin in settings.BACKEND_CORS_ORIGINS:
                if "localhost" in origin or "127.0.0.1" in origin:
                    frontend_url = origin
                    break
        
        reset_link = f"{frontend_url}/mobile/reset-password?token={reset_token}"
        
        return {
            "message": "Un lien de réinitialisation a été généré.",
            "token": reset_token,  # Retourné pour affichage dans l'interface
            "reset_link": reset_link,  # Lien direct pour faciliter l'utilisation
            "warning": "Sans service email configuré, ce token est visible. Pour plus de sécurité, configurez un service d'envoi d'email."
        }
    
    # Même réponse si l'utilisateur n'existe pas (sécurité)
    return {
        "message": "Si un compte existe avec cet email, vous recevrez un lien de réinitialisation."
    }


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset password using token
    """
    import time
    
    # Check if token exists and is not expired (24 hours)
    if request.token not in reset_tokens_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de réinitialisation invalide ou expiré"
        )
    
    email, timestamp = reset_tokens_store[request.token]
    
    # Check if token is expired (24 hours)
    if time.time() - timestamp > 86400:  # 24 hours
        del reset_tokens_store[request.token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de réinitialisation expiré"
        )
    
    # Validate password strength
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le mot de passe doit contenir au moins 6 caractères"
        )
    
    # Update user password
    auth_service = AuthService(db)
    user = auth_service.get_user_by_email(email)
    
    if not user:
        del reset_tokens_store[request.token]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    db.commit()
    
    # Delete used token
    del reset_tokens_store[request.token]
    
    return {"message": "Mot de passe réinitialisé avec succès"}
