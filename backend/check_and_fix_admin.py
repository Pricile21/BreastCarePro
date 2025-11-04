"""
Script pour vérifier et créer/corriger le compte admin
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash, verify_password

def check_and_fix_admin():
    """Vérifier et créer/corriger le compte admin"""
    db = SessionLocal()
    try:
        admin_email = "admin@breastcare.bj"
        admin_password = "admin123"
        
        print("=" * 80)
        print("🔍 VÉRIFICATION DU COMPTE ADMIN")
        print("=" * 80)
        
        # Chercher l'utilisateur admin
        admin_user = db.query(User).filter(User.email == admin_email).first()
        
        if not admin_user:
            print(f"❌ Compte admin NON TROUVÉ - Création...")
            
            # Créer le compte admin
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
            print(f"✅ Compte admin créé avec succès")
            print(f"📧 Email: {admin_email}")
            print(f"🔑 Mot de passe: {admin_password}")
        else:
            print(f"✅ Compte admin trouvé")
            print(f"📧 Email: {admin_user.email}")
            print(f"👤 ID: {admin_user.id}")
            print(f"📋 Type: {admin_user.user_type}")
            print(f"🔐 Hash actuel (preview): {admin_user.hashed_password[:20]}...")
            print(f"📏 Longueur hash: {len(admin_user.hashed_password)}")
            
            # Tester la vérification du mot de passe
            print(f"\n🧪 Test de vérification du mot de passe...")
            is_valid = verify_password(admin_password, admin_user.hashed_password)
            
            if not is_valid:
                print(f"❌ Le mot de passe actuel ne correspond PAS")
                print(f"🔄 Réinitialisation du hash du mot de passe...")
                
                # Réinitialiser le hash
                admin_user.hashed_password = get_password_hash(admin_password)
                db.commit()
                print(f"✅ Hash du mot de passe réinitialisé")
                
                # Re-tester
                is_valid = verify_password(admin_password, admin_user.hashed_password)
                if is_valid:
                    print(f"✅ Vérification réussie après réinitialisation")
                else:
                    print(f"❌ ERREUR: La vérification échoue encore après réinitialisation")
            else:
                print(f"✅ Le mot de passe est VALIDE")
        
        print("\n" + "=" * 80)
        print("✅ VÉRIFICATION TERMINÉE")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    check_and_fix_admin()

