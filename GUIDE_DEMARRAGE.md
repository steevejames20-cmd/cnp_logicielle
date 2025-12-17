# 🚀 Guide de Démarrage Rapide

## ✅ Installation Terminée !

Tous les packages ont été installés avec succès. Environnement  prêt à l'emploi.

## 📋 Packages Installés

- ✅ Streamlit 1.52.1
- ✅ Prophet 1.2.1
- ✅ Pandas 2.3.3
- ✅ NumPy 2.3.5
- ✅ Plotly 6.5.0
- ✅ Matplotlib 3.10.7
- ✅ Seaborn 0.13.2
- ✅ Et toutes les dépendances nécessaires

## 🎯 Prochaines Étapes

### 1. Les données sont déjà générées ✅
Les données simulées ont été créées dans :
- `data/raw/sales_data.csv` (7,310 enregistrements)
- `data/processed/sales_aggregated.csv`

### 2. Lancer l'application Streamlit

Ouvrez un terminal dans le dossier du projet et exécutez :

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

### 3. Utiliser l'application

Une fois l'application lancée :

1. **Sélectionner un produit** dans le menu déroulant de la barre latérale
2. **Explorer les onglets** :
   - 📊 **Données Historiques** : Visualiser les ventes passées
   - 🔮 **Prédictions** : Voir les prévisions sur 30 jours
   - 📈 **Vue Combinée** : Historique + Prédictions ensemble
   - 💡 **Recommandations** : Conseils d'optimisation des stocks

3. **Ajuster les paramètres** dans la barre latérale :
   - Délai de livraison (jours)
   - Facteur de sécurité

### 4. Entraîner les modèles pour tous les produits (optionnel)

Si vous voulez entraîner les modèles pour tous les produits d'avance :

```bash
python src/predictive_model.py
```

Les modèles seront sauvegardés dans le dossier `models/`

## 🔧 Commandes Utiles

### Régénérer les données
```bash
python src/data_generator.py
```

### Tester le modèle
```bash
python -c "from src.predictive_model import train_prophet_model; train_prophet_model()"
```

### Vérifier les packages
```bash
pip list | findstr "streamlit prophet pandas"
```

## 📊 Structure des Données

Les données générées contiennent :
- **10 produits** (PROD_001 à PROD_010)
- **2 ans de données** (2022-01-01 à 2024-01-01)
- **Tendances et saisonnalité** réalistes
- **Variations hebdomadaires** (moins de ventes le week-end)

## ⚠️ Notes Importantes

- Les données sont **simulées** pour la démonstration
- Les modèles sont entraînés **automatiquement** lors de l'utilisation de l'app
- Les prédictions sont générées pour **30 jours** à l'avance
- Les recommandations de stock sont basées sur les prédictions et les paramètres configurés

## 🆘 En Cas de Problème

1. **L'application ne démarre pas** :
   - Vérifiez que Streamlit est installé : `pip show streamlit`
   - Réinstallez si nécessaire : `pip install streamlit`

2. **Erreur avec Prophet** :
   - Vérifiez que cmdstanpy est installé : `pip show cmdstanpy`
   - Le premier entraînement peut prendre quelques secondes

3. **Données manquantes** :
   - Régénérez les données : `python src/data_generator.py`

## 🎉 Prêt à Commencer !

Lancez simplement `streamlit run app.py` et explorez votre système d'analyse prédictive !








