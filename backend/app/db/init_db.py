"""
Initialize database with tables and initial data
"""

from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import text

from app.db.session import SessionLocal
from app.models.base import Base
from app.models.user import User
from app.models.patient import Patient
from app.models.mammography import MammographyAnalysis
from app.models.professional import Professional
from app.models.access_request import AccessRequest
from app.models.healthcare_center import HealthcareCenter  # Add healthcare center model
from app.core.security import get_password_hash


def init_db(db: Session) -> None:
    """
    Initialize database with initial data (compte admin)
    Note: Les tables sont déjà créées par main.py, on ne fait que les données initiales
    """
    # Créer l'administrateur par défaut
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
        db.commit()
        print("✅ Compte administrateur créé automatiquement")
        print("📧 Email: admin@breastcare.bj")
        print("🔑 Mot de passe: admin123")
    else:
        print("✅ Compte administrateur existe déjà")


def migrate_sqlite_schema(engine: Engine) -> None:
    """
    Perform lightweight, idempotent schema adjustments for SQLite.
    Currently ensures `users.phone` column exists.
    """
    try:
        # Skip migration if using PostgreSQL
        if not engine.url.drivername.startswith("sqlite"):
            print(f"📊 Utilisation de {engine.url.drivername}, pas de migration SQLite nécessaire")
            return
            
        with engine.connect() as connection:
            # Check if users table exists
            tables = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
            if not list(tables):
                return  # Nothing to migrate yet

            # Inspect existing columns
            pragma_result = connection.execute(text("PRAGMA table_info(users)"))
            existing_columns = {row[1] for row in pragma_result}

            if "phone" not in existing_columns:
                connection.execute(text("ALTER TABLE users ADD COLUMN phone TEXT"))
    except Exception as e:
        # Do not crash startup on migration attempt; log to stdout
        print(f"⚠️  SQLite migration warning: {e}")


if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
    db.close()
