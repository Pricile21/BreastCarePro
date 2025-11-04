#!/usr/bin/env python3
"""
Diagnostic approfondi du problème d'accès aux rapports
"""

import requests
import json
import sqlite3
import os
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
TEST_EMAIL = "pricilegangbe@gmail.com"
TEST_PASSWORD = "Pricile18"

def check_database_state():
    """Vérifier l'état de la base de données"""
    print("🔍 VÉRIFICATION DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    db_path = "backend/breastcare.db"
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier l'utilisateur
        cursor.execute("""
            SELECT id, email, full_name, professional_id, user_type, is_active 
            FROM users WHERE email = ?
        """, (TEST_EMAIL,))
        user = cursor.fetchone()
        
        if user:
            print(f"✅ Utilisateur trouvé:")
            print(f"   - ID: {user[0]}")
            print(f"   - Email: {user[1]}")
            print(f"   - Nom: {user[2]}")
            print(f"   - Professional ID: {user[3]}")
            print(f"   - Type: {user[4]}")
            print(f"   - Actif: {user[5]}")
        else:
            print("❌ Utilisateur non trouvé")
            return False
        
        # Vérifier le professionnel
        if user[3]:  # Si professional_id existe
            cursor.execute("""
                SELECT id, full_name, specialty, email, is_active 
                FROM professionals WHERE id = ?
            """, (user[3],))
            professional = cursor.fetchone()
            
            if professional:
                print(f"✅ Professionnel associé trouvé:")
                print(f"   - ID: {professional[0]}")
                print(f"   - Nom: {professional[1]}")
                print(f"   - Spécialité: {professional[2]}")
                print(f"   - Email: {professional[3]}")
                print(f"   - Actif: {professional[4]}")
            else:
                print("❌ Professionnel associé non trouvé")
                return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def test_authentication():
    """Tester l'authentification complète"""
    print("\n🔍 TEST D'AUTHENTIFICATION COMPLET")
    print("=" * 50)
    
    try:
        # 1. Connexion
        login_data = {"username": TEST_EMAIL, "password": TEST_PASSWORD}
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        
        if response.status_code != 200:
            print(f"❌ Erreur de connexion: {response.status_code} - {response.text}")
            return None
        
        token = response.json().get("access_token")
        print(f"✅ Connexion réussie - Token: {token[:20]}...")
        
        # 2. Vérifier le profil utilisateur
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Erreur profil utilisateur: {response.status_code} - {response.text}")
            return None
        
        user_data = response.json()
        print(f"✅ Profil utilisateur récupéré:")
        print(f"   - Email: {user_data.get('email')}")
        print(f"   - Type: {user_data.get('user_type')}")
        print(f"   - Professional ID: {user_data.get('professional_id')}")
        
        return token, user_data
        
    except Exception as e:
        print(f"❌ Erreur authentification: {e}")
        return None

def test_professional_endpoints(token):
    """Tester tous les endpoints professionnels"""
    print("\n🔍 TEST DES ENDPOINTS PROFESSIONNELS")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        ("/professionals/me", "Profil professionnel"),
        ("/professionals/dashboard/stats", "Statistiques dashboard"),
        ("/professionals/dashboard/analyses", "Analyses récentes"),
        ("/professionals/dashboard/alerts", "Alertes"),
        ("/professionals/reports", "Rapports")
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        try:
            print(f"\n📡 Test: {description}")
            response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Succès - Données: {len(str(data))} caractères")
                results[endpoint] = {"status": "success", "data": data}
            else:
                error_text = response.text
                print(f"   ❌ Erreur: {error_text}")
                results[endpoint] = {"status": "error", "error": error_text}
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
            results[endpoint] = {"status": "exception", "error": str(e)}
    
    return results

def analyze_reports_error(results):
    """Analyser l'erreur spécifique des rapports"""
    print("\n🔍 ANALYSE DE L'ERREUR RAPPORTS")
    print("=" * 50)
    
    reports_result = results.get("/professionals/reports")
    if not reports_result:
        print("❌ Aucun résultat pour les rapports")
        return
    
    if reports_result["status"] == "error":
        error_text = reports_result["error"]
        print(f"❌ Erreur rapports: {error_text}")
        
        # Analyser l'erreur
        if "Professional not found" in error_text:
            print("\n🔍 DIAGNOSTIC: 'Professional not found'")
            print("   - L'utilisateur n'est pas reconnu comme professionnel")
            print("   - Vérifiez que professional_id est correct dans la base")
            print("   - Vérifiez que le serveur backend a été redémarré")
        elif "Access denied" in error_text:
            print("\n🔍 DIAGNOSTIC: 'Access denied'")
            print("   - L'utilisateur n'a pas les permissions")
            print("   - Vérifiez le type d'utilisateur")
        else:
            print(f"\n🔍 DIAGNOSTIC: Erreur inconnue - {error_text}")
    else:
        print("✅ Les rapports fonctionnent correctement")

def check_backend_logs():
    """Vérifier les logs du backend"""
    print("\n🔍 VÉRIFICATION DES LOGS BACKEND")
    print("=" * 50)
    
    # Vérifier si le backend répond
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend accessible")
            print(f"   Réponse: {response.json()}")
        else:
            print(f"❌ Backend répond mais avec erreur: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Backend non accessible - Vérifiez qu'il est démarré")
    except Exception as e:
        print(f"❌ Erreur de connexion au backend: {e}")

def main():
    """Fonction principale de diagnostic"""
    print("🏥 BREASTCARE BENIN - DIAGNOSTIC APPROFONDI")
    print("=" * 60)
    print(f"🕐 Diagnostic démarré à: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Vérifier la base de données
    if not check_database_state():
        print("\n❌ PROBLÈME: Base de données incorrecte")
        return
    
    # 2. Vérifier le backend
    check_backend_logs()
    
    # 3. Tester l'authentification
    auth_result = test_authentication()
    if not auth_result:
        print("\n❌ PROBLÈME: Authentification échouée")
        return
    
    token, user_data = auth_result
    
    # 4. Tester les endpoints professionnels
    results = test_professional_endpoints(token)
    
    # 5. Analyser l'erreur des rapports
    analyze_reports_error(results)
    
    # 6. Résumé
    print("\n📊 RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 30)
    
    success_count = sum(1 for r in results.values() if r["status"] == "success")
    total_count = len(results)
    
    print(f"Endpoints fonctionnels: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("✅ Tous les endpoints fonctionnent")
    else:
        print("❌ Certains endpoints ont des problèmes")
        
        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        if results.get("/professionals/reports", {}).get("status") == "error":
            print("1. Redémarrez le serveur backend")
            print("2. Vérifiez que la base de données est correcte")
            print("3. Vérifiez les logs du backend pour plus de détails")

if __name__ == "__main__":
    main()
