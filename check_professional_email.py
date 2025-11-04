#!/usr/bin/env python3
"""
Script pour vérifier l'email du professionnel dans la base de données
"""

import sqlite3
import os

def check_professional_email():
    """Vérifier l'email du professionnel dans la base de données"""
    print("🔍 VÉRIFICATION DE L'EMAIL DU PROFESSIONNEL")
    print("=" * 60)
    
    # Chercher la base de données dans le répertoire backend
    backend_dir = "backend"
    db_files = []
    
    for file in os.listdir(backend_dir):
        if file.endswith('.db') or (os.path.isfile(os.path.join(backend_dir, file)) and not file.endswith('.py')):
            db_files.append(os.path.join(backend_dir, file))
    
    if not db_files:
        print(f"❌ Aucune base de données trouvée dans {backend_dir}")
        return
    
    print(f"📁 Fichiers trouvés: {db_files}")
    
    # Utiliser le premier fichier trouvé
    db_path = db_files[0]
    print(f"🔍 Utilisation de: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la table professionals
        print("1️⃣ Vérification de la table professionals...")
        cursor.execute("SELECT id, full_name, email, specialty FROM professionals")
        professionals = cursor.fetchall()
        
        print(f"   📊 {len(professionals)} professionnels trouvés:")
        for prof in professionals:
            print(f"   - ID: {prof[0]}")
            print(f"   - Nom: {prof[1]}")
            print(f"   - Email: {prof[2]}")
            print(f"   - Spécialité: {prof[3]}")
            print()
        
        # Vérifier la table users
        print("2️⃣ Vérification de la table users...")
        cursor.execute("SELECT id, email, full_name, user_type, professional_id FROM users WHERE email = 'pricilegangbe@gmail.com'")
        users = cursor.fetchall()
        
        print(f"   📊 {len(users)} utilisateurs trouvés:")
        for user in users:
            print(f"   - ID: {user[0]}")
            print(f"   - Email: {user[1]}")
            print(f"   - Nom: {user[2]}")
            print(f"   - Type: {user[3]}")
            print(f"   - Professional ID: {user[4]}")
            print()
        
        # Vérifier la correspondance email
        print("3️⃣ Vérification de la correspondance email...")
        cursor.execute("""
            SELECT p.id, p.full_name, p.email, u.id as user_id, u.email as user_email
            FROM professionals p
            JOIN users u ON p.email = u.email
            WHERE u.email = 'pricilegangbe@gmail.com'
        """)
        matches = cursor.fetchall()
        
        if matches:
            print(f"   ✅ {len(matches)} correspondances trouvées:")
            for match in matches:
                print(f"   - Professional ID: {match[0]}")
                print(f"   - Professional Nom: {match[1]}")
                print(f"   - Professional Email: {match[2]}")
                print(f"   - User ID: {match[3]}")
                print(f"   - User Email: {match[4]}")
        else:
            print("   ❌ Aucune correspondance trouvée")
            print("   🔍 Vérification des emails individuels...")
            
            cursor.execute("SELECT email FROM professionals")
            prof_emails = [row[0] for row in cursor.fetchall()]
            print(f"   📧 Emails professionnels: {prof_emails}")
            
            cursor.execute("SELECT email FROM users WHERE email = 'pricilegangbe@gmail.com'")
            user_emails = [row[0] for row in cursor.fetchall()]
            print(f"   📧 Emails utilisateurs: {user_emails}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    """Fonction principale"""
    print("🏥 BREASTCARE BENIN - VÉRIFICATION EMAIL PROFESSIONNEL")
    print("=" * 60)
    
    check_professional_email()

if __name__ == "__main__":
    main()
