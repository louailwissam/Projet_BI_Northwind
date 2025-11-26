import pandas as pd
import sqlalchemy
from scripts.config import DB_CONFIG


def get_sql_engine():
    """Réutilise la configuration pour créer le moteur SQL"""
    conn_str = f"mssql+pyodbc://{DB_CONFIG['server']}/{DB_CONFIG['database']}?driver={DB_CONFIG['driver']}&trusted_connection={DB_CONFIG['trusted_connection']}"
    return sqlalchemy.create_engine(conn_str)


def load_data(df):
    """
    CHARGE les données transformées directement dans une table SQL Server.
    Cette table servira de Data Warehouse.
    """
    print("\n--- 3. CHARGEMENT (LOAD VERS SQL SERVER) ---")

    # Nom de la table finale dans SQL Server
    table_name = "DWH_Global_Analysis"

    try:
        engine = get_sql_engine()

        print(f"   -> Connexion au serveur : {DB_CONFIG['server']}")
        print(f"   -> Écriture dans la table : {table_name}")

        # if_exists='replace' : C'est la clé pour le bouton REFRESH !
        # À chaque fois qu'on lance, il supprime l'ancienne table et recrée la nouvelle avec les nouvelles données.
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        print(f"   ✅ SUCCÈS : {len(df)} lignes insérées dans la table '{table_name}'.")
        return True

    except Exception as e:
        print(f"   ❌ Erreur lors de l'écriture SQL : {e}")
        return False