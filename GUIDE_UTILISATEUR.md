# 📖 Guide Utilisateur - Système d'Analyse Prédictive des Ventes

## 🎯 Vue d'Ensemble

Votre outil est un **système d'analyse prédictive et de visualisation des ventes** spécialement conçu pour optimiser la gestion des stocks dans une entreprise de répartition pharmaceutique. Il utilise l'intelligence artificielle (modèle Prophet) pour prédire les ventes futures et vous donner des recommandations précises pour gérer vos stocks.

---

## 🚀 Ce Que Votre Outil Peut Faire

### 1. **Analyse des Ventes Historiques** 📊
- Visualiser l'évolution des ventes sur 2 ans (2022-2024)
- Analyser les tendances et les patterns de vente
- Identifier les périodes de forte/faible demande
- Calculer des statistiques détaillées (moyennes, maximums, distributions)

### 2. **Prédiction des Ventes Futures** 🔮
- Prédire les ventes pour les **30 prochains jours**
- Utiliser l'intelligence artificielle (modèle Prophet)
- Afficher des intervalles de confiance (précision des prédictions)
- Prendre en compte les saisonnalités et tendances

### 3. **Optimisation des Stocks** 💡
- Calculer automatiquement le **point de réapprovisionnement**
- Recommander les quantités à commander
- Simuler l'évolution du stock dans le temps
- Générer des alertes si le stock est trop bas

### 4. **Visualisation Interactive** 📈
- Graphiques interactifs (zoom, survol pour voir les détails)
- Comparaison historique vs prédictions
- Visualisation de l'évolution du stock

---

## 🎮 Actions Que Vous Pouvez Effectuer

### **Dans la Barre Latérale (Sidebar) ⚙️**

#### 1. **Charger/Recharger les Données** 🔄
- **Bouton:** "🔄 Charger/Recharger les Données"
- **Action:** Actualise les données depuis les fichiers CSV
- **Quand l'utiliser:** Après avoir régénéré les données ou modifié les fichiers

#### 2. **Sélectionner un Produit** 📦
- **Menu déroulant:** Liste de tous les produits disponibles
- **Produits disponibles:**
  - Efferalgan 1000mg
  - Doliprane 1000mg
  - Spasfon Lyoc 80mg
  - Smecta 3g
  - Ibuprofene 400mg
  - Paracetamol 500mg
  - Aspirine 500mg
  - Strepsils Miel Citron
  - Humex Rhume
  - Actifed Rhume
- **Action:** Change le produit analysé dans toute l'application

#### 3. **Configurer le Délai de Livraison** ⏱️
- **Curseur:** "Délai de livraison (jours)"
- **Plage:** 1 à 30 jours
- **Valeur par défaut:** 7 jours
- **Action:** Ajuste le calcul du point de réapprovisionnement
- **Impact:** Plus le délai est long, plus le stock de sécurité recommandé est élevé

#### 4. **Ajuster le Facteur de Sécurité** 🛡️
- **Curseur:** "Facteur de sécurité"
- **Plage:** 1.0 à 3.0
- **Valeur par défaut:** 1.5
- **Action:** Modifie la marge de sécurité pour les stocks
- **Impact:** Plus le facteur est élevé, plus vous avez de stock de sécurité

---

### **Dans la Zone Principale (4 Onglets)**

#### **Onglet 1: 📊 Données Historiques**

**Ce que vous voyez:**
- **Graphique principal:** Évolution des ventes avec ligne de moyenne mobile (7 jours)
- **Statistiques mensuelles:** Tableau avec somme, moyenne et écart-type par mois
- **Distribution des ventes:** Histogramme montrant la fréquence des quantités vendues

**Actions possibles:**
- ✅ **Zoomer** sur le graphique (cliquer et glisser)
- ✅ **Survoler** les points pour voir les valeurs exactes
- ✅ **Télécharger** les données (via le menu du graphique Plotly)
- ✅ **Analyser** les tendances saisonnières
- ✅ **Identifier** les pics et creux de vente

**Métriques affichées en haut:**
- 📊 **Ventes Totales:** Somme de toutes les ventes historiques
- 📈 **Ventes Moyennes/Jour:** Moyenne quotidienne
- ⬆️ **Vente Max/Jour:** Pic de vente le plus élevé
- 📅 **Période (jours):** Nombre de jours de données disponibles

---

#### **Onglet 2: 🔮 Prédictions**

**Ce que vous voyez:**
- **Graphique de prédiction:** 
  - Ligne bleue = Ventes historiques réelles
  - Ligne verte pointillée = Prédictions pour 30 jours
  - Zone verte = Intervalle de confiance à 95%
- **Tableau détaillé:** Prédictions jour par jour avec limites inférieure/supérieure
- **Métriques de prédiction:**
  - 📊 Vente Moyenne Prédite/Jour
  - 📈 Total Prédit (30 jours)
  - ⬆️ Pic Prédit

