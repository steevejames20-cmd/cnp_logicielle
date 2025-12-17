# Budgetis - Assistant budget personnel

## Structure
```
app/
  backend/
    api/ (routes FastAPI)
    core/ (config + DB)
    models/ (SQLAlchemy)
    schemas/ (Pydantic)
    main.py
  frontend/ (HTML/CSS/JS statiques)
```

## Installation rapide
```bash
cd app/backend
python -m venv .venv
.venv\\Scripts\\activate  # ou source .venv/bin/activate
pip install -r ../../requirements.txt
uvicorn app.backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Fonctionnalités
- Budgets avec limite free/premium
- Dépenses quotidiennes
- Objectifs d’épargne
- Conseils basiques (règles) et avancés (premium)
- Stats et projections simples
- Export CSV/PDF (premium)
- Auth JWT basique (register/login/status)
- Frontend statique minimal (5 pages)

## Endpoints clés
- Budgets: `POST/GET/PUT/DELETE /budget`
- Dépenses: `POST/GET /expense`, `GET /expense/by-budget/{id}`
- Épargne: `POST/GET/PUT/DELETE /saving-goal`
- Conseils: `GET /advice/basic`, `GET /advice/advanced`
- Stats: `GET /stats/summary`, `GET /stats/projection`
- Auth: `POST /auth/register`, `POST /auth/login`, `GET /auth/status`
- Export: `POST /export/csv`, `POST /export/pdf`

## Frontend
Ouvrir `app/frontend/index.html` dans le navigateur. Les pages utilisent `fetch()` vers `http://localhost:8000`.

## Notes premium/free
- Free: max 3 budgets, 1 objectif d’épargne, conseils basiques.
- Premium (is_premium=True via register): budgets illimités, conseils avancés, exports.

## Variables d’environnement
Créer un `.env` à la racine backend si besoin:
```
DATABASE_URL=sqlite:///./budgetis.db
SECRET_KEY=change-me
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## Tests rapides via curl
```bash
curl -X POST http://localhost:8000/budget -H \"Content-Type: application/json\" \\
  -d '{\"name\":\"Maison\",\"amount\":1200,\"period\":\"monthly\"}'
curl http://localhost:8000/advice/basic
```

# Budgetis - Assistant budget personnel

## Structure
```
app/
  backend/
    api/ (routes FastAPI)
    core/ (config + DB)
    models/ (SQLAlchemy)
    schemas/ (Pydantic)
    main.py
  frontend/ (HTML/CSS/JS statiques)
```

## Installation rapide
```bash
cd app/backend
python -m venv .venv
.venv\\Scripts\\activate  # ou source .venv/bin/activate
pip install -r ../../requirements.txt
uvicorn app.backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Fonctionnalités
- Budgets avec limite free/premium
- Dépenses quotidiennes
- Objectifs d’épargne
- Conseils basiques (règles) et avancés (premium)
- Stats et projections simples
- Export CSV/PDF (premium)
- Auth JWT basique (register/login/status)
- Frontend statique minimal (5 pages)

## Endpoints clés
- Budgets: `POST/GET/PUT/DELETE /budget`
- Dépenses: `POST/GET /expense`, `GET /expense/by-budget/{id}`
- Épargne: `POST/GET/PUT/DELETE /saving-goal`
- Conseils: `GET /advice/basic`, `GET /advice/advanced`
- Stats: `GET /stats/summary`, `GET /stats/projection`
- Auth: `POST /auth/register`, `POST /auth/login`, `GET /auth/status`
- Export: `POST /export/csv`, `POST /export/pdf`

## Frontend
Ouvrir `app/frontend/index.html` dans le navigateur. Les pages utilisent `fetch()` vers `http://localhost:8000`.

## Notes premium/free
- Free: max 3 budgets, 1 objectif d’épargne, conseils basiques.
- Premium (is_premium=True via register): budgets illimités, conseils avancés, exports.

