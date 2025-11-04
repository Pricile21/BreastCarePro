"""
Script pour initialiser la base de données SQLite et charger les centres
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.user import User
from app.models.patient import Patient
from app.models.mammography import MammographyAnalysis
from app.models.professional import Professional
from app.models.access_request import AccessRequest
from app.models.healthcare_center import HealthcareCenter
from app.core.security import get_password_hash

# Database URL (SQLite)
DATABASE_URL = "sqlite:///./breastcare.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables
print("🏗️  Création des tables...")
Base.metadata.create_all(bind=engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Create admin user
    admin_user = db.query(User).filter(User.email == "admin@breastcare.bj").first()
    if not admin_user:
        admin_user = User(
            id="admin-001",
            email="admin@breastcare.bj",
            full_name="Admin BreastCare",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_verified=True,
            user_type="admin"
        )
        db.add(admin_user)
        print("✅ Compte administrateur créé")
    
    db.commit()
    
    # Import and seed centers
    from app.db.seed_centers import seed_centers, BENIN_CENTERS
    print(f"\n📋 Chargement de {len(BENIN_CENTERS)} centres de santé...")
    seed_centers(db)
    
    print("\n✅ Base de données initialisée avec succès!")
    print(f"📊 {len(BENIN_CENTERS)} centres chargés")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()

