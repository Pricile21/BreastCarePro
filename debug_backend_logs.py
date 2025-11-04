#!/usr/bin/env python3
"""
Script pour déboguer les logs du backend et identifier le problème exact
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000/api/v1"
TEST_EMAIL = "pricilegangbe@gmail.com"
TEST_PASSWORD = "Pricile18"

def debug_reports_endpoint():
    """Déboguer l'endpoint des rapports avec logs détaillés"""
    print("🔍 DEBUG DE L'ENDPOINT RAPPORTS")
    print("=" * 50)
    
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
        
        # 2. Tester l'endpoint des rapports avec logs
        print("\n2️⃣ Test de l'endpoint /professionals/reports...")
        print("   (Les logs du backend devraient s'afficher dans le terminal du serveur)")
        
        response = requests.get(f"{API_BASE_URL}/professionals/reports", headers=headers)
        
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text}")
        
        if response.status_code == 200:
            reports = response.json()
            print(f"   ✅ Succès: {len(reports)} rapports")
        else:
            print(f"   ❌ Erreur: {response.text}")
            
            # Analyser l'erreur
            if "Professional not found" in response.text:
                print("\n🔍 ANALYSE DE L'ERREUR:")
                print("   - L'endpoint retourne 'Professional not found'")
                print("   - Cela signifie que le code backend n'a pas été mis à jour")
                print("   - OU que la session SQLAlchemy n'est pas synchronisée")
                print("   - Vérifiez les logs du backend dans le terminal du serveur")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_all_professional_endpoints():
    """Tester tous les endpoints professionnels pour identifier le problème"""
    print("\n🔍 TEST DE TOUS LES ENDPOINTS PROFESSIONNELS")
    print("=" * 50)
    
    try:
        # Connexion
        login_data = {"username": TEST_EMAIL, "password": TEST_PASSWORD}
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        
        if response.status_code != 200:
            print(f"❌ Erreur connexion: {response.text}")
            return
        
        token = response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Tester chaque endpoint
        endpoints = [
            ("/professionals/me", "Profil professionnel"),
            ("/professionals/dashboard/stats", "Statistiques"),
            ("/professionals/dashboard/analyses", "Analyses"),
            ("/professionals/dashboard/alerts", "Alertes"),
            ("/professionals/reports", "Rapports")
        ]
        
        for endpoint, description in endpoints:
            print(f"\n📡 {description}:")
            try:
                response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Succès")
                else:
                    print(f"   ❌ Erreur: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Exception: {e}")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")

def check_backend_code_changes():
    """Vérifier si les modifications du code backend sont actives"""
    print("\n🔍 VÉRIFICATION DES MODIFICATIONS BACKEND")
    print("=" * 50)
    
    # Vérifier si le fichier a été modifié récemment
    import os
    from datetime import datetime
    
    file_path = "backend/app/api/v1/endpoints/professionals.py"
    if os.path.exists(file_path):
        mod_time = os.path.getmtime(file_path)
        mod_date = datetime.fromtimestamp(mod_time)
        print(f"✅ Fichier backend modifié le: {mod_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Vérifier si le code contient nos modifications
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "fresh_user = db.query(User).filter(User.id == current_user.id).first()" in content:
            print("✅ Code modifié détecté dans le fichier")
        else:
            print("❌ Code modifié non détecté - Le serveur n'a peut-être pas redémarré")
    else:
        print("❌ Fichier backend non trouvé")

def main():
    """Fonction principale"""
    print("🏥 BREASTCARE BENIN - DEBUG BACKEND LOGS")
    print("=" * 60)
    
    # 1. Vérifier les modifications du code
    check_backend_code_changes()
    
    # 2. Tester tous les endpoints
    test_all_professional_endpoints()
    
    # 3. Déboguer l'endpoint des rapports
    debug_reports_endpoint()
    
    # 4. Recommandations
    print("\n💡 RECOMMANDATIONS:")
    print("1. Vérifiez les logs du backend dans le terminal du serveur")
    print("2. Si vous voyez les messages de debug (🔍, 🔧, ✅), le code est actif")
    print("3. Si vous ne voyez pas ces messages, le serveur n'a pas redémarré")
    print("4. Redémarrez le serveur backend si nécessaire")

if __name__ == "__main__":
    main()
