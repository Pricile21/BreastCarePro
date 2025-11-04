#!/usr/bin/env python3
"""
Script pour démarrer les serveurs backend et frontend
"""

import subprocess
import time
import sys
import os
import signal
import threading

def start_backend():
    """Démarrer le serveur backend"""
    print("🚀 Démarrage du serveur backend...")
    os.chdir("backend")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur backend")
    except Exception as e:
        print(f"❌ Erreur backend: {e}")

def start_frontend():
    """Démarrer le serveur frontend"""
    print("🚀 Démarrage du serveur frontend...")
    os.chdir("frontend")
    try:
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur frontend")
    except Exception as e:
        print(f"❌ Erreur frontend: {e}")

def main():
    """Fonction principale"""
    print("🏥 BREASTCARE BENIN - DÉMARRAGE DES SERVEURS")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Erreur: Ce script doit être exécuté depuis la racine du projet")
        sys.exit(1)
    
    print("📋 Instructions:")
    print("1. Le backend démarrera sur http://localhost:8000")
    print("2. Le frontend démarrera sur http://localhost:3000")
    print("3. Appuyez sur Ctrl+C pour arrêter les serveurs")
    print()
    
    try:
        # Démarrer le backend dans un thread séparé
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # Attendre un peu que le backend démarre
        print("⏳ Attente du démarrage du backend...")
        time.sleep(5)
        
        # Démarrer le frontend
        start_frontend()
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt des serveurs")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
