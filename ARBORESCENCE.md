# 📁 Arborescence Complète du Projet

## Structure des Répertoires et Fichiers

```
cnp_logicielle/
│
├── 📄 app.py                          # Application Streamlit principale
│   └── Interface utilisateur complète avec visualisations et recommandations
│
├── 📄 requirements.txt                # Dépendances Python (Prophet, Streamlit, etc.)
│
├── 📄 README.md                       # Documentation principale du projet
│
├── 📄 ARBORESCENCE.md                 # Ce fichier - structure du projet
│
├── 📄 .gitignore                      # Fichiers à ignorer par git
│
├── 📂 src/                            # Code source principal
│   ├── __init__.py                    # Module Python
│   ├── data_generator.py             # Génération de données simulées
│   ├── predictive_model.py           # Modèle Prophet pour prédictions
│   └── utils.py                       # Fonctions utilitaires
│
├── 📂 data/                           # Données du projet
│   ├── raw/                          # Données brutes générées
│   │   └── sales_data.csv            # (généré par data_generator.py)
│   └── processed/                    # Données traitées
│       └── sales_aggregated.csv      # (généré par data_generator.py)
│
├── 📂 models/                         # Modèles entraînés
│   └── prophet_model_PROD_XXX.pkl    # (générés par predictive_model.py)
│
├── 📂 notebooks/                      # Notebooks Jupyter pour exploration
│   └── (optionnel - pour analyses exploratoires)
│
└── 📂 config/                         # Fichiers de configuration
    └── config.yaml                    # Configuration centralisée
```

## 📋 Description des Fichiers Principaux

### 1. **app.py** (Application Streamlit)
- Interface utilisateur interactive
- Visualisation des ventes historiques
- Affichage des prédictions Prophet
- Recommandations d'optimisation des stocks
- Dashboard avec 4 onglets:
  - Données Historiques
  - Prédictions
  - Vue Combinée
  - Recommandations

### 2. **src/data_generator.py**
- Génère des données simulées réalistes
- Crée 2 ans de données historiques (2022-2024)
- 10 produits par défaut
- Inclut tendances, saisonnalité, variations hebdomadaires
- Exporte en CSV dans `data/raw/` et `data/processed/`

### 3. **src/predictive_model.py**
- Implémente le modèle Prophet
- Entraîne un modèle par produit
- Génère des prédictions sur 30 jours
- Sauvegarde les modèles dans `models/`
- Fonction pour entraîner tous les produits

### 4. **src/utils.py**
- Fonctions utilitaires réutilisables
- Chargement de données
- Calcul du point de réapprovisionnement
- Formatage et helpers

### 5. **requirements.txt**
- Liste complète des dépendances
- Prophet, Streamlit, Pandas, NumPy, Plotly, etc.

### 6. **config/config.yaml**
- Configuration centralisée
- Paramètres de génération de données
- Paramètres du modèle Prophet
- Paramètres d'optimisation des stocks

## 🚀 Workflow d'Utilisation

1. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

2. **Génération des données**
   ```bash
   python src/data_generator.py
   ```

3. **Entraînement des modèles** (optionnel - fait automatiquement par l'app)
   ```bash
   python src/predictive_model.py
   ```

4. **Lancement de l'application**
   ```bash
   streamlit run app.py
   ```

## 📊 Flux de Données

```
data_generator.py
    ↓
data/raw/sales_data.csv
    ↓
data/processed/sales_aggregated.csv
    ↓
predictive_model.py
    ↓
models/prophet_model_*.pkl
    ↓
app.py (Streamlit)
    ↓
Visualisations + Recommandations
```

## 🎯 Points Clés de l'Architecture

- **Modularité**: Code organisé en modules réutilisables
- **Séparation des préoccupations**: Génération, Modélisation, Visualisation
- **Extensibilité**: Facile d'ajouter de nouveaux produits ou fonctionnalités
- **Maintenabilité**: Code commenté et bien structuré