**Actions possibles:**
- ✅ **Voir** les prédictions jour par jour dans le tableau
- ✅ **Analyser** l'intervalle de confiance (précision des prédictions)
- ✅ **Comparer** les prédictions avec l'historique
- ✅ **Exporter** les prédictions (via le menu Plotly)

**Note:** Le modèle s'entraîne automatiquement la première fois (peut prendre quelques secondes)

---

#### **Onglet 3: 📈 Vue Combinée**

**Ce que vous voyez:**
- **Graphique complet:** Historique + Prédictions sur un seul graphique
- **Ligne rouge pointillée:** Marque la séparation entre historique et prédictions ("Aujourd'hui")
- **Vue d'ensemble:** Permet de voir la continuité entre passé et futur

**Actions possibles:**
- ✅ **Visualiser** la transition historique → prédictions
- ✅ **Identifier** si les prédictions suivent la tendance historique
- ✅ **Zoomer** sur des périodes spécifiques
- ✅ **Analyser** la cohérence des prédictions

---

#### **Onglet 4: 💡 Recommandations**

**Ce que vous voyez:**

1. **Informations du Produit:**
   - Nom du produit sélectionné
   - ID du produit

2. **Trois Métriques Clés:**
   - 📊 **Demande Prédite (30 jours):** Total des ventes attendues
   - ⏱️ **Point de Réapprovisionnement:** Seuil en dessous duquel il faut commander
   - 🛒 **Quantité Recommandée à Commander:** Quantité exacte à commander

3. **Détails du Calcul** (expandable):
   - Explication détaillée des calculs
   - Formules utilisées
   - Paramètres pris en compte

4. **Visualisation du Stock:**
   - Graphique montrant l'évolution prévue du stock sur 30 jours
   - Ligne rouge = Point de réapprovisionnement
   - Ligne orange = Stock de sécurité
   - Zone bleue = Niveau de stock prévu

5. **Champ de Saisie:**
   - **Stock Actuel:** Entrez votre stock actuel pour voir la simulation

**Actions possibles:**
- ✅ **Entrer** votre stock actuel pour voir la simulation
- ✅ **Ajuster** les paramètres (délai, facteur) dans la sidebar pour voir l'impact
- ✅ **Lire** les détails du calcul pour comprendre la logique
- ✅ **Voir** l'alerte si le stock est trop bas (message rouge)
- ✅ **Utiliser** la quantité recommandée pour passer vos commandes

**Alertes automatiques:**
- ⚠️ **Alerte Rouge:** Si le stock actuel < point de réapprovisionnement
- ✅ **Message Vert:** Si le stock est suffisant

---

## 📋 Workflow Recommandé

### **Pour une Analyse Complète:**

1. **Sélectionnez un produit** dans la sidebar
2. **Consultez l'onglet "Données Historiques"** pour comprendre les tendances passées
3. **Allez dans "Prédictions"** pour voir les prévisions à 30 jours
4. **Vérifiez la "Vue Combinée"** pour la continuité historique/prédictions
5. **Consultez "Recommandations"** pour:
   - Entrer votre stock actuel
   - Voir la quantité à commander
   - Lire les détails du calcul
6. **Ajustez les paramètres** (délai, facteur) si nécessaire
7. **Utilisez les recommandations** pour passer vos commandes

### **Pour une Analyse Rapide:**

1. Sélectionnez le produit
2. Allez directement dans "Recommandations"
3. Entrez votre stock actuel
4. Notez la quantité recommandée à commander

---

## 💡 Cas d'Usage Pratiques

### **Cas 1: Vérification Quotidienne des Stocks**
- Ouvrez l'application
- Sélectionnez chaque produit un par un
- Allez dans "Recommandations"
- Entrez le stock actuel
- Notez les produits qui nécessitent une commande (alerte rouge)

### **Cas 2: Analyse de Tendances**
- Sélectionnez un produit
- Consultez "Données Historiques"
- Identifiez les périodes de forte demande
- Comparez avec les prédictions dans "Vue Combinée"

### **Cas 3: Planification des Commandes**
- Sélectionnez tous vos produits importants
- Notez les quantités recommandées dans "Recommandations"
- Ajustez le délai de livraison selon vos fournisseurs
- Utilisez ces données pour créer votre bon de commande

### **Cas 4: Analyse de Performance**
- Comparez les prédictions avec les ventes réelles (après 30 jours)
- Ajustez le facteur de sécurité si nécessaire
- Analysez les statistiques mensuelles pour identifier les patterns

---

## 🔧 Fonctionnalités Techniques

### **Modèle de Prédiction:**
- **Algorithme:** Prophet (Facebook)
- **Période de prédiction:** 30 jours
- **Précision:** Intervalle de confiance à 95%
- **Prise en compte:** Tendances, saisonnalité hebdomadaire et annuelle

