"""
BreastCare Pro - Main FastAPI Application
"""

from fastapi import FastAPI, Request
import sys
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db.init_db import migrate_sqlite_schema, init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for breast cancer screening and risk assessment using AI",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize database and seed initial data on startup
    """
    print("\n" + "="*80)
    print("🚀 DÉMARRAGE DU BACKEND BREASTCARE")
    print("="*80)
    print(f"📡 Serveur écoute sur: http://0.0.0.0:8000")
    print(f"📚 Documentation: http://localhost:8000/docs")
    print(f"🏥 Health check: http://localhost:8000/health")
    print("="*80 + "\n")
    
    try:
        from app.models.base import Base
        # Import all models to ensure they're registered with Base.metadata
        from app.models import healthcare_center, user, patient, mammography, professional, access_request, appointment, risk_assessment
        from app.models.healthcare_center import HealthcareCenter
        from app.models.user import User
        from app.models.patient import Patient
        from app.models.mammography import MammographyAnalysis
        from app.models.professional import Professional
        from app.models.access_request import AccessRequest
        from app.models.appointment import Appointment
        from app.models.risk_assessment import RiskAssessment
        
        # Apply lightweight SQLite schema migrations before ensuring tables
        migrate_sqlite_schema(engine)

        # Create all tables if they don't exist
        print("🏗️  Création des tables si nécessaire...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables vérifiées")
        
        # Initialize database and create default admin account
        from app.db.session import SessionLocal
        from app.db.seed_centers import seed_centers, BENIN_CENTERS
        
        db = SessionLocal()
        try:
            # Créer le compte admin s'il n'existe pas
            print("👤 Vérification/création du compte admin...")
            init_db(db)
            
            # Seed healthcare centers if table is empty
            center_count = db.query(HealthcareCenter).count()
            if center_count == 0:
                print(f"📋 Aucun centre trouvé. Chargement de {len(BENIN_CENTERS)} centres...")
                seed_centers(db)
            else:
                print(f"✅ {center_count} centres déjà dans la base")
        finally:
            db.close()
            
    except Exception as e:
        print(f"⚠️  Erreur lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()

# Middleware de logging pour voir toutes les requêtes
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        import sys
        from datetime import datetime
        start_time = time.time()
        print(f"\n{'='*80}")
        print(f"🌐 [MIDDLEWARE] REQUÊTE REÇUE: {request.method} {request.url.path}")
        print(f"🌐 [MIDDLEWARE] Timestamp: {datetime.now().isoformat()}")
        print(f"🌐 [MIDDLEWARE] Client: {request.client.host if request.client else 'N/A'}")
        print(f"📥 [MIDDLEWARE] Headers: {dict(request.headers)}")
        sys.stdout.flush()
        
        # IMPORTANT: Ne pas lire le body ici car cela consomme le stream
        # et empêche FastAPI de parser le JSON. Utiliser request.client.host pour info.
        if request.method == "POST":
            content_type = request.headers.get("content-type", "")
            content_length = request.headers.get("content-length", "unknown")
            origin = request.headers.get("origin", "N/A")
            print(f"📦 [MIDDLEWARE] Body info: Content-Type={content_type}, Length={content_length}")
            print(f"📦 [MIDDLEWARE] Origin: {origin}")
            sys.stdout.flush()
        
        print(f"{'='*80}\n")
        sys.stdout.flush()
        
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"✅ [MIDDLEWARE] Réponse envoyée: {response.status_code} (en {process_time:.3f}s)")
        sys.stdout.flush()
        return response

# Ajouter le middleware de logging AVANT CORS
app.add_middleware(LoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware - allow localhost and 127.0.0.1
# DÉSACTIVÉ TEMPORAIREMENT - Peut bloquer les requêtes en développement
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"],
# )

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "BreastCare Pro API",
        "version": settings.VERSION,
        "status": "active",
        "description": "AI-powered breast cancer screening platform for Africa"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "breastcare-api"}

@app.post("/admin/fix-professional-account")
async def fix_professional_account(email: str = "pricilegangbe@gmail.com"):
    """
    Endpoint de diagnostic pour vérifier/créer le compte professionnel
    """
    from app.db.session import SessionLocal
    from app.models.user import User
    from app.models.professional import Professional
    from app.models.access_request import AccessRequest
    from app.core.security import get_password_hash, verify_password
    from app.services.admin_service import AdminService
    
    db = SessionLocal()
    try:
        result = {
            "email": email,
        }
        
        # Chercher la demande d'accès
        access_request = db.query(AccessRequest).filter(AccessRequest.email == email).first()
        
        if not access_request:
            return {"error": "Aucune demande d'accès trouvée", **result}
        
        result["access_request"] = {
            "status": access_request.status,
            "full_name": access_request.full_name,
            "password_hash_preview": access_request.password[:30] + "..." if access_request.password else None
        }
        
        # Chercher l'utilisateur
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Si la demande est approuvée, créer le compte
            if access_request.status == "approved":
                admin_service = AdminService(db)
                try:
                    admin_service._create_user_account_from_request(access_request)
                    
                    # Re-vérifier l'utilisateur créé
                    user = db.query(User).filter(User.email == email).first()
                    result["action"] = "created"
                    result["message"] = "Compte professionnel créé"
                    result["user"] = {
                        "exists": True,
                        "user_type": user.user_type if user else None,
                        "is_active": user.is_active if user else None,
                    }
                except Exception as e:
                    return {"error": str(e), **result}
            else:
                return {"error": "Demande d'accès non approuvée", "status": access_request.status, **result}
        else:
            result["user"] = {
                "exists": True,
                "user_type": user.user_type,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "password_hash_preview": user.hashed_password[:30] + "..." if user.hashed_password else None,
            }
            
            # Vérifier si le user_type est correct
            if user.user_type != "professional":
                user.user_type = "professional"
                db.commit()
                result["action"] = "updated"
                result["message"] = "user_type mis à jour vers 'professional'"
            else:
                result["action"] = "exists"
                result["message"] = "Compte existe déjà et est correct"
            
            # Vérifier que le mot de passe correspond
            if access_request.password and user.hashed_password:
                passwords_match = (access_request.password == user.hashed_password)
                result["password_match"] = passwords_match
                if not passwords_match:
                    # Corriger le mot de passe
                    user.hashed_password = access_request.password
                    db.commit()
                    result["action"] = "password_fixed"
                    result["message"] = "Mot de passe corrigé pour correspondre à la demande d'accès"
        
        # Chercher le professionnel
        professional = db.query(Professional).filter(Professional.email == email).first()
        result["professional"] = {
            "exists": professional is not None,
            "name": professional.full_name if professional else None,
            "id": professional.id if professional else None,
        }
        
        return result
    except Exception as e:
        db.rollback()
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}
    finally:
        db.close()

@app.post("/admin/fix-admin-account")
async def fix_admin_account():
    """
    Endpoint de diagnostic pour vérifier/créer le compte admin
    """
    from app.db.session import SessionLocal
    from app.models.user import User
    from app.core.security import get_password_hash, verify_password
    
    db = SessionLocal()
    try:
        admin_email = "admin@breastcare.bj"
        admin_password = "admin123"
        
        admin_user = db.query(User).filter(User.email == admin_email).first()
        
        result = {
            "email": admin_email,
            "exists": admin_user is not None,
            "user_type": admin_user.user_type if admin_user else None,
            "is_active": admin_user.is_active if admin_user else None,
        }
        
        if not admin_user:
            # Créer le compte
            admin_user = User(
                id="admin-001",
                email=admin_email,
                full_name="Admin BreastCare",
                hashed_password=get_password_hash(admin_password),
                is_active=True,
                is_verified=True,
                user_type="admin"
            )
            db.add(admin_user)
            db.commit()
            result["action"] = "created"
            result["message"] = "Compte admin créé"
        else:
            # Tester le mot de passe
            password_valid = verify_password(admin_password, admin_user.hashed_password)
            result["password_valid"] = password_valid
            result["hash_preview"] = admin_user.hashed_password[:30] + "..."
            result["hash_length"] = len(admin_user.hashed_password)
            
            if not password_valid:
                # Réinitialiser le hash
                admin_user.hashed_password = get_password_hash(admin_password)
                db.commit()
                result["action"] = "password_reset"
                result["message"] = "Hash du mot de passe réinitialisé"
            else:
                result["action"] = "ok"
                result["message"] = "Compte admin valide"
        
        return result
    except Exception as e:
        db.rollback()
        return {"error": str(e), "traceback": str(e.__traceback__)}
    finally:
        db.close()
