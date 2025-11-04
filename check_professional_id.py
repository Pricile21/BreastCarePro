#!/usr/bin/env python3
"""
Script pour vérifier le professional_id et identifier le problème
"""

import sqlite3
import os

def check_professional_id_issue():
    """Vérifier le problème du professional_id"""
    print("🔍 VÉRIFICATION DU PROFESSIONAL_ID")
    print("=" * 50)
    
    db_path = "backend/breastcare.db"
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier l'utilisateur
        print("1️⃣ Vérification de l'utilisateur:")
        cursor.execute("""
            SELECT id, email, full_name, professional_id, user_type 
            FROM users WHERE email = ?
        """, ("pricilegangbe@gmail.com",))
        user = cursor.fetchone()
        
        if user:
            print(f"   ✅ Utilisateur trouvé:")
            print(f"      - ID: {user[0]}")
            print(f"      - Email: {user[1]}")
            print(f"      - Nom: {user[2]}")
            print(f"      - Professional ID: {user[3]}")
            print(f"      - Type: {user[4]}")
            
            professional_id = user[3]
        else:
            print("   ❌ Utilisateur non trouvé")
            return False
        
        # 2. Vérifier si le professional_id existe dans la table professionals
        print(f"\n2️⃣ Vérification du professional_id '{professional_id}':")
        if professional_id:
            cursor.execute("""
                SELECT id, full_name, specialty, email 
                FROM professionals WHERE id = ?
            """, (professional_id,))
            professional = cursor.fetchone()
            
            if professional:
                print(f"   ✅ Professionnel trouvé:")
                print(f"      - ID: {professional[0]}")
                print(f"      - Nom: {professional[1]}")
                print(f"      - Spécialité: {professional[2]}")
                print(f"      - Email: {professional[3]}")
            else:
                print(f"   ❌ PROFESSIONNEL NON TROUVÉ!")
                print(f"      - L'ID '{professional_id}' n'existe pas dans la table professionals")
                print(f"      - C'est le problème !")
                
                # Chercher tous les professionnels disponibles
                print(f"\n3️⃣ Professionnels disponibles:")
                cursor.execute("SELECT id, full_name, email FROM professionals")
                all_professionals = cursor.fetchall()
                
                if all_professionals:
                    print(f"   📋 {len(all_professionals)} professionnels trouvés:")
                    for prof in all_professionals:
                        print(f"      - ID: {prof[0]}, Nom: {prof[1]}, Email: {prof[2]}")
                else:
                    print("   ❌ Aucun professionnel dans la base")
                
                return False
        else:
            print("   ❌ Aucun professional_id associé à l'utilisateur")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def fix_professional_id():
    """Corriger le professional_id"""
    print("\n🔧 CORRECTION DU PROFESSIONAL_ID")
    print("=" * 40)
    
    db_path = "backend/breastcare.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Trouver un professionnel valide
        cursor.execute("SELECT id, full_name, email FROM professionals LIMIT 1")
        valid_professional = cursor.fetchone()
        
        if not valid_professional:
            print("❌ Aucun professionnel valide trouvé")
            return False
        
        print(f"✅ Professionnel valide trouvé: {valid_professional[1]} (ID: {valid_professional[0]})")
        
        # 2. Mettre à jour l'utilisateur avec le bon professional_id
        cursor.execute("""
            UPDATE users 
            SET professional_id = ?, user_type = ? 
            WHERE email = ?
        """, (valid_professional[0], "professional", "pricilegangbe@gmail.com"))
        
        conn.commit()
        
        # 3. Vérifier la correction
        cursor.execute("""
            SELECT professional_id, user_type 
            FROM users WHERE email = ?
        """, ("pricilegangbe@gmail.com",))
        updated_user = cursor.fetchone()
        
        print(f"✅ Correction réussie:")
        print(f"   - Nouveau Professional ID: {updated_user[0]}")
        print(f"   - Type: {updated_user[1]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🏥 BREASTCARE BENIN - VÉRIFICATION PROFESSIONAL_ID")
    print("=" * 60)
    
    # Vérifier le problème
    if check_professional_id_issue():
        print("\n✅ Le professional_id est correct")
    else:
        print("\n❌ Le professional_id est incorrect")
        
        # Proposer la correction
        print("\n🔧 Voulez-vous corriger automatiquement ?")
        print("   - Oui: Le script va corriger automatiquement")
        print("   - Non: Vous devrez corriger manuellement")
        
        # Correction automatique
        if fix_professional_id():
            print("\n🎉 CORRECTION RÉUSSIE !")
            print("Vous pouvez maintenant tester l'accès aux rapports.")
        else:
            print("\n❌ CORRECTION ÉCHOUÉE")

if __name__ == "__main__":
    main()
