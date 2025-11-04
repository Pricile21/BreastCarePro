"""
Script pour créer un compte patient de test pour la plateforme mobile
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_test_patient():
    """Créer un compte patient de test"""
    db = SessionLocal()
    try:
        email = "patient@test.com"
        password = "test123"
        
        print("=" * 80)
        print("🏥 CRÉATION D'UN COMPTE PATIENT DE TEST")
        print("=" * 80)
        
        # Vérifier si le compte existe déjà
        existing = db.query(User).filter(User.email == email).first()
        
        if existing:
            print(f"⚠️  Le compte {email} existe déjà")
            print(f"📧 Email: {existing.email}")
            print(f"👤 Type: {existing.user_type}")
            print(f"✅ Statut: {'Actif' if existing.is_active else 'Inactif'}")
            
            # Réinitialiser le mot de passe
            existing.hashed_password = get_password_hash(password)
            existing.is_active = True
            db.commit()
            print(f"🔄 Mot de passe réinitialisé")
        else:
            # Créer le compte
            patient = User(
                id=f"patient-{email.split('@')[0]}",
                email=email,
                full_name="Patient Test",
                phone="+22912345678",
                hashed_password=get_password_hash(password),
                is_active=True,
                is_verified=False,
                user_type="patient"
            )
            db.add(patient)
            db.commit()
            print(f"✅ Compte patient créé avec succès")
        
        print(f"\n📋 INFORMATIONS DE CONNEXION:")
        print(f"📧 Email: {email}")
        print(f"🔑 Mot de passe: {password}")
        print(f"🌐 Plateforme: /mobile/login")
        print("\n" + "=" * 80)
        print("✅ VOUS POUVEZ MAINTENANT VOUS CONNECTER SUR /mobile/login")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_patient()

