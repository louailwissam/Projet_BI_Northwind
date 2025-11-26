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
        # LA REQUÊTE MAGIQUE : On joint Orders, Customers et Employees
        # pour avoir les noms au lieu des IDs, comme dans Excel.
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

        # On renomme tes colonnes Excel pour qu'elles aient le même nom que SQL
        mapping = {
            'Order ID': 'OrderID',
            'Order Date': 'OrderDate',
            'Shipped Date': 'ShippedDate',
            'Ship City': 'ShipCity',
            'Ship Country/Region': 'ShipCountry',
            'Customer': 'CompanyName',  # Nom déjà présent dans Excel
            'Employee': 'EmployeeName'  # Nom déjà présent dans Excel
        }
        df_excel = df_excel.rename(columns=mapping)

        # On garde les colonnes communes
        cols = ['OrderID', 'OrderDate', 'ShippedDate', 'ShipCity', 'ShipCountry', 'CompanyName', 'EmployeeName']
        # On filtre seulement si les colonnes existent
        cols_existantes = [c for c in cols if c in df_excel.columns]
        df_excel = df_excel[cols_existantes]

        df_excel['Source'] = 'Access_Excel'
        print(f"    Excel : {len(df_excel)} commandes récupérées.")

    else:
        print(f"    Fichier introuvable : {file_path}")
        df_excel = pd.DataFrame()

    # ---------------------------------------------------------
    # FUSION
    # ---------------------------------------------------------
    if df_sql.empty and df_excel.empty:
        return pd.DataFrame()

    df_final = pd.concat([df_sql, df_excel], ignore_index=True)
    print(f"    TOTAL CONSOLIDÉ : {len(df_final)} lignes.")

    return df_final