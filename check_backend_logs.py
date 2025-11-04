#!/usr/bin/env python3
"""
Script pour vérifier les logs du backend
"""

import subprocess
import time
import requests

API_BASE_URL = "http://localhost:8000/api/v1"
TEST_EMAIL = "pricilegangbe@gmail.com"
TEST_PASSWORD = "Pricile18"

def check_backend_logs():
    """Vérifier les logs du backend"""
    print("🔍 VÉRIFICATION DES LOGS DU BACKEND")
    print("=" * 50)
    
    # Test de l'endpoint des rapports
    print("\n📡 Envoi de la requête à l'endpoint /professionals/reports...")
    
    try:
        # Connexion
        login_data = {"username": TEST_EMAIL, "password": TEST_PASSWORD}
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        
        if response.status_code != 200:
            print(f"❌ Erreur connexion: {response.text}")
            return False
        
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Connexion réussie")
        
        # Test de l'endpoint des rapports
        print("\n📡 Appel de l'endpoint /professionals/reports...")
        response = requests.get(f"{API_BASE_URL}/professionals/reports", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        print("\n💡 Vérifiez les logs du backend dans la console où le serveur tourne.")
        print("   Les logs devraient afficher:")
        print("   - 🔍 Endpoint reports appelé pour user: pricilegangbe@gmail.com")
        print("   - 🔧 Association de l'utilisateur... ou ✅ Utilisateur déjà associé...")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    check_backend_logs()
