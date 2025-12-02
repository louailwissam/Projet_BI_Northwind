# Projet BI Northwind - Solution ETL & Dashboard

## Description du Projet
Ce projet consiste en la conception et la réalisation d'une solution de Business Intelligence (BI) complète pour l'entreprise fictive Northwind.

L'objectif principal est de consolider des données de ventes dispersées entre une base de données de production (SQL Server) et des fichiers d'archives (Excel/Access) afin de produire des indicateurs clés de performance sur la logistique et les ventes.

La solution repose sur un pipeline ETL (Extract, Transform, Load) développé en Python et une interface de visualisation interactive.

## Fonctionnalités
- Extraction de données depuis des sources hétérogènes (SQL Server et Excel).
- Nettoyage des données et gestion des doublons (priorisation de la source SQL).
- Transformation et calcul de KPIs métiers (Statut de livraison, délais).
- Chargement des données consolidées dans un Data Warehouse (Table SQL dédiée).
- Tableau de bord interactif avec filtres temporels et analyses par employé/client.

## Arborescence du Projet
Le projet respecte la structure suivante :

## Arborescence du Projet

```text
Projet_BI_Northwind/
│
├── data/
│   └── raw/                # Dossier contenant Orders.xlsx
│
├── scripts/                # Le cœur de l'ETL
│   ├── config.py           # Configuration (Serveur, Chemins)
│   ├── extract.py          # Extraction SQL + Excel
│   ├── transform.py        # Nettoyage et calcul des KPIs
│   └── load.py             # Chargement dans le Data Warehouse
│
├── reports/                # Contient le rapport final (PDF)
├── figures/                # Contient les captures d'écran
├── video/                  # Contient la vidéo de démonstration
├── notebooks/              # Zone de tests et brouillons
│
├── app.py                  # L'application Dashboard (Streamlit)
├── main.py                 # Le script d'exécution principal
├── requirements.txt        # Liste des bibliothèques à installer
└── README.md               # Documentation du projet
```
## Prérequis Techniques
- Python 3.8 ou supérieur
- Microsoft SQL Server (avec la base de données Northwind installée)
- Pilote ODBC pour SQL Server 

## Installation

1. Cloner le dépôt :
   git clone https://github.com/louailwissam/Projet_BI_Northwind.git
   cd Projet_BI_Northwind

2. Installer les bibliothèques Python nécessaires :
   pip install -r requirements.txt

   (Si le fichier requirements.txt est absent, installez manuellement : pandas, sqlalchemy, pyodbc, openpyxl, streamlit, matplotlib, seaborn).

3. Configuration :
   Ouvrez le fichier scripts/config.py et modifiez le paramètre SERVER pour qu'il corresponde à votre instance SQL Server locale.

## Utilisation

Mode Interface Graphique  :
Pour lancer le tableau de bord et piloter la mise à jour des données :
   streamlit run app.py

Mode Ligne de Commande :
Pour exécuter uniquement le traitement de données (ETL) sans l'interface visuelle :
   python main.py

## Justification des Choix Techniques

1. Langage Python & Pandas :
   Choisi pour sa puissance de traitement de données, sa capacité à manipuler des formats variés (Excel, SQL) et sa richesse en bibliothèques d'analyse.

2. Architecture ETL Modulaire :
   Le découpage en scripts distincts (Extract, Transform, Load) assure une meilleure maintenabilité, facilite le débogage et respecte le principe de séparation des responsabilités.

3. SQL Server :
   Utilisé comme entrepôt de données (Data Warehouse) pour garantir la persistance, la sécurité et l'intégrité des données transformées.

4. Streamlit :
   Sélectionné pour la couche de visualisation car il permet de développer rapidement une application web interactive connectée aux données Python sans nécessiter de compétences avancées en développement web (HTML/CSS/JS).

---
Auteur : Louail Wissam

