"""
Fonctions utilitaires pour le projet
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def ensure_dir(directory: str) -> None:
    """
    Crée un répertoire s'il n'existe pas
    
    Args:
        directory: Chemin du répertoire à créer
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_data(file_path: str) -> pd.DataFrame:
    """
    Charge les données depuis un fichier CSV
    
    Args:
        file_path: Chemin vers le fichier CSV
        
    Returns:
        DataFrame pandas avec les données
    """
    try:
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        print(f"Erreur: Le fichier {file_path} n'existe pas.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Erreur lors du chargement: {e}")
        return pd.DataFrame()


def calculate_reorder_point(predicted_demand: float, lead_time_days: int = 7, 
                           safety_stock_factor: float = 1.5) -> float:
    """
    Calcule le point de réapprovisionnement
    
    Args:
        predicted_demand: Demande prédite pour la période
        lead_time_days: Délai de livraison en jours
        safety_stock_factor: Facteur de sécurité pour le stock
    
    Returns:
        Point de réapprovisionnement recommandé
    """
    daily_demand = predicted_demand / 30  # Demande journalière moyenne
    reorder_point = (daily_demand * lead_time_days) * safety_stock_factor
    return max(0, round(reorder_point, 2))


def format_currency(amount: float) -> str:
    """
    Formate un montant en devise
    
    Args:
        amount: Montant à formater
        
    Returns:
        Chaîne formatée
    """
    return f"{amount:,.2f} €"


# Dictionnaire des noms de produits pharmaceutiques réels
PRODUCT_NAMES = {
    'PROD_001': 'Efferalgan 1000mg',
    'PROD_002': 'Doliprane 1000mg',
    'PROD_003': 'Spasfon Lyoc 80mg',
    'PROD_004': 'Smecta 3g',
    'PROD_005': 'Ibuprofene 400mg',
    'PROD_006': 'Paracetamol 500mg',
    'PROD_007': 'Aspirine 500mg',
    'PROD_008': 'Strepsils Miel Citron',
    'PROD_009': 'Humex Rhume',
    'PROD_010': 'Actifed Rhume'
}


def get_product_name(product_id: str) -> str:
    """
    Retourne le nom réel du produit pharmaceutique à partir de l'ID
    
    Args:
        product_id: Identifiant du produit
        
    Returns:
        Nom réel du produit ou ID si non trouvé
    """
    return PRODUCT_NAMES.get(product_id, f"Produit {product_id}")

