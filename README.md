#  Projet BI - Analyse des Livraisons Northwind

Ce projet est un système ETL complet développé en Python pour analyser la performance des livraisons de la société Northwind. Il consolide des données hétérogènes provenant de **SQL Server** (données historiques) et de fichiers **Excel/Access** (nouvelles commandes).

##  Fonctionnalités

*   **ETL Automatisé :** Extraction, Transformation et Chargement des données.
*   **Data Warehouse :** Centralisation des données propres dans une table SQL Server (`DWH_Global_Analysis`).
*   **Dashboard Interactif :** Application Web (Streamlit) permettant de visualiser les KPIs.
*   **Bouton Refresh :** Une fonctionnalité permettant de relancer l'ETL et mettre à jour les graphiques en un clic depuis l'interface.

##  Technologies utilisées

*   **Langage :** Python 
*   **ETL :** Pandas, SQLAlchemy, PyODBC
*   **Visualisation :** Streamlit, Matplotlib, Seaborn
*   **Base de données :** SQL Server 
