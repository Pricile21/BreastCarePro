"""
Script pour nettoyer et peupler la base de données avec de vraies données de patients
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import date
import os

# Configuration de la base de données
DATABASE_URL = "sqlite:///./breast_cancer.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def clean_and_populate_database():
    """
    Nettoie la base de données et ajoute de vraies données de patients
    """
    db = SessionLocal()
    
    try:
        # Nettoyer la table des patients
        print("🧹 Nettoyage de la base de données...")
        db.execute(text("DELETE FROM patients"))
        db.execute(text("DELETE FROM mammography_analyses"))
        db.execute(text("DELETE FROM users WHERE email != 'pricilegangbe@gmail.com'"))
        
        # Ajouter de vraies données de patients
        print("📝 Ajout des vraies données de patients...")
        
        patients_data = [
            {
                "user_id": "1",  # ID de l'utilisateur Dr GANGBE Pricile
                "patient_id": "P-2024-0001",
                "full_name": "Marie KOUASSI",
                "date_of_birth": date(1979, 3, 15),
                "age": 45,
                "phone_number": "+229 97 12 34 56",
                "address": "Quartier Cotonou, Cotonou, Bénin",
                "emergency_contact": "+229 97 12 34 57",
                "medical_history": "Antécédents familiaux de cancer du sein",
                "family_history": "Mère décédée d'un cancer du sein à 65 ans",
                "notes": "Patient régulière, très coopérative"
            },
            {
                "user_id": "1",
                "patient_id": "P-2024-0002",
                "full_name": "Fatou TRAORE",
                "date_of_birth": date(1972, 7, 22),
                "age": 52,
                "phone_number": "+229 97 23 45 67",
                "address": "Porto-Novo, Bénin",
                "emergency_contact": "+229 97 23 45 68",
                "medical_history": "Hypertension artérielle, diabète type 2",
                "family_history": "Sœur avec cancer du sein diagnostiqué à 48 ans",
                "notes": "Surveillance renforcée recommandée"
            },
            {
                "user_id": "1",
                "patient_id": "P-2024-0003",
                "full_name": "Aminata DIALLO",
                "date_of_birth": date(1986, 11, 8),
                "age": 38,
                "phone_number": "+229 97 34 56 78",
                "address": "Abomey-Calavi, Bénin",
                "emergency_contact": "+229 97 34 56 79",
                "medical_history": "Aucun antécédent médical significatif",
                "family_history": "Aucun antécédent familial de cancer",
                "notes": "Première mammographie de dépistage"
            },
            {
                "user_id": "1",
                "patient_id": "P-2024-0004",
                "full_name": "Grace ADJOVI",
                "date_of_birth": date(1975, 5, 30),
                "age": 49,
                "phone_number": "+229 97 45 67 89",
                "address": "Parakou, Bénin",
                "emergency_contact": "+229 97 45 67 90",
                "medical_history": "Fibromes utérins, traitement hormonal",
                "family_history": "Grand-mère maternelle avec cancer du sein",
                "notes": "Surveillance régulière nécessaire"
            },
            {
                "user_id": "1",
                "patient_id": "P-2024-0005",
                "full_name": "Claire ZINSOU",
                "date_of_birth": date(1983, 9, 12),
                "age": 41,
                "phone_number": "+229 97 56 78 90",
                "address": "Natitingou, Bénin",
                "emergency_contact": "+229 97 56 78 91",
                "medical_history": "Asthme léger",
                "family_history": "Aucun antécédent familial de cancer",
                "notes": "Patient jeune, dépistage précoce"
            }
        ]
        
        # Insérer les données
        for patient_data in patients_data:
            db.execute(text("""
                INSERT INTO patients (
                    user_id, patient_id, full_name, date_of_birth, age,
                    phone_number, address, emergency_contact, medical_history,
                    family_history, notes, created_at, updated_at
                ) VALUES (
                    :user_id, :patient_id, :full_name, :date_of_birth, :age,
                    :phone_number, :address, :emergency_contact, :medical_history,
                    :family_history, :notes, datetime('now'), datetime('now')
                )
            """), patient_data)
        
        db.commit()
        print("✅ Base de données nettoyée et peuplée avec succès!")
        print(f"📊 {len(patients_data)} patients ajoutés")
        
        # Vérifier les données
        result = db.execute(text("SELECT COUNT(*) FROM patients")).scalar()
        print(f"🔍 Nombre total de patients dans la DB: {result}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_and_populate_database()
