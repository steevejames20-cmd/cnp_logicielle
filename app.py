"""
Application Streamlit pour la visualisation et l'analyse prédictive
des ventes pharmaceutiques avec recommandations d'optimisation des stocks
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import sys
from datetime import datetime, timedelta
import pickle

# Palette et styles globaux (clair, moderne)
PRIMARY = "#2563EB"       # bleu
SECONDARY = "#10B981"     # vert doux
ACCENT = "#F59E0B"        # amber
TEXT_MAIN = "#0F172A"     # texte principal foncé
TEXT_MUTED = "#6B7280"    # gris moyen

# Internationalisation simple (FR/EN) — défini tôt pour être disponible dans le bandeau hero
LANG_STRINGS = {
    "fr": {
        "lang_label": "Langue",
        "hero_badge": "Tableau de bord ventes & stocks",
        "hero_title": "Analyse des ventes & optimisation des stocks",
        "hero_subtitle": "Répartition pharmaceutique — prédiction 30 jours et recommandations claires.",
        "hero_stack": "Prophet · Streamlit · Plotly",
        "sidebar_conf": "⚙️ Configuration",
        "sidebar_data": "📊 Données",
        "reload": "🔄 Charger/Recharger les Données",
        "data_missing": "❌ Les données n'existent pas!",
        "data_hint": "💡 Exécutez d'abord: `python src/data_generator.py`",
        "product_select": "📦 Sélectionner un produit",
        "lead_time": "Délai de livraison (jours)",
        "lead_help": "Temps nécessaire pour recevoir une nouvelle commande",
        "safety": "Facteur de sécurité",
        "safety_help": "Facteur multiplicateur pour le stock de sécurité",
        "selected_product": "Produit sélectionné",
        "tabs": ["📊 Données Historiques", "🔮 Prédictions", "📈 Vue Combinée", "💡 Recommandations"],
        "hist_title": "📊 Visualisation des Ventes Historiques",
        "hist_stats": "📈 Statistiques Mensuelles",
        "hist_dist": "📊 Distribution des Ventes",
        "metric_total": "📊 Ventes Totales",
        "metric_avg": "📈 Ventes Moyennes/Jour",
        "metric_max": "⬆️ Vente Max/Jour",
        "metric_period": "📅 Période (jours)",
        "pred_title": "🔮 Prédictions des Ventes (30 jours)",
        "pred_spinner": "🔄 Chargement ou entraînement du modèle en cours...",
        "pred_avg": "📊 Vente Moyenne Prédite/Jour",
        "pred_total": "📈 Total Prédit (30 jours)",
        "pred_peak": "⬆️ Pic Prédit",
        "pred_table": "📋 Détails des Prédictions",
        "combined_title": "Vue Complète: Historique et Prédictions",
        "reco_title": "💡 Recommandations d'Optimisation des Stocks",
        "reco_spinner": "🔄 Calcul des recommandations...",
        "reco_product": "📦 Produit",
        "reco_pred_demand": "📊 Demande Prédite (30 jours)",
        "reco_reorder": "⏱️ Point de Réapprovisionnement",
        "reco_order": "🛒 Quantité Recommandée à Commander",
        "reco_details": "📋 Détails du Calcul",
        "stock_current": "Stock Actuel (unités)",
        "stock_title": "📊 Visualisation du Niveau de Stock Recommandé",
        "alert_low": "⚠️ Alerte: Le stock actuel ({current}) est inférieur au point de réapprovisionnement ({reorder}).",
        "alert_ok": "✅ Le stock actuel ({current}) est au-dessus du point de réapprovisionnement.",
        "stock_opt": "🎯 Optimisation des Stocks",
        "load_error": "❌ Impossible de charger les données",
        "pred_error": "❌ Impossible de générer les prédictions",
        "reco_error": "❌ Impossible de générer les recommandations",
        "load_warning": "⚠️ Veuillez charger les données depuis la barre latérale.",
        "data_loaded": "✅ Données chargées: {n:,} enregistrements",
    },
    "en": {
        "lang_label": "Language",
        "hero_badge": "Sales & inventory dashboard",
        "hero_title": "Sales analysis & inventory optimization",
        "hero_subtitle": "Pharma distribution — 30-day forecast with clear recommendations.",
        "hero_stack": "Prophet · Streamlit · Plotly",
        "sidebar_conf": "⚙️ Settings",
        "sidebar_data": "📊 Data",
        "reload": "🔄 Load/Reload Data",
        "data_missing": "❌ Data not found!",
        "data_hint": "💡 Run first: `python src/data_generator.py`",
        "product_select": "📦 Select a product",
        "lead_time": "Lead time (days)",
        "lead_help": "Time needed to receive a new order",
        "safety": "Safety factor",
        "safety_help": "Multiplier for safety stock",
        "selected_product": "Selected product",
        "tabs": ["📊 Historical Data", "🔮 Forecasts", "📈 Combined View", "💡 Recommendations"],
        "hist_title": "📊 Historical Sales Visualization",
        "hist_stats": "📈 Monthly Statistics",
        "hist_dist": "📊 Sales Distribution",
        "metric_total": "📊 Total Sales",
        "metric_avg": "📈 Avg Sales/Day",
        "metric_max": "⬆️ Max Sale/Day",
        "metric_period": "📅 Period (days)",
        "pred_title": "🔮 Sales Forecasts (30 days)",
        "pred_spinner": "🔄 Loading or training model...",
        "pred_avg": "📊 Avg Predicted/Day",
        "pred_total": "📈 Total Predicted (30 days)",
        "pred_peak": "⬆️ Peak Predicted",
        "pred_table": "📋 Forecast Details",
        "combined_title": "Full View: History & Forecasts",
        "reco_title": "💡 Stock Optimization Recommendations",
        "reco_spinner": "🔄 Computing recommendations...",
        "reco_product": "📦 Product",
        "reco_pred_demand": "📊 Predicted Demand (30 days)",
        "reco_reorder": "⏱️ Reorder Point",
        "reco_order": "🛒 Recommended Order Quantity",
        "reco_details": "📋 Calculation Details",
        "stock_current": "Current Stock (units)",
        "stock_title": "📊 Projected Stock Level",
        "alert_low": "⚠️ Alert: Current stock ({current}) is below reorder point ({reorder}).",
        "alert_ok": "✅ Current stock ({current}) is above the reorder point.",
        "stock_opt": "🎯 Inventory Optimization",
        "load_error": "❌ Unable to load data",
        "pred_error": "❌ Unable to generate forecasts",
        "reco_error": "❌ Unable to generate recommendations",
        "load_warning": "⚠️ Please load data from the sidebar.",
        "data_loaded": "✅ Data loaded: {n:,} rows",
    },
}


def tr(key: str, lang: str) -> str:
    return LANG_STRINGS.get(lang, LANG_STRINGS["fr"]).get(key, LANG_STRINGS["fr"].get(key, key))

# Ajouter le répertoire src au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.utils import load_data, calculate_reorder_point, get_product_name
from src.predictive_model import train_prophet_model, load_model, prepare_prophet_data

# Injection de styles pour un rendu moderne
def inject_styles():
    st.markdown(
        f"""
        <style>
        /* Mise en page aérée et fond clair */
        .block-container {{
            padding: 1.5rem 2rem 1.5rem 2rem;
            background: #f4f6fb;
            color: {TEXT_MAIN};
        }}
        /* Cartes génériques */
        .app-card {{
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.08);
        }}
        /* Bandeau héro */
        .hero {{
            background: linear-gradient(135deg, #eef2ff 0%, #e0f7f0 100%);
            color: {TEXT_MAIN};
            border-radius: 18px;
            padding: 18px 22px;
            box-shadow: 0 12px 35px rgba(0,0,0,0.12);
        }}
        /* Badges */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
            background: rgba(255,255,255,0.08);
            color: {TEXT_MAIN};
        }}
        /* Titres */
        h1, h2, h3, h4, h5 {{
            color: {TEXT_MAIN};
        }}
        .stTabs [data-baseweb="tab-list"] button {{
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            color: {TEXT_MAIN};
            margin-right: 6px;
        }}
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
            color: {TEXT_MAIN};
        }}
        .stTabs [aria-selected="true"] {{
            border-color: {PRIMARY};
            box-shadow: 0 8px 20px rgba(37,99,235,0.12);
        }}
        /* Tableaux */
        .stDataFrame {{
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }}
        /* Graphiques */
        .element-container:has(.plotly-chart) {{
            border-radius: 14px;
            border: 1px solid #e5e7eb;
            padding: 8px;
            background: #ffffff;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }}
        /* Inputs */
        .stSlider, .stNumberInput, .stSelectbox {{
            color: {TEXT_MAIN};
        }}
        /* Metrics lisibles */
        div[data-testid="stMetricValue"] {{
            color: {TEXT_MAIN} !important;
            opacity: 1 !important;
            font-weight: 700;
        }}
        div[data-testid="stMetricLabel"] {{
            color: {TEXT_MAIN} !important;
            opacity: 1 !important;
            font-weight: 600;
        }}
        div[data-testid="stMetricLabel"] p {{
            color: {TEXT_MAIN} !important;
            opacity: 1 !important;
        }}
        /* Renforcer les labels des métriques */
        div[data-testid="stMetric"] label {{
            color: {TEXT_MAIN} !important;
            opacity: 1 !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stMetric"] label div, 
        div[data-testid="stMetric"] label span {{
            color: {TEXT_MAIN} !important;
            opacity: 1 !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stMetric"] svg {{
            color: {TEXT_MAIN} !important;
            opacity: 0.9 !important;
        }}
        div[data-testid="stMetricDelta"] {{
            color: {ACCENT} !important;
            opacity: 1 !important;
        }}
        /* Alertes plus lisibles */
        .stAlert {{
            color: {TEXT_MAIN} !important;
            background: #f8fafc !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 10px !important;
        }}
        .stAlert p {{
            color: {TEXT_MAIN} !important;
            opacity: 1 !important;
        }}
        /* Forcer une police moderne et lisible */
        *, body {{
            font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Composant de métrique moderne
def metric_card(title: str, value: str, helper: str = "", color: str = PRIMARY):
    st.markdown(
        f"""
        <div class="app-card" style="border-left:4px solid {color}; margin-bottom:0.5rem;">
            <div style="color:{TEXT_MUTED}; font-size:12px; text-transform:uppercase; letter-spacing:0.5px;">{title}</div>
            <div style="color:{TEXT_MAIN}; font-size:24px; font-weight:700; margin:2px 0 4px 0;">{value}</div>
            <div style="color:{TEXT_MUTED}; font-size:12px;">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Configuration de la page
st.set_page_config(
    page_title="Analyse Prédictive des Ventes - Répartition Pharmaceutique",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliquer le style
inject_styles()

# Initialiser la langue avant tout affichage
if 'lang' not in st.session_state:
    st.session_state.lang = "fr"

# Titre principal
st.markdown(
    f"""
    <div class="hero">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
            <div>
                <div class="badge" style="background: rgba(37,99,235,0.12); color:{TEXT_MAIN};">{tr("hero_badge", st.session_state.lang)}</div>
                <h2 style="margin:6px 0 2px 0; color:{TEXT_MAIN};">{tr("hero_title", st.session_state.lang)}</h2>
                <div style="color:{TEXT_MUTED};">{tr("hero_subtitle", st.session_state.lang)}</div>
            </div>
            <div class="badge" style="background: rgba(16,185,129,0.12); color:{TEXT_MAIN};">{tr("hero_stack", st.session_state.lang)}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("")

# Internationalisation simple (FR/EN)
LANG_STRINGS = {
    "fr": {
        "lang_label": "Langue",
        "hero_badge": "Tableau de bord ventes & stocks",
        "hero_title": "Analyse des ventes & optimisation des stocks",
        "hero_subtitle": "Répartition pharmaceutique — prédiction 30 jours et recommandations claires.",
        "hero_stack": "Prophet · Streamlit · Plotly",
        "sidebar_conf": "⚙️ Configuration",
        "sidebar_data": "📊 Données",
        "reload": "🔄 Charger/Recharger les Données",
        "data_missing": "❌ Les données n'existent pas!",
        "data_hint": "💡 Exécutez d'abord: `python src/data_generator.py`",
        "product_select": "📦 Sélectionner un produit",
        "lead_time": "Délai de livraison (jours)",
        "lead_help": "Temps nécessaire pour recevoir une nouvelle commande",
        "safety": "Facteur de sécurité",
        "safety_help": "Facteur multiplicateur pour le stock de sécurité",
        "selected_product": "Produit sélectionné",
        "tabs": ["📊 Données Historiques", "🔮 Prédictions", "📈 Vue Combinée", "💡 Recommandations"],
        "hist_title": "📊 Visualisation des Ventes Historiques",
        "hist_stats": "📈 Statistiques Mensuelles",
        "hist_dist": "📊 Distribution des Ventes",
        "metric_total": "📊 Ventes Totales",
        "metric_avg": "📈 Ventes Moyennes/Jour",
        "metric_max": "⬆️ Vente Max/Jour",
        "metric_period": "📅 Période (jours)",
        "pred_title": "🔮 Prédictions des Ventes (30 jours)",
        "pred_spinner": "🔄 Chargement ou entraînement du modèle en cours...",
        "pred_avg": "📊 Vente Moyenne Prédite/Jour",
        "pred_total": "📈 Total Prédit (30 jours)",
        "pred_peak": "⬆️ Pic Prédit",
        "pred_table": "📋 Détails des Prédictions",
        "combined_title": "Vue Complète: Historique et Prédictions",
        "reco_title": "💡 Recommandations d'Optimisation des Stocks",
        "reco_spinner": "🔄 Calcul des recommandations...",
        "reco_product": "📦 Produit",
        "reco_pred_demand": "📊 Demande Prédite (30 jours)",
        "reco_reorder": "⏱️ Point de Réapprovisionnement",
        "reco_order": "🛒 Quantité Recommandée à Commander",
        "reco_details": "📋 Détails du Calcul",
        "stock_current": "Stock Actuel (unités)",
        "stock_title": "📊 Visualisation du Niveau de Stock Recommandé",
        "alert_low": "⚠️ Alerte: Le stock actuel ({current}) est inférieur au point de réapprovisionnement ({reorder}).",
        "alert_ok": "✅ Le stock actuel ({current}) est au-dessus du point de réapprovisionnement.",
    },
    "en": {
        "lang_label": "Language",
        "hero_badge": "Sales & inventory dashboard",
        "hero_title": "Sales analysis & inventory optimization",
        "hero_subtitle": "Pharma distribution — 30-day forecast with clear recommendations.",
        "hero_stack": "Prophet · Streamlit · Plotly",
        "sidebar_conf": "⚙️ Settings",
        "sidebar_data": "📊 Data",
        "reload": "🔄 Load/Reload Data",
        "data_missing": "❌ Data not found!",
        "data_hint": "💡 Run first: `python src/data_generator.py`",
        "product_select": "📦 Select a product",
        "lead_time": "Lead time (days)",
        "lead_help": "Time needed to receive a new order",
        "safety": "Safety factor",
        "safety_help": "Multiplier for safety stock",
        "selected_product": "Selected product",
        "tabs": ["📊 Historical Data", "🔮 Forecasts", "📈 Combined View", "💡 Recommendations"],
        "hist_title": "📊 Historical Sales Visualization",
        "hist_stats": "📈 Monthly Statistics",
        "hist_dist": "📊 Sales Distribution",
        "metric_total": "📊 Total Sales",
        "metric_avg": "📈 Avg Sales/Day",
        "metric_max": "⬆️ Max Sale/Day",
        "metric_period": "📅 Period (days)",
        "pred_title": "🔮 Sales Forecasts (30 days)",
        "pred_spinner": "🔄 Loading or training model...",
        "pred_avg": "📊 Avg Predicted/Day",
        "pred_total": "📈 Total Predicted (30 days)",
        "pred_peak": "⬆️ Peak Predicted",
        "pred_table": "📋 Forecast Details",
        "combined_title": "Full View: History & Forecasts",
        "reco_title": "💡 Stock Optimization Recommendations",
        "reco_spinner": "🔄 Computing recommendations...",
        "reco_product": "📦 Product",
        "reco_pred_demand": "📊 Predicted Demand (30 days)",
        "reco_reorder": "⏱️ Reorder Point",
        "reco_order": "🛒 Recommended Order Quantity",
        "reco_details": "📋 Calculation Details",
        "stock_current": "Current Stock (units)",
        "stock_title": "📊 Projected Stock Level",
        "alert_low": "⚠️ Alert: Current stock ({current}) is below reorder point ({reorder}).",
        "alert_ok": "✅ Current stock ({current}) is above the reorder point.",
    },
}


def tr(key: str, lang: str) -> str:
    return LANG_STRINGS.get(lang, LANG_STRINGS["fr"]).get(key, LANG_STRINGS["fr"].get(key, key))


# Initialisation de la session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'models_trained' not in st.session_state:
    st.session_state.models_trained = False


@st.cache_data
def load_sales_data(file_path: str = "data/processed/sales_aggregated.csv") -> pd.DataFrame:
    """
    Charge les données de ventes (mise en cache)
    """
    if os.path.exists(file_path):
        return load_data(file_path)
    return pd.DataFrame()


def load_or_train_model(product_id: str, data_df: pd.DataFrame) -> tuple:
    """
    Charge un modèle existant ou en entraîne un nouveau
    """
    model_path = f"models/prophet_model_{product_id}.pkl"
    
    if os.path.exists(model_path):
        try:
            model = load_model(model_path)
            # Préparer les données pour générer les prédictions
            prophet_df = prepare_prophet_data(data_df, product_id)
            future_dates = model.make_future_dataframe(periods=30)
            forecast = model.predict(future_dates)
            
            last_historical_date = prophet_df['ds'].max()
            future_forecast = forecast[forecast['ds'] > last_historical_date].copy()
            
            return model, forecast, prophet_df, future_forecast
        except Exception as e:
            st.warning(f"Erreur lors du chargement du modèle: {e}. Entraînement d'un nouveau modèle...")
    
    # Entraîner un nouveau modèle si aucun modèle n'existe
    try:
        model, forecast, historical = train_prophet_model(
            data_path="data/processed/sales_aggregated.csv",
            product_id=product_id,
            forecast_days=30
        )
        last_historical_date = historical['ds'].max()
        future_forecast = forecast[forecast['ds'] > last_historical_date].copy()
        return model, forecast, historical, future_forecast
    except Exception as e:
        st.error(f"Erreur lors de l'entraînement: {e}")
        return None, None, None, None


# Sidebar - Navigation et paramètres
with st.sidebar:
    st.header(tr("sidebar_conf", st.session_state.lang))
    
    # Section de chargement des données
    st.subheader(tr("sidebar_data", st.session_state.lang))
    
    # Sélecteur de langue
    lang_choice = st.radio(
        tr("lang_label", st.session_state.lang),
        options=["fr", "en"],
        format_func=lambda x: "Français" if x == "fr" else "English",
        horizontal=True,
    )
    st.session_state.lang = lang_choice
    
    if st.button(tr("reload", st.session_state.lang), use_container_width=True):
        st.session_state.data_loaded = False
        st.rerun()
    
    # Vérifier si les données existent
    data_path = "data/processed/sales_aggregated.csv"
    if not os.path.exists(data_path):
        st.error(tr("data_missing", st.session_state.lang))
        st.info(tr("data_hint", st.session_state.lang))
        st.stop()
    
    # Charger les données
    data_df = load_sales_data(data_path)
    
    if not data_df.empty:
        st.session_state.data_loaded = True
        st.success(tr("data_loaded", st.session_state.lang).format(n=len(data_df)))
        
        # Sélection du produit avec noms affichés
        products = sorted(data_df['product_id'].unique())
        # Créer un dictionnaire product_id -> product_name
        if 'product_name' in data_df.columns:
            product_names_dict = dict(zip(data_df['product_id'], data_df['product_name']))
            product_labels = [f"{product_names_dict.get(pid, get_product_name(pid))} ({pid})" for pid in products]
        else:
            product_labels = [f"{get_product_name(pid)} ({pid})" for pid in products]
        
        selected_index = st.selectbox(
            tr("product_select", st.session_state.lang),
            options=range(len(products)),
            format_func=lambda x: product_labels[x],
            index=0
        )
        selected_product = products[selected_index]
        
        # Afficher le nom complet du produit sélectionné
        if 'product_name' in data_df.columns:
            selected_product_name = product_names_dict.get(selected_product, get_product_name(selected_product))
        else:
            selected_product_name = get_product_name(selected_product)
        st.info(f"💊 **Produit sélectionné:** {selected_product_name}")
        
        # Paramètres d'optimisation
        st.subheader(tr("stock_opt", st.session_state.lang))
        lead_time = st.slider(
            tr("lead_time", st.session_state.lang),
            min_value=1,
            max_value=30,
            value=7,
            help=tr("lead_help", st.session_state.lang)
        )
        
        safety_factor = st.slider(
            tr("safety", st.session_state.lang),
            min_value=1.0,
            max_value=3.0,
            value=1.5,
            step=0.1,
            help=tr("safety_help", st.session_state.lang)
        )
    else:
        st.error(tr("load_error", st.session_state.lang))
        st.stop()


# Contenu principal
if st.session_state.data_loaded:
    # Obtenir le nom du produit sélectionné
    if 'product_name' in data_df.columns:
        selected_product_name = data_df[data_df['product_id'] == selected_product]['product_name'].iloc[0]
    else:
        selected_product_name = get_product_name(selected_product)
    
    # Afficher le titre avec le nom du produit
    st.markdown(f"### 💊 {selected_product_name}")
    st.markdown(f"*{tr('selected_product', st.session_state.lang)}: {selected_product}*")
    st.markdown("---")
    
    # Filtrer les données pour le produit sélectionné
    product_data = data_df[data_df['product_id'] == selected_product].copy()
    product_data = product_data.groupby('date')['quantity_sold'].sum().reset_index()
    product_data = product_data.sort_values('date')
    
    # Afficher les métriques clés
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = product_data['quantity_sold'].sum()
        st.metric(tr("metric_total", st.session_state.lang), f"{total_sales:,.0f}")
    
    with col2:
        avg_daily_sales = product_data['quantity_sold'].mean()
        st.metric(tr("metric_avg", st.session_state.lang), f"{avg_daily_sales:.1f}")
    
    with col3:
        max_daily_sales = product_data['quantity_sold'].max()
        st.metric(tr("metric_max", st.session_state.lang), f"{max_daily_sales:.0f}")
    
    with col4:
        date_range = (product_data['date'].max() - product_data['date'].min()).days
        st.metric(tr("metric_period", st.session_state.lang), f"{date_range}")
    
    st.markdown("---")
    
    # Onglets pour différentes vues
    tab1, tab2, tab3, tab4 = st.tabs(tr("tabs", st.session_state.lang))
    
    with tab1:
        st.subheader(tr("hist_title", st.session_state.lang))
        
        # Graphique des ventes historiques
        fig_hist = go.Figure()
        
        fig_hist.add_trace(go.Scatter(
            x=product_data['date'],
            y=product_data['quantity_sold'],
            mode='lines+markers',
            name='Ventes réelles',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=4)
        ))
        
        # Ligne de moyenne mobile (7 jours)
        product_data['moving_avg'] = product_data['quantity_sold'].rolling(window=7).mean()
        fig_hist.add_trace(go.Scatter(
            x=product_data['date'],
            y=product_data['moving_avg'],
            mode='lines',
            name='Moyenne mobile (7 jours)',
            line=dict(color='orange', width=2, dash='dash')
        ))
        
        fig_hist.update_layout(
            title="Évolution des Ventes Historiques",
            xaxis_title="Date",
            yaxis_title="Quantité Vendue",
            hovermode='x unified',
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Statistiques détaillées
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(tr("hist_stats", st.session_state.lang))
            product_data['year_month'] = product_data['date'].dt.to_period('M')
            monthly_stats = product_data.groupby('year_month')['quantity_sold'].agg(['sum', 'mean', 'std']).reset_index()
            monthly_stats['year_month'] = monthly_stats['year_month'].astype(str)
            st.dataframe(monthly_stats, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader(tr("hist_dist", st.session_state.lang))
            fig_dist = px.histogram(
                product_data,
                x='quantity_sold',
                nbins=30,
                title="Distribution des Quantités Vendues",
                labels={'quantity_sold': 'Quantité Vendue', 'count': 'Fréquence'}
            )
            st.plotly_chart(fig_dist, use_container_width=True)
    
    with tab2:
        st.subheader(tr("pred_title", st.session_state.lang))
        
        # Afficher un spinner pendant le chargement/entraînement
        with st.spinner(tr("pred_spinner", st.session_state.lang)):
            model, forecast, historical, future_forecast = load_or_train_model(selected_product, data_df)
        
        if model is not None and future_forecast is not None:
            # Graphique des prédictions
            fig_pred = go.Figure()
            
            # Données historiques
            fig_pred.add_trace(go.Scatter(
                x=historical['ds'],
                y=historical['y'],
                mode='lines+markers',
                name='Ventes historiques',
                line=dict(color='#1f77b4', width=2)
            ))
            
            # Prédictions
            fig_pred.add_trace(go.Scatter(
                x=future_forecast['ds'],
                y=future_forecast['yhat'],
                mode='lines+markers',
                name='Prédiction',
                line=dict(color='green', width=2, dash='dash')
            ))
            
            # Intervalle de confiance supérieur
            fig_pred.add_trace(go.Scatter(
                x=future_forecast['ds'],
                y=future_forecast['yhat_upper'],
                mode='lines',
                name='Limite supérieure (95%)',
                line=dict(width=0),
                showlegend=False
            ))
            
            # Intervalle de confiance inférieur
            fig_pred.add_trace(go.Scatter(
                x=future_forecast['ds'],
                y=future_forecast['yhat_lower'],
                mode='lines',
                name='Intervalle de confiance',
                fill='tonexty',
                fillcolor='rgba(0, 255, 0, 0.2)',
                line=dict(width=0)
            ))
            
            fig_pred.update_layout(
                title="Prédictions des Ventes avec Intervalles de Confiance",
                xaxis_title="Date",
                yaxis_title="Quantité Vendue",
                hovermode='x unified',
                height=500,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_pred, use_container_width=True)
            
            # Métriques de prédiction
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_predicted = future_forecast['yhat'].mean()
                st.metric(tr("pred_avg", st.session_state.lang), f"{avg_predicted:.1f}")
            
            with col2:
                total_predicted = future_forecast['yhat'].sum()
                st.metric(tr("pred_total", st.session_state.lang), f"{total_predicted:,.0f}")
            
            with col3:
                max_predicted = future_forecast['yhat'].max()
                st.metric(tr("pred_peak", st.session_state.lang), f"{max_predicted:.0f}")
            
            # Tableau des prédictions
            st.subheader(tr("pred_table", st.session_state.lang))
            forecast_display = future_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
            forecast_display.columns = ['Date', 'Prédiction', 'Limite Inférieure', 'Limite Supérieure']
            forecast_display['Prédiction'] = forecast_display['Prédiction'].round(1)
            forecast_display['Limite Inférieure'] = forecast_display['Limite Inférieure'].round(1)
            forecast_display['Limite Supérieure'] = forecast_display['Limite Supérieure'].round(1)
            st.dataframe(forecast_display, use_container_width=True, hide_index=True)
        else:
            st.error(tr("pred_error", st.session_state.lang))
    
    with tab3:
        st.subheader(tr("combined_title", st.session_state.lang))
        
        with st.spinner("🔄 Chargement des données..."):
            model, forecast, historical, future_forecast = load_or_train_model(selected_product, data_df)
        
        if model is not None:
            # Graphique combiné
            fig_combined = go.Figure()
            
            # Historique
            fig_combined.add_trace(go.Scatter(
                x=historical['ds'],
                y=historical['y'],
                mode='lines+markers',
                name='Ventes historiques',
                line=dict(color='#1f77b4', width=2)
            ))
            
            # Prédictions
            fig_combined.add_trace(go.Scatter(
                x=future_forecast['ds'],
                y=future_forecast['yhat'],
                mode='lines+markers',
                name='Prédiction',
                line=dict(color='green', width=2, dash='dash')
            ))
            
            # Intervalle de confiance
            fig_combined.add_trace(go.Scatter(
                x=future_forecast['ds'],
                y=future_forecast['yhat_upper'],
                mode='lines',
                name='Limite supérieure',
                line=dict(width=0),
                showlegend=False
            ))
            
            fig_combined.add_trace(go.Scatter(
                x=future_forecast['ds'],
                y=future_forecast['yhat_lower'],
                mode='lines',
                name='Intervalle de confiance (95%)',
                fill='tonexty',
                fillcolor='rgba(0, 255, 0, 0.2)',
                line=dict(width=0)
            ))
            
            # Ligne verticale pour séparer historique et prédictions
            last_historical_date = historical['ds'].max()
            # Utiliser add_shape au lieu de add_vline pour éviter l'erreur avec Timestamp
            # Convertir en datetime si nécessaire pour compatibilité Plotly
            if isinstance(last_historical_date, pd.Timestamp):
                last_date = last_historical_date
            else:
                last_date = pd.Timestamp(last_historical_date)
            
            fig_combined.add_shape(
                type="line",
                x0=last_date,
                x1=last_date,
                y0=0,
                y1=1,
                yref="paper",
                line=dict(color="red", width=2, dash="dot")
            )
            # Ajouter une annotation pour le texte
            fig_combined.add_annotation(
                x=last_date,
                y=1,
                yref="paper",
                text="Aujourd'hui",
                showarrow=False,
                xanchor="left",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="red",
                borderwidth=1
            )
            
            fig_combined.update_layout(
                title="Vue Complète: Historique et Prédictions",
                xaxis_title="Date",
                yaxis_title="Quantité Vendue",
                hovermode='x unified',
                height=600,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_combined, use_container_width=True)
    
    with tab4:
        st.subheader(tr("reco_title", st.session_state.lang))
        
        with st.spinner("🔄 Calcul des recommandations..."):
            model, forecast, historical, future_forecast = load_or_train_model(selected_product, data_df)
        
        if model is not None and future_forecast is not None:
            # Calculer la demande prédite totale pour 30 jours
            total_predicted_demand = future_forecast['yhat'].sum()
            avg_daily_predicted = future_forecast['yhat'].mean()
            
            # Calculer le point de réapprovisionnement
            reorder_point = calculate_reorder_point(
                predicted_demand=total_predicted_demand,
                lead_time_days=lead_time,
                safety_stock_factor=safety_factor
            )
            
            # Recommandation de commande
            recommended_order = max(0, round(reorder_point * 1.2))  # 20% de marge supplémentaire
            
            # Afficher les recommandations
            st.info(f"{tr('reco_product', st.session_state.lang)}: {get_product_name(selected_product)} ({selected_product})")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    tr("reco_pred_demand", st.session_state.lang),
                    f"{total_predicted_demand:,.0f} unités"
                )
            
            with col2:
                st.metric(
                    tr("reco_reorder", st.session_state.lang),
                    f"{reorder_point:,.0f} unités"
                )
            
            with col3:
                st.metric(
                    tr("reco_order", st.session_state.lang),
                    f"{recommended_order:,.0f} unités",
                    delta=f"+{recommended_order - reorder_point:.0f} unités"
                )
            
            # Détails du calcul
            with st.expander(tr("reco_details", st.session_state.lang)):
                st.markdown(f"""
                **Paramètres utilisés:**
                - Délai de livraison: {lead_time} jours
                - Facteur de sécurité: {safety_factor}x
                - Demande journalière moyenne prédite: {avg_daily_predicted:.1f} unités/jour
                
                **Calcul du point de réapprovisionnement:**
                ```
                Demande journalière = {avg_daily_predicted:.1f} unités/jour
                Besoin pendant le délai = {avg_daily_predicted:.1f} × {lead_time} = {avg_daily_predicted * lead_time:.1f} unités
                Stock de sécurité = {avg_daily_predicted * lead_time:.1f} × {safety_factor} = {reorder_point:.0f} unités
                ```
                
                **Recommandation:**
                - Commander **{recommended_order} unités** pour maintenir un stock optimal
                - Cette quantité couvre la demande prévue + délai de livraison + marge de sécurité
                """)
            
            # Graphique de visualisation du stock
            st.subheader(tr("stock_title", st.session_state.lang))
            
            # Simuler un niveau de stock actuel (exemple)
            current_stock = st.number_input(
                tr("stock_current", st.session_state.lang),
                min_value=0,
                value=int(reorder_point * 0.8),
                step=10
            )
            
            # Créer un graphique de niveau de stock
            stock_dates = pd.date_range(
                start=datetime.now(),
                periods=30,
                freq='D'
            )
            
            # Simuler l'évolution du stock
            stock_levels = []
            stock = current_stock
            daily_consumption = avg_daily_predicted
            
            for date in stock_dates:
                stock_levels.append(max(0, stock))
                stock = max(0, stock - daily_consumption)
            
            fig_stock = go.Figure()
            
            fig_stock.add_trace(go.Scatter(
                x=stock_dates,
                y=stock_levels,
                mode='lines+markers',
                name='Niveau de stock prévu',
                line=dict(color='blue', width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 0, 255, 0.1)'
            ))
            
            # Ligne du point de réapprovisionnement
            fig_stock.add_hline(
                y=reorder_point,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Point de réapprovisionnement ({reorder_point:.0f})"
            )
            
            # Ligne du stock de sécurité
            safety_stock = reorder_point / safety_factor
            fig_stock.add_hline(
                y=safety_stock,
                line_dash="dot",
                line_color="orange",
                annotation_text=f"Stock de sécurité ({safety_stock:.0f})"
            )
            
            fig_stock.update_layout(
                title="Évolution Prévue du Niveau de Stock",
                xaxis_title="Date",
                yaxis_title="Niveau de Stock (unités)",
                hovermode='x unified',
                height=400,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_stock, use_container_width=True)
            
            # Alerte si stock actuel est faible
            if current_stock < reorder_point:
                st.warning(tr("alert_low", st.session_state.lang).format(current=current_stock, reorder=f"{reorder_point:.0f}"))
            else:
                st.success(tr("alert_ok", st.session_state.lang).format(current=current_stock, reorder=f"{reorder_point:.0f}"))
        else:
            st.error(tr("reco_error", st.session_state.lang))
else:
        st.warning(tr("load_warning", st.session_state.lang))

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>Système d'Analyse Prédictive des Ventes - Répartition Pharmaceutique</p>
    <p>Prophet × Streamlit × Python</p>
    </div>
    """,
    unsafe_allow_html=True
)

