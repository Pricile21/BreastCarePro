#!/usr/bin/env python3
"""
Script pour déboguer le problème des rapports
"""

import requests
import json

API_BASE_URL = "http://localhost:8000/api/v1"
TEST_EMAIL = "pricilegangbe@gmail.com"
TEST_PASSWORD = "Pricile18"

def debug_reports():
    """Déboguer l'endpoint des rapports"""
    print("🔍 DEBUG - Endpoint des rapports")
    print("=" * 50)
    
    try:
        # 1. Connexion
        print("1️⃣ Connexion...")
        login_data = {"username": TEST_EMAIL, "password": TEST_PASSWORD}
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        
        if response.status_code != 200:
            print(f"❌ Erreur connexion: {response.text}")
            return False
        
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Connexion réussie")
        
        # 2. Vérifier l'utilisateur actuel
        print("\n2️⃣ Vérification de l'utilisateur actuel...")
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"User ID: {user_data.get('id')}")
            print(f"Email: {user_data.get('email')}")
            print(f"Professional ID: {user_data.get('professional_id')}")
            print(f"User Type: {user_data.get('user_type')}")
        
        # 3. Test de l'endpoint /professionals/me
        print("\n3️⃣ Test de l'endpoint /professionals/me...")
        response = requests.get(f"{API_BASE_URL}/professionals/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        # 4. Test de l'endpoint des rapports
        print("\n4️⃣ Test de l'endpoint /professionals/reports...")
        response = requests.get(f"{API_BASE_URL}/professionals/reports", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.status_code == 200
            
    except Exception as e:
        print(f"❌ Erreur debug: {e}")
        return False

if __name__ == "__main__":
    debug_reports()
