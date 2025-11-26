from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data  #  l'import du Load
import os


def main():
    print(" DÉMARRAGE DU JOB ETL NORTHWIND\n")

    # ---------------------------
    # 1. EXTRACT
    # ---------------------------
    df_raw = extract_data()
    if df_raw.empty:
        print(" Arrêt : Pas de données extraites.")
        return

    # ---------------------------
    # 2. TRANSFORM
    # ---------------------------
    df_clean = transform_data(df_raw)

    # Petit check qualité
    print("\n    KPI GLOBAL :")
    print(df_clean['Status_Livraison'].value_counts())

    # ---------------------------
    # 3. LOAD
    # ---------------------------
    file_path = load_data(df_clean)

    if file_path:
        print("\n ETL TERMINÉ ! Les données sont prêtes pour la visualisation.")
    else:
        print("\n ETL terminé avec des erreurs de sauvegarde.")


if __name__ == "__main__":
    main()