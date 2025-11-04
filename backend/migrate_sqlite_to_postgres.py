"""
Script de migration des données de SQLite vers PostgreSQL
Exécutez ce script une fois après avoir déployé sur Render
"""

import os
import sys
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

def migrate_database():
    """
    Migre toutes les données de SQLite vers PostgreSQL
    """
    # URLs de connexion
    sqlite_url = "sqlite:///./breastcare.db"
    postgres_url = os.getenv("DATABASE_URL")
    
    if not postgres_url:
        print("❌ DATABASE_URL n'est pas défini")
        print("   Assurez-vous d'avoir défini cette variable d'environnement")
        sys.exit(1)
    
    print("🔄 Début de la migration SQLite → PostgreSQL")
    print(f"📥 Source: SQLite")
    print(f"📤 Destination: PostgreSQL")
    
    # Connecter aux deux bases de données
    sqlite_engine = create_engine(sqlite_url, echo=False)
    postgres_engine = create_engine(postgres_url, echo=False)
    
    # Créer les sessions
    SqliteSession = sessionmaker(bind=sqlite_engine)
    PostgresSession = sessionmaker(bind=postgres_engine)
    
    sqlite_session = SqliteSession()
    postgres_session = PostgresSession()
    
    try:
        # Créer les tables dans PostgreSQL si elles n'existent pas
        print("🏗️  Création des tables dans PostgreSQL...")
        from app.models.base import Base
        Base.metadata.create_all(bind=postgres_engine)
        print("✅ Tables créées")
        
        # Liste des tables à migrer
        tables_to_migrate = [
            "users",
            "patients",
            "professionals",
            "healthcare_centers",
            "access_requests",
            "mammography_analyses"
        ]
        
        for table_name in tables_to_migrate:
            try:
                print(f"\n📋 Migration de la table: {table_name}")
                
                # Lire depuis SQLite
                sqlite_table = Table(table_name, MetaData(), autoload_with=sqlite_engine)
                rows = sqlite_session.query(sqlite_table).all()
                
                if not rows:
                    print(f"   ⚠️  Aucune donnée à migrer")
                    continue
                
                print(f"   📊 {len(rows)} lignes trouvées")
                
                # Écrire dans PostgreSQL
                # Note: On utilise ici une approche simple avec INSERT OR IGNORE
                # SQLAlchemy ne fournit pas nativement cette fonctionnalité pour PostgreSQL
                # On doit donc vérifier l'existence manuellement
                
                postgres_table = Table(table_name, MetaData(), autoload_with=postgres_engine)
                
                migrated_count = 0
                for row in rows:
                    try:
                        # Convertir la ligne en dictionnaire
                        row_dict = {column: getattr(row, column) for column in sqlite_table.columns.keys()}
                        
                        # Nettoyer les valeurs None pour les Enum
                        for key, value in row_dict.items():
                            if hasattr(value, 'value'):
                                row_dict[key] = value.value
                        
                        # Insérer dans PostgreSQL
                        postgres_session.execute(
                            postgres_table.insert().values(**row_dict)
                        )
                        migrated_count += 1
                    except Exception as e:
                        # Ignorer les doublons
                        if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
                            continue
                        else:
                            print(f"   ⚠️  Erreur lors de l'insertion: {e}")
                
                postgres_session.commit()
                print(f"   ✅ {migrated_count} lignes migrées avec succès")
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
                postgres_session.rollback()
                continue
        
        print("\n✅ Migration terminée avec succès!")
        print("📊 Vérification des données...")
        
        # Vérifier que les données sont bien migrées
        for table_name in tables_to_migrate:
            try:
                postgres_table = Table(table_name, MetaData(), autoload_with=postgres_engine)
                count = postgres_session.query(postgres_table).count()
                print(f"   {table_name}: {count} lignes")
            except:
                pass
                
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        sqlite_session.close()
        postgres_session.close()
        sqlite_engine.dispose()
        postgres_engine.dispose()


if __name__ == "__main__":
    migrate_database()

