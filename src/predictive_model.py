"""
Modèle de prédiction utilisant Prophet pour les ventes pharmaceutiques
Génère des prédictions sur 30 jours pour l'optimisation des stocks
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import os
import pickle
import sys
from datetime import datetime, timedelta

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import ensure_dir, load_data


def prepare_prophet_data(df: pd.DataFrame, product_id: str) -> pd.DataFrame:
    """
    Prépare les données pour Prophet (format requis: ds et y)
    
    Args:
        df: DataFrame avec les données de ventes
        product_id: ID du produit à analyser
    
    Returns:
        DataFrame formaté pour Prophet
    """
    # Filtrer pour le produit spécifique
    product_df = df[df['product_id'] == product_id].copy()
    
    # Agrégation par date (au cas où il y aurait plusieurs enregistrements par jour)
    product_df = product_df.groupby('date')['quantity_sold'].sum().reset_index()
    
    # Renommer les colonnes pour Prophet (ds = date, y = valeur à prédire)
    prophet_df = pd.DataFrame({
        'ds': product_df['date'],
        'y': product_df['quantity_sold']
    })
    
    # Trier par date
    prophet_df = prophet_df.sort_values('ds').reset_index(drop=True)
    
    return prophet_df


def train_prophet_model(
    data_path: str = "data/processed/sales_aggregated.csv",
    product_id: str = None,
    forecast_days: int = 30
) -> tuple:
    """
    Entraîne un modèle Prophet pour un produit spécifique
    
    Args:
        data_path: Chemin vers les données agrégées
        product_id: ID du produit (si None, utilise le premier produit)
        forecast_days: Nombre de jours à prédire
    
    Returns:
        Tuple (modèle, prédictions, historique)
    """
    print(f"🔄 Chargement des données depuis {data_path}...")
    
    # Charger les données
    df = load_data(data_path)
    
    if df.empty:
        raise ValueError("Les données sont vides. Veuillez d'abord générer les données.")
    
    # Si aucun produit spécifié, utiliser le premier
    if product_id is None:
        product_id = df['product_id'].unique()[0]
        print(f"  ℹ️  Aucun produit spécifié, utilisation de: {product_id}")
    
    print(f"📦 Entraînement du modèle pour le produit: {product_id}")
    
    # Préparer les données pour Prophet
    prophet_df = prepare_prophet_data(df, product_id)
    
    if len(prophet_df) < 30:
        raise ValueError(f"Pas assez de données historiques (minimum 30 jours requis, {len(prophet_df)} disponibles)")
    
    print(f"  📊 Nombre de points de données: {len(prophet_df)}")
    print(f"  📅 Période: {prophet_df['ds'].min()} à {prophet_df['ds'].max()}")
    
    # Initialiser et configurer le modèle Prophet
    model = Prophet(
        yearly_seasonality=True,      # Saisonnalité annuelle
        weekly_seasonality=True,       # Saisonnalité hebdomadaire
        daily_seasonality=False,       # Pas de saisonnalité journalière
        seasonality_mode='multiplicative',  # Mode multiplicatif pour les ventes
        changepoint_prior_scale=0.05,  # Sensibilité aux changements de tendance
        interval_width=0.95           # Intervalle de confiance à 95%
    )
    
    # Entraîner le modèle
    print("  🔄 Entraînement en cours...")
    model.fit(prophet_df)
    
    # Créer un DataFrame pour les dates futures
    future_dates = model.make_future_dataframe(periods=forecast_days)
    
    # Générer les prédictions
    print(f"  🔮 Génération des prédictions pour {forecast_days} jours...")
    forecast = model.predict(future_dates)
    
    # Extraire seulement les prédictions futures
    last_historical_date = prophet_df['ds'].max()
    future_forecast = forecast[forecast['ds'] > last_historical_date].copy()
    
    print(f"✅ Modèle entraîné avec succès!")
    print(f"   📈 Prédictions générées du {future_forecast['ds'].min()} au {future_forecast['ds'].max()}")
    
    return model, forecast, prophet_df


def save_model(model: Prophet, product_id: str, output_dir: str = "models") -> str:
    """
    Sauvegarde le modèle entraîné
    
    Args:
        model: Modèle Prophet entraîné
        product_id: ID du produit
        output_dir: Répertoire de sortie
    
    Returns:
        Chemin du fichier sauvegardé
    """
    ensure_dir(output_dir)
    filename = f"{output_dir}/prophet_model_{product_id}.pkl"
    
    with open(filename, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"💾 Modèle sauvegardé dans: {filename}")
    return filename


def load_model(file_path: str) -> Prophet:
    """
    Charge un modèle sauvegardé
    
    Args:
        file_path: Chemin vers le fichier du modèle
    
    Returns:
        Modèle Prophet chargé
    """
    with open(file_path, 'rb') as f:
        model = pickle.load(f)
    return model


def train_all_products(
    data_path: str = "data/processed/sales_aggregated.csv",
    forecast_days: int = 30,
    models_dir: str = "models"
) -> dict:
    """
    Entraîne des modèles pour tous les produits
    
    Args:
        data_path: Chemin vers les données
        forecast_days: Nombre de jours à prédire
        models_dir: Répertoire pour sauvegarder les modèles
    
    Returns:
        Dictionnaire avec les modèles et prédictions pour chaque produit
    """
    print("=" * 60)
    print("ENTRAÎNEMENT DES MODÈLES POUR TOUS LES PRODUITS")
    print("=" * 60)
    print()
    
    # Charger les données
    df = load_data(data_path)
    
    if df.empty:
        raise ValueError("Les données sont vides. Veuillez d'abord générer les données.")
    
    products = df['product_id'].unique()
    results = {}
    
    for product_id in products:
        print(f"\n{'='*60}")
        print(f"Produit: {product_id}")
        print(f"{'='*60}")
        
        try:
            model, forecast, historical = train_prophet_model(
                data_path=data_path,
                product_id=product_id,
                forecast_days=forecast_days
            )
            
            # Sauvegarder le modèle
            model_path = save_model(model, product_id, models_dir)
            
            # Extraire les prédictions futures
            last_historical_date = historical['ds'].max()
            future_forecast = forecast[forecast['ds'] > last_historical_date].copy()
            
            results[product_id] = {
                'model': model,
                'forecast': forecast,
                'historical': historical,
                'future_forecast': future_forecast,
                'model_path': model_path
            }
            
        except Exception as e:
            print(f"❌ Erreur pour le produit {product_id}: {e}")
            continue
    
    print(f"\n{'='*60}")
    print(f"✅ Entraînement terminé pour {len(results)} produit(s)")
    print(f"{'='*60}")
    
    return results


if __name__ == "__main__":
    """
    Point d'entrée principal pour l'entraînement des modèles
    """
    print("=" * 60)
    print("MODÈLE DE PRÉDICTION PROPHET - VENTES PHARMACEUTIQUES")
    print("=" * 60)
    print()
    
    # Vérifier si les données existent
    data_path = "data/processed/sales_aggregated.csv"
    if not os.path.exists(data_path):
        print("❌ Les données n'existent pas. Veuillez d'abord exécuter:")
        print("   python src/data_generator.py")
        sys.exit(1)
    
    # Entraîner les modèles pour tous les produits
    results = train_all_products(
        data_path=data_path,
        forecast_days=30,
        models_dir="models"
    )
    
    print(f"\n✅ Processus terminé avec succès!")
    print(f"   📦 Modèles entraînés: {len(results)}")
    print(f"   📁 Emplacement: models/")








