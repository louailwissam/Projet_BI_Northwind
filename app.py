import streamlit as st
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data
from scripts.config import DB_CONFIG

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="Dashboard Northwind", layout="wide")
st.title(" Dashboard BI - Suivi des Livraisons Northwind")

# --- STYLE CSS (Optionnel, pour faire joli) ---
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


# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header(" Contrôle")
    if st.button(" ACTUALISER LES DONNÉES (ETL)"):
        run_full_etl()
    st.info("Ce bouton relance tout le processus ")


# --- LECTURE DONNÉES ---
def get_data():
    conn_str = f"mssql+pyodbc://{DB_CONFIG['server']}/{DB_CONFIG['database']}?driver={DB_CONFIG['driver']}&trusted_connection={DB_CONFIG['trusted_connection']}"
    engine = sqlalchemy.create_engine(conn_str)
    try:
        return pd.read_sql("SELECT * FROM DWH_Global_Analysis", engine)
    except:
        return pd.DataFrame()


df = get_data()

if df.empty:
    st.warning(" Aucune donnée. Cliquez sur ACTUALISER.")
else:
    # --- 1. KPIs GLOBAUX ---
    st.subheader(" Indicateurs Clés")
    col1, col2, col3, col4 = st.columns(4)

    total = len(df)
    livrees = len(df[df['Status_Livraison'] == 'Livrée'])
    non_livrees = len(df[df['Status_Livraison'] == 'Non Livrée'])
    pct_livraison = round((livrees / total) * 100, 1)

    col1.metric("Total Commandes", total)
    col2.metric("Livrées", livrees)
    col3.metric("Non Livrées", non_livrees, delta="-Alert")
    col4.metric("Taux de Livraison", f"{pct_livraison}%")

    st.divider()

    # --- 2. ANALYSE TEMPORELLE (Par Date) ---
    st.subheader(" Évolution des Commandes (Livrées vs Non Livrées)")

    # On prépare les données : Group by Mois + Status
    df_date = df.groupby(['Mois_Annee', 'Status_Livraison']).size().unstack().fillna(0)

    # Graphique en ligne (Line Chart) interactif natif Streamlit
    st.line_chart(df_date, color=["#ff9999", "#66b3ff"])  # Rouge pour Non Livrée (si alpha), Bleu pour Livrée

    st.divider()

    # --- 3. ANALYSE PAR EMPLOYE ET CLIENT ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("bust_in_silhouette: Performance par Employé")
        # On compte Livrée/Non Livrée par employé
        fig, ax = plt.subplots(figsize=(6, 6))

        # Le paramètre 'hue' permet de séparer les couleurs par Status
        sns.countplot(y='EmployeeName', data=df, hue='Status_Livraison',
                      palette={'Livrée': '#66b3ff', 'Non Livrée': '#ff9999'}, ax=ax)

        ax.set_xlabel("Nombre de commandes")
        ax.set_ylabel("")
        st.pyplot(fig)

    with c2:
        st.subheader(" Top 10 Clients (État des commandes)")
        # On prend les 10 plus gros clients pour ne pas surcharger le graphe
        top_10_names = df['CompanyName'].value_counts().head(10).index
        df_top_clients = df[df['CompanyName'].isin(top_10_names)]

        fig, ax = plt.subplots(figsize=(6, 6))
        sns.countplot(y='CompanyName', data=df_top_clients, hue='Status_Livraison',
                      palette={'Livrée': '#66b3ff', 'Non Livrée': '#ff9999'}, ax=ax)

        ax.set_xlabel("Nombre de commandes")
        ax.set_ylabel("")
        st.pyplot(fig)