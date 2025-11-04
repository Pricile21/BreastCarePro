#!/usr/bin/env python3
"""
Script pour créer des analyses de test
"""

import sqlite3
import uuid
from datetime import datetime, timedelta

def create_test_analyses():
    """Créer des analyses de test pour l'utilisateur"""
    print("🔧 CRÉATION D'ANALYSES DE TEST")
    print("=" * 50)
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('backend/breastcare.db')
        cursor = conn.cursor()
        
        # 1. Vérifier l'utilisateur
        print("1️⃣ Vérification de l'utilisateur...")
        cursor.execute("SELECT id, email, professional_id, user_type FROM users WHERE email = ?", ('pricilegangbe@gmail.com',))
        user = cursor.fetchone()
        if not user:
            print("❌ Utilisateur non trouvé")
            return False
        
        user_id, email, professional_id, user_type = user
        print(f"✅ Utilisateur trouvé: {user_id}")
        
        # 2. Créer des analyses de test
        print("\n2️⃣ Création d'analyses de test...")
        
        analyses_data = [
            {
                'id': str(uuid.uuid4()),
                'analysis_id': f'ANALYSIS-{datetime.now().strftime("%Y%m%d")}-001',
                'user_id': user_id,
                'patient_id': f'PAT-{datetime.now().strftime("%Y%m%d")}-001',
                'bi_rads_category': 'BI-RADS 2',
                'confidence_score': 0.85,
                'breast_density': 'Dense',
                'findings': 'Aucune anomalie détectée',
                'recommendations': 'Contrôle de routine dans 2 ans',
                'status': 'COMPLETED',
                'created_at': datetime.now() - timedelta(days=1),
                'updated_at': datetime.now() - timedelta(days=1)
            },
            {
                'id': str(uuid.uuid4()),
                'analysis_id': f'ANALYSIS-{datetime.now().strftime("%Y%m%d")}-002',
                'user_id': user_id,
                'patient_id': f'PAT-{datetime.now().strftime("%Y%m%d")}-002',
                'bi_rads_category': 'BI-RADS 3',
                'confidence_score': 0.72,
                'breast_density': 'Heterogeneously dense',
                'findings': 'Opacité suspecte nécessitant un suivi',
                'recommendations': 'Contrôle dans 6 mois',
                'status': 'PENDING',
                'created_at': datetime.now() - timedelta(hours=6),
                'updated_at': datetime.now() - timedelta(hours=6)
            },
            {
                'id': str(uuid.uuid4()),
                'analysis_id': f'ANALYSIS-{datetime.now().strftime("%Y%m%d")}-003',
                'user_id': user_id,
                'patient_id': f'PAT-{datetime.now().strftime("%Y%m%d")}-003',
                'bi_rads_category': 'BI-RADS 4',
                'confidence_score': 0.68,
                'breast_density': 'Extremely dense',
                'findings': 'Anomalie suspecte nécessitant une biopsie',
                'recommendations': 'Biopsie recommandée',
                'status': 'COMPLETED',
                'created_at': datetime.now() - timedelta(hours=2),
                'updated_at': datetime.now() - timedelta(hours=2)
            }
        ]
        
        for analysis in analyses_data:
            cursor.execute("""
                INSERT INTO mammography_analyses 
                (id, analysis_id, user_id, patient_id, bi_rads_category, confidence_score, 
                 breast_density, findings, recommendations, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis['id'], analysis['analysis_id'], analysis['user_id'], analysis['patient_id'],
                analysis['bi_rads_category'], analysis['confidence_score'],
                analysis['breast_density'], analysis['findings'], analysis['recommendations'],
                analysis['status'], analysis['created_at'], analysis['updated_at']
            ))
            print(f"  ✅ Analyse créée: {analysis['id']}")
        
        conn.commit()
        
        # 3. Vérifier les analyses créées
        print("\n3️⃣ Vérification des analyses créées...")
        cursor.execute("SELECT COUNT(*) FROM mammography_analyses WHERE user_id = ?", (user_id,))
        count = cursor.fetchone()[0]
        print(f"✅ {count} analyses créées pour l'utilisateur {user_id}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    create_test_analyses()
