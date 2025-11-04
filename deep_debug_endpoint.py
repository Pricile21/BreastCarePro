#!/usr/bin/env python3
"""
Script de diagnostic approfondi pour comprendre le problème
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000/api/v1"
TEST_EMAIL = "pricilegangbe@gmail.com"
TEST_PASSWORD = "Pricile18"

def test_all_endpoints():
    """Tester tous les endpoints pour comprendre le problème"""
    print("🔍 DIAGNOSTIC APPROFONDI")
    print("=" * 60)
    
    try:
        # 1. Connexion
        print("1️⃣ Connexion...")
        login_data = {"username": TEST_EMAIL, "password": TEST_PASSWORD}
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        
        if response.status_code != 200:
            print(f"❌ Erreur connexion: {response.text}")
            return
        
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Connexion réussie")
        
        # 2. Test de l'endpoint /auth/me
        print("\n2️⃣ Test /auth/me...")
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"   - Email: {user_data.get('email')}")
            print(f"   - Type: {user_data.get('user_type')}")
            print(f"   - Professional ID: {user_data.get('professional_id')}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # 3. Test de l'endpoint /professionals/me
        print("\n3️⃣ Test /professionals/me...")
        response = requests.get(f"{API_BASE_URL}/professionals/me", headers=headers)
        if response.status_code == 200:
            prof_data = response.json()
            print(f"   - Nom: {prof_data.get('full_name')}")
            print(f"   - ID: {prof_data.get('id')}")
            print(f"   - Email: {prof_data.get('email')}")
            print(f"   - Spécialité: {prof_data.get('specialty')}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # 4. Test de l'endpoint /professionals/reports
        print("\n4️⃣ Test /professionals/reports...")
        print("   📋 Regardez les logs du backend pour les messages de debug")
        response = requests.get(f"{API_BASE_URL}/professionals/reports", headers=headers)
        print(f"   📊 Status: {response.status_code}")
        print(f"   📄 Réponse: {response.text}")
        
        # 5. Test de l'endpoint /professionals/dashboard
        print("\n5️⃣ Test /professionals/dashboard...")
        response = requests.get(f"{API_BASE_URL}/professionals/dashboard", headers=headers)
        print(f"   📊 Status: {response.status_code}")
        if response.status_code == 200:
            dashboard_data = response.json()
            print(f"   - Stats: {dashboard_data.get('stats', {})}")
        else:
            print(f"   📄 Réponse: {response.text}")
        
        # 6. Test de l'endpoint /professionals/analyses
        print("\n6️⃣ Test /professionals/analyses...")
        response = requests.get(f"{API_BASE_URL}/professionals/analyses", headers=headers)
        print(f"   📊 Status: {response.status_code}")
        if response.status_code == 200:
            analyses_data = response.json()
            print(f"   - Analyses: {len(analyses_data)} trouvées")
        else:
            print(f"   📄 Réponse: {response.text}")
        
        # 7. Test de l'endpoint /professionals/alerts
        print("\n7️⃣ Test /professionals/alerts...")
        response = requests.get(f"{API_BASE_URL}/professionals/alerts", headers=headers)
        print(f"   📊 Status: {response.status_code}")
        if response.status_code == 200:
            alerts_data = response.json()
            print(f"   - Alertes: {len(alerts_data)} trouvées")
        else:
            print(f"   📄 Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Fonction principale"""
    print("🏥 BREASTCARE BENIN - DIAGNOSTIC APPROFONDI")
    print("=" * 60)
    
    test_all_endpoints()
    
    print("\n📋 ANALYSE DES RÉSULTATS:")
    print("1. Si /auth/me retourne 'Professional ID: None' → Problème de session")
    print("2. Si /professionals/me fonctionne → Le professionnel existe")
    print("3. Si /professionals/reports échoue → Problème dans l'endpoint")
    print("4. Si /professionals/dashboard fonctionne → L'utilisateur est bien un professionnel")
    print("5. Regardez les logs du backend pour les messages de debug")

if __name__ == "__main__":
    main()
