import pandas as pd
import numpy as np

def load_and_clean_sales_data(file_path):
    """
    Fonction de chargement, de nettoyage et de préparation des données de ventes.
    """
    # 1. Chargement des données brutes
    print("--- Chargement des données ---")
    df = pd.read_csv(file_path)
    print(f"Dimensions initiales du dataset : {df.shape}")
    
    # 2. Suppression des doublons
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"Doublons supprimés : {initial_rows - len(df)}")
    
    # 3. Gestion des valeurs manquantes
    # Suppression des lignes où les identifiants clés ou les montants sont manquants
    df = df.dropna(subset=['order_id', 'product_id', 'sales_amount'])
    
    # Remplacement des valeurs textuelles manquantes par une valeur par défaut
    if 'customer_region' in df.columns:
        df['customer_region'].fillna('Unknown', inplace=True)
        
    # 4. Conversion des types de données
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'])
        
    # S'assurer que les colonnes numériques sont au bon format
    df['sales_amount'] = pd.to_numeric(df['sales_amount'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    
    # 5. Feature Engineering (Création de nouvelles variables utiles pour l'analyse)
    # Extraction du mois et de l'année pour faciliter les agrégations temporelles
    df['order_month'] = df['order_date'].dt.to_period('M')
    df['order_year'] = df['order_date'].dt.year
    
    # Calcul du montant total de la ligne si unitaire et quantité existent
    if 'unit_price' in df.columns and 'quantity' in df.columns:
        df['calculated_total'] = df['unit_price'] * df['quantity']
        
    print(f"Dimensions finales après nettoyage : {df.shape}")
    return df

# Exemple d'utilisation :
# df_cleaned = load_and_clean_sales_data('raw_sales_data.csv')
# df_cleaned.to_csv('cleaned_sales_data.csv', index=False)
