"""
Script pour vérifier et créer/corriger le compte professionnel
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models.user import User
from app.models.professional import Professional
from app.models.access_request import AccessRequest
from app.core.security import get_password_hash, verify_password

def check_and_fix_professional():
    """Vérifier et créer/corriger le compte professionnel"""
    db = SessionLocal()
    try:
        email = "pricilegangbe@gmail.com"
        
        print("=" * 80)
        print("🔍 VÉRIFICATION DU COMPTE PROFESSIONNEL")
        print("=" * 80)
        
        # Chercher la demande d'accès
        access_request = db.query(AccessRequest).filter(AccessRequest.email == email).first()
        
        if access_request:
            print(f"✅ Demande d'accès trouvée:")
            print(f"   Status: {access_request.status}")
            print(f"   Email: {access_request.email}")
            print(f"   Nom: {access_request.full_name}")
            print(f"   Password hash preview: {access_request.password[:30] if access_request.password else 'None'}...")
        else:
            print(f"❌ Aucune demande d'accès trouvée pour {email}")
        
        # Chercher l'utilisateur
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            print(f"\n✅ Utilisateur trouvé:")
            print(f"   ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Type: {user.user_type}")
            print(f"   Actif: {user.is_active}")
            print(f"   Vérifié: {user.is_verified}")
            print(f"   Password hash preview: {user.hashed_password[:30] if user.hashed_password else 'None'}...")
        else:
            print(f"\n❌ Aucun utilisateur trouvé pour {email}")
        
        # Chercher le professionnel
        professional = db.query(Professional).filter(Professional.email == email).first()
        
        if professional:
            print(f"\n✅ Professionnel trouvé:")
            print(f"   ID: {professional.id}")
            print(f"   Nom: {professional.full_name}")
            print(f"   Spécialité: {professional.specialty}")
        else:
            print(f"\n❌ Aucun professionnel trouvé pour {email}")
        
        print("\n" + "=" * 80)
        print("✅ VÉRIFICATION TERMINÉE")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_and_fix_professional()

