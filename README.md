# PROJET BI NORTHWIND : PIPELINE ETL ET DASHBOARD DECISIONNEL

**Auteur :** Louail Wissam
**Date :** 11 Decembre 2025

---

## 1. INTRODUCTION ET CONTEXTE

Dans un contexte ou les donnees de l'entreprise **Northwind Traders** sont fragmentees, ce projet vise a consolider l'information pour faciliter la prise de decision.

L'objectif principal est de resoudre la dispersion des commandes stockees sur deux supports distincts :
1.  **SQL Server (ERP)** : Base de donnees relationnelle.
2.  **Fichiers Excel** : Commandes manuelles ou archives.

La solution repose sur la conception d'un **Pipeline ETL (Extract, Transform, Load)** automatise en Python, alimentant un **Entrepot de Donnees (Data Warehouse)** et restitue via une interface web interactive developpee avec **Streamlit**.

---

## 2. ARCHITECTURE TECHNIQUE (PIPELINE ETL)

L'architecture du projet est modulaire, respectant le principe de separation des responsabilites. Chaque etape est isolee dans un script dedie.

### 2.1. Configuration (config.py)
Module central des parametres. Il definit les chemins d'acces relatifs et centralise les identifiants de connexion a la base de donnees (Driver ODBC, Serveur).

### 2.2. Module d'Extraction (extract.py)
Responsable de l'ingestion des donnees brutes :
*   **Ingestion SQL :** Utilisation de SQLAlchemy pour les requetes complexes (Jointures Clients/Employes).
*   **Ingestion Excel :** Lecture et mapping des colonnes via Pandas.
*   **Consolidation :** Fusion des flux et deduplication sur la cle primaire `OrderID`. En cas de conflit, SQL Server est considere comme la source de verite.

### 2.3. Module de Transformation (transform.py)
Application de la logique metier et qualite des donnees :
*   **Standardisation Temporelle :** Conversion des dates au format standard.
*   **Enrichissement :** Creation d'attributs derives (Mois, Annee).
*   **Calcul de KPI :** Creation de la metrique `Status_Livraison` (basee sur la presence d'une date d'expedition).
*   **Nettoyage Textuel :** Normalisation des chaines de caracteres.

### 2.4. Module de Chargement (load.py)
Ecriture vers la cible finale :
*   **Cible :** Table `DWH_Global_Analysis` dans SQL Server.
*   **Strategie :** "Full Load". La table de destination est entierement reconstruite a chaque execution pour garantir une synchronisation parfaite.

### 2.5. Orchestration (main.py)
Point d'entree unique qui sequence l'execution (Extract -> Transform -> Load) et gere les arrets d'urgence.

---

## 3. MODELISATION OLAP

Pour l'analyse decisionnelle, le modele transactionnel (OLTP) a ete transforme en modele analytique denormalise (Table Unique).

*   **Avantage :** Simplification des requetes et optimisation des performances de lecture pour le Dashboard.
*   **Dimensions :** Temps (Annee, Mois), Entites (Employe, Client), Geographie (Ville, Pays).
*   **Mesures :** Volume de commandes, Statut de livraison.

---

## 4. INTERFACE DE VISUALISATION (DASHBOARD)

L'application (`app.py`), developpee avec Streamlit, se connecte en lecture a l'entrepot de donnees.

### Fonctionnalites
*   **ETL On-Demand :** Un bouton "ACTUALISER LES DONNEES" permet de declencher le pipeline complet et de rafraichir le cache de l'application.
*   **Filtrage Temporel :** Selection dynamique de la periode via un calendrier, mettant a jour tous les graphiques.

### Analyses Disponibles
1.  **KPIs Globaux :** Total commandes, Volume Livre vs Non Livre, Taux de reussite.
2.  **Analyse Temporelle :** Courbe d'evolution mensuelle des commandes et suivi des incidents.
3.  **Performance Employe :** Graphique a barres de la charge de travail par employe.
4.  **Top 10 Clients :** Identification des comptes generant le plus de volume.

---

## 5. INSTALLATION ET EXECUTION

### Prerequis
*   Python 3.8 ou superieur
*   Serveur SQL accessible
*   Pilote ODBC pour SQL Server

### Installation
```bash
pip install -r requirements.txt