### **Calcul du Point de Réapprovisionnement:**
```
Point de Réapprovisionnement = (Demande Journalière × Délai de Livraison) × Facteur de Sécurité
```

### **Recommandation de Commande:**
```
Quantité à Commander = Point de Réapprovisionnement × 1.2 (marge de 20%)
```

---

## ⚠️ Notes Importantes

1. **Données Simulées:** Les données actuelles sont simulées pour la démonstration
2. **Premier Entraînement:** Le modèle peut prendre quelques secondes à s'entraîner la première fois
3. **Modèles Sauvegardés:** Les modèles entraînés sont sauvegardés dans `models/` pour accélérer les prochaines utilisations
4. **Actualisation:** Rechargez les données si vous modifiez les fichiers CSV

---

## 🎯 Résumé des Actions Disponibles

| Action | Où | Description |
|--------|-----|------------|
| 🔄 Recharger données | Sidebar | Actualise les données |
| 📦 Sélectionner produit | Sidebar | Change le produit analysé |
| ⏱️ Ajuster délai | Sidebar | Modifie le délai de livraison (1-30 jours) |
| 🛡️ Ajuster sécurité | Sidebar | Modifie le facteur de sécurité (1.0-3.0) |
| 📊 Voir historique | Onglet 1 | Analyse les ventes passées |
| 🔮 Voir prédictions | Onglet 2 | Prédictions à 30 jours |
| 📈 Vue combinée | Onglet 3 | Historique + Prédictions |
| 💡 Voir recommandations | Onglet 4 | Calculs d'optimisation des stocks |
| 📝 Entrer stock actuel | Onglet 4 | Simule l'évolution du stock |
| 🔍 Zoomer graphiques | Tous onglets | Interaction avec les graphiques Plotly |
| 📥 Exporter données | Graphiques | Télécharger via menu Plotly |

---

## 🚀 Prêt à Utiliser!

Votre outil est maintenant prêt. Lancez-le avec `streamlit run app.py` et commencez à optimiser votre gestion des stocks!

---

# 📌 Emplacement du guide
Ce guide est enregistré sur votre PC ici : `C:\Users\DELL\cnp_logicielle\GUIDE_UTILISATEUR.md`

---

# 🚀 Améliorations possibles (roadmap rapide)
- Ajout d’un upload de données réelles (CSV) depuis l’interface Streamlit.
- Intégration d’une alerte email/Teams/Slack quand le stock passe sous le seuil.
- Prise en compte des délais fournisseurs par produit (et non global).
- Ajout d’un coût de stockage et d’un coût de rupture pour optimiser le stock de sécurité.
- Versionner les modèles par date d’entraînement et exposer un bouton “réentraîner”.
- Export des recommandations au format Excel/CSV directement depuis l’onglet Recommandations.
- Ajout d’un comparatif “prédictions vs ventes réelles” pour mesurer l’erreur.

---

# 🧭 Réalisation du projet (bref et précis)
**Objectif :** prédire les ventes à 30 jours et recommander quoi commander pour éviter les ruptures tout en limitant le stock inutile.  
**Données :** séries temporelles de ventes (date, produit, quantité).  
**Modèle :** Prophet (détection de tendance + saisonnalité hebdo/annuelle + intervalles de confiance).  
**Stack :** Python, Streamlit (UI), Plotly (graphiques), Pandas (traitement), Prophet (prédiction).  
**Fonctionnement :**  
1) `src/data_generator.py` génère/agrège des données (ou on peut charger les vôtres).  
2) `src/predictive_model.py` entraîne Prophet par produit et peut sauvegarder les modèles.  
3) `app.py` charge les données, entraîne/charge Prophet à la volée, affiche historique, prédictions, recommandations de stock.  

---

# 🛠️ Mode d’emploi simplifié
1) **Installer les dépendances** (déjà fait) : `pip install -r requirements.txt`  
2) **Générer ou charger vos données** :  
   - Générer (démo) : `python src/data_generator.py`  
   - Ou remplacer `data/raw/sales_data.csv` par vos ventes (colonnes : `date,product_id,product_name?,quantity_sold`).  
3) **Lancer l’app** : `streamlit run app.py` (ouvre le navigateur).  
4) **Dans l’app** :  
   - Choisir un produit (nom réel affiché).  
   - Ajuster délai de livraison et facteur de sécurité (sidebar).  
   - Onglet **Prédictions** : voir la demande à 30 jours.  
   - Onglet **Recommandations** : entrer votre stock actuel, lire la quantité à commander et les alertes.  
5) **Exporter** : via le menu Plotly (télécharger les graphes) ou ajouter un export CSV (amélioration proposée).  

En cas de doute : relancer `python src/data_generator.py`, puis `streamlit run app.py`.

