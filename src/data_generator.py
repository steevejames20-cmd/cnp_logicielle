"""
Générateur de données simulées pour les ventes pharmaceutiques
Crée un jeu de données réaliste avec des tendances saisonnières
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import ensure_dir


def generate_sales_data(
    start_date: str = "2022-01-01",
    end_date: str = "2024-01-01",
    num_products: int = 10,
    output_path: str = "data/raw/sales_data.csv"
) -> pd.DataFrame:
    """
    Génère des données de ventes simulées pour une entreprise pharmaceutique
    
    Args:
        start_date: Date de début (format YYYY-MM-DD)
        end_date: Date de fin (format YYYY-MM-DD)
        num_products: Nombre de produits à générer
        output_path: Chemin de sortie pour le fichier CSV
    
    Returns:
        DataFrame avec les données de ventes générées
    """
    print("🔄 Génération des données de ventes simulées...")
    
    # Créer le répertoire de sortie si nécessaire
    ensure_dir(os.path.dirname(output_path))
    
    # Générer la plage de dates
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Liste des noms de produits pharmaceutiques réels
    product_names_list = [
        'Efferalgan 1000mg',
        'Doliprane 1000mg',
        'Spasfon Lyoc 80mg',
        'Smecta 3g',
        'Ibuprofene 400mg',
        'Paracetamol 500mg',
        'Aspirine 500mg',
        'Strepsils Miel Citron',
        'Humex Rhume',
        'Actifed Rhume'
    ]
    
    # Liste pour stocker toutes les données
    all_data = []
    
    # Générer des données pour chaque produit
    for product_id in range(1, num_products + 1):
        product_id_str = f'PROD_{product_id:03d}'
        product_name = product_names_list[product_id - 1] if product_id <= len(product_names_list) else f'Produit {product_id}'
        print(f"  📦 Génération des données pour {product_name} ({product_id_str})...")
        
        # Paramètres de base pour chaque produit (variabilité)
        base_demand = np.random.uniform(50, 200)  # Demande de base variable
        trend = np.random.uniform(-0.1, 0.1)  # Tendance légère (croissance/décroissance)
        
        # Générer les ventes pour chaque jour
        for date in dates:
            # Composante de tendance
            days_from_start = (date - dates[0]).days
            trend_component = 1 + (trend * days_from_start / 365)
            
            # Composante saisonnière (variations hebdomadaires et mensuelles)
            day_of_week = date.weekday()  # 0 = lundi, 6 = dimanche
            month = date.month
            
            # Moins de ventes le week-end
            weekly_factor = 0.7 if day_of_week >= 5 else 1.0
            
            # Variations mensuelles (ex: plus de ventes en hiver pour certains produits)
            monthly_factor = 1.0 + 0.2 * np.sin(2 * np.pi * month / 12)
            
            # Composante aléatoire
            random_factor = np.random.uniform(0.8, 1.2)
            
            # Calcul de la quantité vendue
            quantity = base_demand * trend_component * weekly_factor * monthly_factor * random_factor
            
            # S'assurer que la quantité est positive et entière
            quantity = max(0, int(round(quantity)))
            
            # Ajouter les données
            all_data.append({
                'date': date,
                'product_id': product_id_str,
                'product_name': product_name,
                'quantity_sold': quantity
            })
    
    # Créer le DataFrame
    df = pd.DataFrame(all_data)
    
    # Trier par date et produit
    df = df.sort_values(['date', 'product_id']).reset_index(drop=True)
    
    # Sauvegarder dans un fichier CSV
    df.to_csv(output_path, index=False)
    print(f"✅ Données générées et sauvegardées dans: {output_path}")
    print(f"   📊 Nombre total d'enregistrements: {len(df):,}")
    print(f"   📅 Période: {df['date'].min()} à {df['date'].max()}")
    print(f"   🏷️  Nombre de produits: {df['product_id'].nunique()}")
    
    return df


def generate_aggregated_data(
    input_path: str = "data/raw/sales_data.csv",
    output_path: str = "data/processed/sales_aggregated.csv"
) -> pd.DataFrame:
    """
    Agrège les données par date et produit (somme des quantités)
    
    Args:
        input_path: Chemin vers le fichier de données brutes
        output_path: Chemin de sortie pour les données agrégées
    
    Returns:
        DataFrame agrégé
    """
    print("🔄 Agrégation des données...")
    
    # Charger les données
    df = pd.read_csv(input_path)
    df['date'] = pd.to_datetime(df['date'])
    
    # Si product_name n'existe pas, le créer à partir de product_id
    if 'product_name' not in df.columns:
        from src.utils import get_product_name
        df['product_name'] = df['product_id'].apply(get_product_name)
    
    # Agrégation par date et produit (garder product_name)
    df_agg = df.groupby(['date', 'product_id', 'product_name'])['quantity_sold'].sum().reset_index()
    
    # Créer le répertoire de sortie
    ensure_dir(os.path.dirname(output_path))
    
    # Sauvegarder
    df_agg.to_csv(output_path, index=False)
    print(f"✅ Données agrégées sauvegardées dans: {output_path}")
    
    return df_agg


if __name__ == "__main__":
    """
    Point d'entrée principal pour la génération de données
    """
    print("=" * 60)
    print("GÉNÉRATEUR DE DONNÉES SIMULÉES - VENTES PHARMACEUTIQUES")
    print("=" * 60)
    print()
    
    # Générer les données de base
    df = generate_sales_data(
        start_date="2022-01-01",
        end_date="2024-01-01",
        num_products=10,
        output_path="data/raw/sales_data.csv"
    )
    
    # Générer les données agrégées
    df_agg = generate_aggregated_data(
        input_path="data/raw/sales_data.csv",
        output_path="data/processed/sales_aggregated.csv"
    )
    
    print()
    print("=" * 60)
    print("✅ Génération terminée avec succès!")
    print("=" * 60)

