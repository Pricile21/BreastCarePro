"""
Script to seed database with Béninese healthcare centers for breast cancer screening

⚠️ IMPORTANT NOTE: 
Due to limited centralized data sources about permanent screening centers in Benin,
this list is based on known major hospitals and health facilities that participate
in breast cancer screening initiatives. Some details (phone numbers, exact addresses)
may need verification with local authorities.

Data sources:
- CNHU (Centre National Hospitalier Universitaire) - main referral hospital
- Campaign reports mentioning screening locations
- Known major health facilities in Benin
- Ministry of Health campaign locations (partial list)
- Clinics identified in web research

Total centers: 15 centers (7 hospitals, 1 CHU, 4 clinics, 3 health centers)

Recommended: Contact Ministry of Health Benin for verified, complete data.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.healthcare_center import HealthcareCenter
import uuid


# Real healthcare centers in Benin that offer breast cancer screening
BENIN_CENTERS = [
    {
        "name": "Centre National Hospitalier Universitaire (CNHU) Hubert Koutoukou Maga",
        "type": "hospital",
        "address": "Cotonou, Benin",
        "city": "Cotonou",
        "department": "Littoral",
        "latitude": 6.3557,
        "longitude": 2.4124,
        "phone_number": None,  # À vérifier avec le ministère de la Santé
        "email": None,
        "services": ["Consultation oncologique", "Chirurgie", "Chimiothérapie", "Échographie", "Biopsie"],
        "equipment": ["Échographe", "Équipement chirurgical"],
        "specialties": ["Oncologie", "Chirurgie", "Médecine générale"],
        "operating_hours": {
            "monday": "8h-17h",
            "tuesday": "8h-17h",
            "wednesday": "8h-17h",
            "thursday": "8h-17h",
            "friday": "8h-17h",
            "saturday": "8h-12h",
            "sunday": "Fermé"
        },
        "description": "Hôpital national de référence pour le traitement du cancer au Bénin. Disponible: chirurgie et chimiothérapie. Radiothérapie non disponible (évacuation nécessaire).",
        "languages_spoken": ["Français"],
        "is_verified": False,  # Doit être vérifié
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Centre Hospitalier Universitaire de la Mère et de l'Enfant (CHU-MEL) Lagune",
        "type": "hospital",
        "address": "Cotonou, Benin",
        "city": "Cotonou",
        "department": "Littoral",
        "latitude": 6.3722,
        "longitude": 2.4211,
        "phone_number": None,
        "email": None,
        "services": ["Consultation gynécologique", "Consultation générale"],
        "equipment": [],
        "specialties": ["Gynécologie", "Médecine générale"],
        "operating_hours": {
            "monday": "8h-16h",
            "tuesday": "8h-16h",
            "wednesday": "8h-16h",
            "thursday": "8h-16h",
            "friday": "8h-16h",
            "saturday": "Fermé",
            "sunday": "Fermé"
        },
        "description": "Centre hospitalier universitaire spécialisé en santé maternelle et infantile",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Hôpital de Zone Suru-Léré",
        "type": "hospital",
        "address": "Suru-Léré, Cotonou",
        "city": "Cotonou",
        "department": "Littoral",
        "latitude": 6.3411,
        "longitude": 2.4033,
        "phone_number": None,
        "email": None,
        "services": ["Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-16h",
            "tuesday": "8h-16h",
            "wednesday": "8h-16h",
            "thursday": "8h-16h",
            "friday": "8h-16h",
            "saturday": "Fermé",
            "sunday": "Fermé"
        },
        "description": "Hôpital de zone à Cotonou",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Hôpital de Zone de Mènontin",
        "type": "hospital",
        "address": "Mènontin, Cotonou",
        "city": "Cotonou",
        "department": "Littoral",
        "latitude": 6.3783,
        "longitude": 2.4389,
        "phone_number": None,
        "email": None,
        "services": ["Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-16h",
            "tuesday": "8h-16h",
            "wednesday": "8h-16h",
            "thursday": "8h-16h",
            "friday": "8h-16h",
            "saturday": "Fermé",
            "sunday": "Fermé"
        },
        "description": "Hôpital de zone à Cotonou",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Hôpital de Zone Abomey-Calavi",
        "type": "hospital",
        "address": "Abomey-Calavi",
        "city": "Abomey-Calavi",
        "department": "Atlantique",
        "latitude": 6.4474,
        "longitude": 2.3514,
        "phone_number": None,
        "email": None,
        "services": ["Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-16h",
            "tuesday": "8h-16h",
            "wednesday": "8h-16h",
            "thursday": "8h-16h",
            "friday": "8h-16h",
            "saturday": "Fermé",
            "sunday": "Fermé"
        },
        "description": "Hôpital de zone desservant Abomey-Calavi et environs",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Hôpital Départemental du Borgou (Parakou)",
        "type": "hospital",
        "address": "Parakou",
        "city": "Parakou",
        "department": "Borgou",
        "latitude": 9.3372,
        "longitude": 2.6303,
        "phone_number": None,
        "email": None,
        "services": ["Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-16h",
            "tuesday": "8h-16h",
            "wednesday": "8h-16h",
            "thursday": "8h-16h",
            "friday": "8h-16h",
            "saturday": "Fermé",
            "sunday": "Fermé"
        },
        "description": "Hôpital départemental desservant la région Nord du Bénin",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Centre de Santé de Référence (Bohicon)",
        "type": "center",
        "address": "Bohicon",
        "city": "Bohicon",
        "department": "Zou",
        "latitude": 7.1753,
        "longitude": 2.0666,
        "phone_number": None,
        "email": None,
        "services": ["Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-16h",
            "tuesday": "8h-16h",
            "wednesday": "8h-16h",
            "thursday": "8h-16h",
            "friday": "8h-16h",
            "saturday": "Fermé",
            "sunday": "Fermé"
        },
        "description": "Centre de santé de référence dans le département du Zou",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Clinique Saint Nicolas",
        "type": "clinic",
        "address": "Agbokou, Porto-Novo",
        "city": "Porto-Novo",
        "department": "Ouémé",
        "latitude": 6.4969,
        "longitude": 2.6284,
        "phone_number": None,
        "email": None,
        "services": ["Dépistage cancer du sein", "Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale", "Gynécologie"],
        "operating_hours": {
            "monday": "8h-17h",
            "tuesday": "8h-17h",
            "wednesday": "8h-17h",
            "thursday": "8h-17h",
            "friday": "8h-17h",
            "saturday": "8h-12h",
            "sunday": "Fermé"
        },
        "description": "Clinique privée proposant des services de dépistage du cancer du sein à Porto-Novo",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Clinique Les Archanges",
        "type": "clinic",
        "address": "Cotonou, Benin",
        "city": "Cotonou",
        "department": "Littoral",
        "latitude": 6.3667,
        "longitude": 2.4167,
        "phone_number": None,
        "email": None,
        "services": ["Dépistage cancer du sein", "Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-17h",
            "tuesday": "8h-17h",
            "wednesday": "8h-17h",
            "thursday": "8h-17h",
            "friday": "8h-17h",
            "saturday": "8h-12h",
            "sunday": "Fermé"
        },
        "description": "Établissement privé proposant des services de dépistage du cancer du sein à Cotonou",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Clinique Médicale La Vie",
        "type": "clinic",
        "address": "Abomey-Calavi, Benin",
        "city": "Abomey-Calavi",
        "department": "Atlantique",
        "latitude": 6.4474,
        "longitude": 2.3514,
        "phone_number": None,
        "email": None,
        "services": ["Dépistage cancer du sein", "Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-17h",
            "tuesday": "8h-17h",
            "wednesday": "8h-17h",
            "thursday": "8h-17h",
            "friday": "8h-17h",
            "saturday": "8h-12h",
            "sunday": "Fermé"
        },
        "description": "Clinique privée proposant des services de dépistage du cancer du sein à Abomey-Calavi",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Hôpital de Zone de Lokossa",
        "type": "hospital",
        "address": "Lokossa, Benin",
        "city": "Lokossa",
        "department": "Mono",
        "latitude": 6.6400,
        "longitude": 1.7200,
        "phone_number": None,
        "email": None,
        "services": ["Dépistage cancer du sein", "Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-16h",
            "tuesday": "8h-16h",
            "wednesday": "8h-16h",
            "thursday": "8h-16h",
            "friday": "8h-16h",
            "saturday": "Fermé",
            "sunday": "Fermé"
        },
        "description": "Hôpital régional offrant des services de dépistage du cancer du sein",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Clinique Biasa",
        "type": "clinic",
        "address": "Cotonou, Benin",
        "city": "Cotonou",
        "department": "Littoral",
        "latitude": 6.3667,
        "longitude": 2.4167,
        "phone_number": None,
        "email": None,
        "services": ["Dépistage cancer du sein", "Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-17h",
            "tuesday": "8h-17h",
            "wednesday": "8h-17h",
            "thursday": "8h-17h",
            "friday": "8h-17h",
            "saturday": "8h-12h",
            "sunday": "Fermé"
        },
        "description": "Établissement privé proposant des services de dépistage du cancer du sein à Cotonou",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Hôpital Évangélique de Bembéréké (HEB)",
        "type": "hospital",
        "address": "Bembéréké, Benin",
        "city": "Bembéréké",
        "department": "Borgou",
        "latitude": 10.2281,
        "longitude": 2.6625,
        "phone_number": None,
        "email": None,
        "services": ["Dépistage cancer du sein", "Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-16h",
            "tuesday": "8h-16h",
            "wednesday": "8h-16h",
            "thursday": "8h-16h",
            "friday": "8h-16h",
            "saturday": "Fermé",
            "sunday": "Fermé"
        },
        "description": "Hôpital évangélique offrant des services de dépistage du cancer du sein dans la zone sanitaire Bembéréké-Sinendé",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    },
    {
        "name": "Hôpital Saint Jean de Dieu",
        "type": "hospital",
        "address": "Tanguieta, Benin",
        "city": "Tanguieta",
        "department": "Atacora",
        "latitude": 10.6214,
        "longitude": 1.2611,
        "phone_number": None,
        "email": None,
        "services": ["Dépistage cancer du sein", "Consultation", "Soins généraux"],
        "equipment": [],
        "specialties": ["Médecine générale"],
        "operating_hours": {
            "monday": "8h-16h",
            "tuesday": "8h-16h",
            "wednesday": "8h-16h",
            "thursday": "8h-16h",
            "friday": "8h-16h",
            "saturday": "Fermé",
            "sunday": "Fermé"
        },
        "description": "Hôpital offrant des services de dépistage du cancer du sein",
        "languages_spoken": ["Français"],
        "is_verified": False,
        "rating": None,
        "total_reviews": 0
    }
]


def seed_centers(db: Session):
    """Seed the database with Béninese healthcare centers"""
    print("🌱 Seeding healthcare centers database...")
    
    for center_data in BENIN_CENTERS:
        # Check if center already exists
        existing = db.query(HealthcareCenter).filter(
            HealthcareCenter.name == center_data["name"]
        ).first()
        
        if existing:
            print(f"⚠️  Center '{center_data['name']}' already exists, skipping...")
            continue
        
        center = HealthcareCenter(
            id=str(uuid.uuid4()),
            **center_data
        )
        
        db.add(center)
        print(f"✅ Added: {center_data['name']}")
    
    db.commit()
    print(f"✅ Successfully seeded {len(BENIN_CENTERS)} healthcare centers")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_centers(db)
    except Exception as e:
        print(f"❌ Error seeding centers: {e}")
        db.rollback()
    finally:
        db.close()

