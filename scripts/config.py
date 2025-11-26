import os

# --- 1. CHEMINS DES DOSSIERS ---
# Cela permet à Python de trouver le dossier 'data' automatiquement
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')

# --- 2. CONFIGURATION SQL SERVER ---
# C'est ici qu'on met tes infos de connexion
DB_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': 'DESKTOP-EQ55Q8H\\SQLEXPRESS',
    'database': 'Northwind',
    'trusted_connection': 'yes'
}

# --- 3. NOMS DES FICHIERS EXCEL ---
EXCEL_FILES = {
    'orders': 'Orders.xlsx'
}