import streamlit as st
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data
from scripts.config import DB_CONFIG
import datetime  # Nécessaire pour les dates par défaut

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="Dashboard Northwind", layout="wide")
st.title("  Dashboard BI - Suivi des Livraisons Northwind")

# --- STYLE CSS  ---
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; padding: 15px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)


# --- FONCTION ETL (REFRESH) ---
def run_full_etl():
    with st.spinner('Extraction des données en cours...'):
        df_raw = extract_data()
    with st.spinner('Transformation et calcul des KPIs...'):
        df_clean = transform_data(df_raw)
    with st.spinner('Mise à jour du Data Warehouse SQL...'):
        succes = load_data(df_clean)
    if succes:
        st.success("Données mises à jour avec succès !")
    else:
        st.error(" Erreur lors de la mise à jour.")


# --- LECTURE DONNÉES ---
@st.cache_data(ttl=60)  # Petit cache pour éviter de recharger SQL à chaque clic
def get_data():
    conn_str = f"mssql+pyodbc://{DB_CONFIG['server']}/{DB_CONFIG['database']}?driver={DB_CONFIG['driver']}&trusted_connection={DB_CONFIG['trusted_connection']}"
    engine = sqlalchemy.create_engine(conn_str)
    try:
        df = pd.read_sql("SELECT * FROM DWH_Global_Analysis", engine)
        # S'assurer que OrderDate est bien en datetime
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        return df
    except:
        return pd.DataFrame()


# Chargement initial
df = get_data()

# --- BARRE LATÉRALE (Filtres & Actions) ---
with st.sidebar:
    st.header(" Contrôle & Filtres")

    # 1. Bouton ETL
    if st.button(" ACTUALISER LES DONNÉES"):
        run_full_etl()
        st.cache_data.clear()  # On vide le cache pour voir les nouvelles données
        df = get_data()  # On recharge

    st.divider()

    # 2. Filtre par Date
    st.subheader(" Période d'analyse")

    if not df.empty:
        # Dates par défaut : min et max des données
        min_date = df['OrderDate'].min().date()
        max_date = df['OrderDate'].max().date()

        date_debut = st.date_input("Date de début", min_date)
        date_fin = st.date_input("Date de fin", max_date)
    else:
        date_debut = None
        date_fin = None

# --- FILTRAGE DU DATAFRAME ---
if not df.empty and date_debut and date_fin:
    # On applique le masque de filtrage
    mask = (df['OrderDate'].dt.date >= date_debut) & (df['OrderDate'].dt.date <= date_fin)
    df_filtered = df.loc[mask]
else:
    df_filtered = df

# --- AFFICHAGE DASHBOARD ---

if df_filtered.empty:
    if df.empty:
        st.warning(" Aucune donnée dans la base. Cliquez sur ACTUALISER.")
    else:
        st.warning(" Aucune commande trouvée pour la période sélectionnée.")
else:
    # --- 1. KPIs GLOBAUX ---
    st.subheader(f" Indicateurs Clés ({date_debut} au {date_fin})")
    col1, col2, col3, col4 = st.columns(4)

    total = len(df_filtered)
    livrees = len(df_filtered[df_filtered['Status_Livraison'] == 'Livrée'])
    non_livrees = len(df_filtered[df_filtered['Status_Livraison'] == 'Non Livrée'])

    if total > 0:
        pct_livraison = round((livrees / total) * 100, 1)
    else:
        pct_livraison = 0

    col1.metric("Total Commandes", total)
    col2.metric("Livrées", livrees)
    col3.metric("Non Livrées", non_livrees, delta="-Attention" if non_livrees > 0 else "OK")
    col4.metric("Taux de Livraison", f"{pct_livraison}%")

    st.divider()

    # --- 2. ANALYSE TEMPORELLE (Par Date) ---
    st.subheader(" Évolution temporelle")

    # On regroupe
    df_date = df_filtered.groupby(['Mois_Annee', 'Status_Livraison']).size().unstack().fillna(0)
    st.line_chart(df_date, color=["#ff9999", "#66b3ff"])

    st.divider()

    # --- 3. ANALYSE PAR EMPLOYE ET CLIENT ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("👤 Performance par Employé")
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.countplot(y='EmployeeName', data=df_filtered, hue='Status_Livraison',
                      palette={'Livrée': '#66b3ff', 'Non Livrée': '#ff9999'}, ax=ax)
        ax.set_xlabel("Nombre de commandes")
        ax.set_ylabel("")
        st.pyplot(fig)

    with c2:
        st.subheader("Top 10 Clients")
        # Top 10 basé sur les données filtrées
        top_10_names = df_filtered['CompanyName'].value_counts().head(10).index
        df_top_clients = df_filtered[df_filtered['CompanyName'].isin(top_10_names)]

        fig, ax = plt.subplots(figsize=(6, 6))
        sns.countplot(y='CompanyName', data=df_top_clients, hue='Status_Livraison',
                      palette={'Livrée': '#66b3ff', 'Non Livrée': '#ff9999'}, ax=ax)
        ax.set_xlabel("Nombre de commandes")
        ax.set_ylabel("")
        st.pyplot(fig)