## Variables d’environnement
Créer un `.env` à la racine backend si besoin:
```
DATABASE_URL=sqlite:///./budgetis.db
SECRET_KEY=change-me
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

## Tests rapides via curl
```bash
curl -X POST http://localhost:8000/budget -H \"Content-Type: application/json\" \\
  -d '{\"name\":\"Maison\",\"amount\":1200,\"period\":\"monthly\"}'
curl http://localhost:8000/advice/basic
```

# Système d'Analyse Prédictive et de Visualisation des Ventes
## Optimisation de la Gestion des Stocks - Répartition Pharmaceutique

### 📋 Description du Projet
Ce projet implémente un système d'analyse prédictive utilisant Prophet pour prédire les ventes futures et optimiser la gestion des stocks dans une entreprise de répartition pharmaceutique. L'interface utilisateur est développée avec Streamlit pour une visualisation interactive.

### 🏗️ Arborescence du Projet

```
cnp_logicielle/
│
├── app.py                          # Application Streamlit principale
├── requirements.txt                # Dépendances Python
├── README.md                       # Documentation du projet
│
├── src/                            # Code source principal
│   ├── __init__.py
│   ├── data_generator.py          # Génération de données simulées
│   ├── predictive_model.py        # Modèle Prophet pour prédictions
│   └── utils.py                   # Fonctions utilitaires
│
├── data/                           # Données du projet
│   ├── raw/                       # Données brutes
│   ├── processed/                 # Données traitées
│   └── .gitkeep                   # Maintient le dossier dans git
│
├── models/                         # Modèles entraînés
│   └── .gitkeep
│
├── notebooks/                      # Notebooks Jupyter pour exploration
│   └── .gitkeep
│
├── config/                         # Fichiers de configuration
│   └── config.yaml
│
└── .gitignore                      # Fichiers à ignorer par git
```

### 📦 Installation

1. **Cloner le dépôt** (si applicable)
2. **Créer un environnement virtuel**:
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Installer les dépendances**:
   ```bash
   pip install -r requirements.txt
   ```

### 🚀 Utilisation

#### 1. Générer des données simulées
```bash
python src/data_generator.py
```

#### 2. Entraîner le modèle de prédiction
```bash
python src/predictive_model.py
```

#### 3. Lancer l'application Streamlit
```bash
streamlit run app.py
```

### 📊 Plan d'Implémentation

#### Phase 1: Préparation de l'environnement
- [x] Création de l'arborescence du projet
- [x] Configuration des dépendances
- [x] Mise en place de la structure de base

#### Phase 2: Génération de données
- [ ] Implémentation du générateur de données simulées
- [ ] Création de données historiques réalistes (2 ans de données)
- [ ] Export des données au format CSV

#### Phase 3: Modèle de prédiction
- [ ] Implémentation du modèle Prophet
- [ ] Entraînement sur les données historiques
- [ ] Génération de prédictions (30 jours)
- [ ] Sauvegarde du modèle entraîné

#### Phase 4: Application Streamlit
- [ ] Interface de chargement des données
- [ ] Visualisation des ventes historiques
- [ ] Affichage des prédictions
- [ ] Recommandations d'optimisation des stocks
- [ ] Dashboard interactif

#### Phase 5: Optimisation des stocks
- [ ] Calcul des niveaux de réapprovisionnement
- [ ] Recommandations de commandes
- [ ] Alertes de stock faible

### 🛠️ Technologies Utilisées

- **Python 3.8+**
- **Streamlit**: Interface utilisateur interactive
- **Prophet**: Modèle de prédiction de séries temporelles
- **Pandas**: Manipulation de données
- **NumPy**: Calculs numériques
- **Matplotlib/Plotly**: Visualisations

### 📝 Notes

- Les données sont simulées pour des besoins de démonstration
- Le modèle Prophet nécessite des données avec une tendance claire
- Les prédictions sont générées pour 30 jours à l'avance
- Les recommandations de stock sont basées sur les prédictions et un délai de réapprovisionnement







