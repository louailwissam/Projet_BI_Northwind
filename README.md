Northwind BI : Pipeline ETL & Dashboard Décisionnel
Ce projet est une solution complète de Business Intelligence (BI) conçue pour analyser la performance logistique de l'entreprise Northwind. Il intègre un pipeline ETL (Extract, Transform, Load) automatisé et une interface de visualisation interactive.
- Objectif du Projet
L'objectif est de consolider des données de ventes dispersées entre une base de production (SQL Server) et des archives historiques (Excel), afin de fournir une vue unifiée sur les indicateurs de livraison.
Fonctionnalités Clés
- Connexion Hybride : Fusion intelligente des données SQL et Excel.
- Gestion des Doublons : Algorithme de déduplication priorisant les données SQL (Source de vérité).
  - Nettoyage de Données : Standardisation des dates et normalisation des textes.
- KPI Métier : Calcul automatique du statut de livraison (Livrée / Non Livrée).
  - Dashboard Interactif : Application Web permettant le filtrage par dates et l'analyse par employé/client.
Architecture Technique
Extract (extract.py) : Récupération des données brutes et fusion.
Transform (transform.py) : Nettoyage, typage et calculs métier.
Load (load.py) : Chargement en mode "Full Refresh" dans la table DWH_Global_Analysis.
Visualize (app.py) : Restitution graphique.
Structure du Projet
Projet_BI_Northwind/
│
├── data/
│   └── raw/
│       └── Orders.xlsx       # Fichier source Excel (Archives)
│
├── scripts/
│   ├── config.py             # Configuration (Chemins, Connexion DB)
│   ├── extract.py            # Script d'extraction et déduplication
│   ├── transform.py          # Script de nettoyage et KPIs
│   └── load.py               # Script de chargement SQL
│
├── app.py                    # Application Dashboard (Streamlit)
Installation et Démarrage
 Prérequis
Python  installé.
SQL Server (Express ) avec la base de données Northwind.
Le fichier Orders.xlsx placé dans data/raw/.
├── main.py                   # Orchestrateur ETL (Backend uniquement)
├── requirements.txt          # Liste des dépendances Python
└── README.md                 # Documentation du projet
