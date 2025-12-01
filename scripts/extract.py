import pandas as pd
import sqlalchemy
import os
from scripts.config import DB_CONFIG, DATA_RAW_DIR


# Fonction de connexion
def get_sql_engine():
    conn_str = f"mssql+pyodbc://{DB_CONFIG['server']}/{DB_CONFIG['database']}?driver={DB_CONFIG['driver']}&trusted_connection={DB_CONFIG['trusted_connection']}"
    return sqlalchemy.create_engine(conn_str)


def extract_data():
    print("\n--- 1. EXTRACTION DES DONNÉES ---")

    # ---------------------------------------------------------
    # PARTIE A : SQL SERVER (On transforme les IDs en NOMS)
    # ---------------------------------------------------------
    print("   -> Connexion à SQL Server...")
    try:
        engine = get_sql_engine()
        # LA REQUÊTE : On joint Orders, Customers et Employees
        query = """
        SELECT 
            o.OrderID,
            o.OrderDate,
            o.ShippedDate,
            o.ShipCity,
            o.ShipCountry,
            c.CompanyName,
            e.FirstName + ' ' + e.LastName as EmployeeName
        FROM Orders o
        LEFT JOIN Customers c ON o.CustomerID = c.CustomerID
        LEFT JOIN Employees e ON o.EmployeeID = e.EmployeeID
        """
        df_sql = pd.read_sql(query, engine)
        df_sql['Source'] = 'SQL_Server'
        print(f"    SQL : {len(df_sql)} commandes récupérées.")

    except Exception as e:
        print(f"    Erreur SQL : {e}")
        df_sql = pd.DataFrame()

    # ---------------------------------------------------------
    # PARTIE B : EXCEL (Orders.xlsx)
    # ---------------------------------------------------------
    print("   -> Lecture du fichier Excel...")
    file_path = os.path.join(DATA_RAW_DIR, 'Orders.xlsx')

    if os.path.exists(file_path):
        df_excel = pd.read_excel(file_path)

        # On renomme les colonnes Excel pour qu'elles aient le même nom que SQL
        mapping = {
            'Order ID': 'OrderID',
            'Order Date': 'OrderDate',
            'Shipped Date': 'ShippedDate',
            'Ship City': 'ShipCity',
            'Ship Country/Region': 'ShipCountry',
            'Customer': 'CompanyName',
            'Employee': 'EmployeeName'
        }
        df_excel = df_excel.rename(columns=mapping)

        # On garde les colonnes communes
        cols = ['OrderID', 'OrderDate', 'ShippedDate', 'ShipCity', 'ShipCountry', 'CompanyName', 'EmployeeName']
        cols_existantes = [c for c in cols if c in df_excel.columns]
        df_excel = df_excel[cols_existantes]

        df_excel['Source'] = 'Access_Excel'
        print(f"    Excel : {len(df_excel)} commandes récupérées.")

    else:
        print(f"    Fichier introuvable : {file_path}")
        df_excel = pd.DataFrame()

    # ---------------------------------------------------------
    # FUSION ET GESTION DES DOUBLONS
    # ---------------------------------------------------------
    if df_sql.empty and df_excel.empty:
        return pd.DataFrame()

    # 1. On empile tout
    df_final = pd.concat([df_sql, df_excel], ignore_index=True)
    count_before = len(df_final)

    # 2. Détection et Suppression des doublons
    # On regarde si 'OrderID' apparaît plusieurs fois.
    # keep='first' signifie qu'on garde la première occurrence (celle de SQL car df_sql est premier dans concat)
    nb_doublons = df_final.duplicated(subset=['OrderID']).sum()

    if nb_doublons > 0:
        print(f"     ATTENTION : {nb_doublons} doublons détectés (IDs identiques dans SQL et Excel).")
        df_final = df_final.drop_duplicates(subset=['OrderID'], keep='first')
        print("     Doublons supprimés (Priorité aux données SQL).")
    else:
        print("     Aucun doublon : Les commandes SQL et Excel sont bien distinctes.")

    print(f"    TOTAL CONSOLIDÉ UNIQUE : {len(df_final)} lignes.")

    return df_final