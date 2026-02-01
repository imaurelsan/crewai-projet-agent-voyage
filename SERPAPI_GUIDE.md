# 🔍 Guide d'installation SerpAPI (Optionnel)

## Qu'est-ce que SerpAPI?

SerpAPI est un service qui permet de faire des **recherches Google avancées** via une API. 

### 🆚 Comparaison: DuckDuckGo vs SerpAPI

| Critère | DuckDuckGo (gratuit) | SerpAPI (premium) |
|---------|---------------------|-------------------|
| **Prix** | ✅ Gratuit, illimité | 💰 100 gratuit/mois, puis payant |
| **Qualité** | ⚠️ Basique | ✅ Excellente (Google) |
| **Précision** | ⚠️ Moyenne | ✅ Très précise |
| **Temps réel** | ❌ Non | ✅ Oui |
| **Configuration** | ✅ Aucune | ⚠️ Clé API requise |

## 📝 Pourquoi ajouter SerpAPI?

### Avantages:
- ✅ **Meilleure qualité** de résultats pour les attractions touristiques
- ✅ **Plus précis** pour trouver restaurants, hôtels, activités
- ✅ **Résultats en temps réel** (prix, disponibilités)
- ✅ **100 recherches gratuites** par mois (suffisant pour tester)

### Inconvénients:
- ⚠️ Nécessite une inscription
- ⚠️ Limité à 100 recherches/mois (version gratuite)
- ⚠️ Payant au-delà (à partir de $50/mois pour 5000 recherches)

## 🚀 Installation (5 minutes)

### Étape 1: Créer un compte

1. Allez sur [https://serpapi.com/](https://serpapi.com/)
2. Cliquez sur **"Get Free API Key"**
3. Créez un compte avec votre email
4. Confirmez votre email

### Étape 2: Obtenir votre clé API

1. Connectez-vous à votre compte SerpAPI
2. Allez dans **Dashboard** (tableau de bord)
3. Copiez votre **API Key** (ressemble à: `abc123def456...`)

### Étape 3: Configurer le projet

1. Ouvrez le fichier `.env` à la racine du projet
   ```powershell
   notepad .env
   ```

2. Ajoutez votre clé API:
   ```env
   SERPAPI_API_KEY=votre_clé_api_ici
   ```

3. Sauvegardez le fichier

### Étape 4: Vérifier l'installation

Lancez le test:
```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Clé SerpAPI:', 'Configurée ✅' if os.getenv('SERPAPI_API_KEY') else 'Non configurée ❌')"
```

## 📊 Quota et limites

### Plan Gratuit (Free)
- ✅ 100 recherches par mois
- ✅ Toutes les fonctionnalités
- ✅ Support email
- ⚠️ Pas de carte de crédit requise

### Comment vérifier votre quota?

1. Allez sur [https://serpapi.com/dashboard](https://serpapi.com/dashboard)
2. Regardez **"Searches this month"**
3. Le quota se réinitialise chaque mois

## 🔧 Utilisation dans le projet

### Avec SerpAPI configuré:

L'outil `search_web_serpapi` sera utilisé automatiquement:

```python
from src.tools import search_web_serpapi

# Recherche Google avancée
result = search_web_serpapi.invoke({
    "query": "meilleures attractions Paris",
    "num_results": 5
})
```

### Sans SerpAPI:

Le système utilise `search_web` (DuckDuckGo) par défaut:

```python
from src.tools import search_web

# Recherche DuckDuckGo (toujours disponible)
result = search_web.invoke({
    "query": "meilleures attractions Paris",
    "num_results": 5
})
```

## ⚠️ Sécurité

### ❌ Ne jamais faire:
- Commit le fichier `.env` sur GitHub
- Partager votre clé API publiquement
- Utiliser la même clé sur plusieurs projets publics

### ✅ Bonnes pratiques:
- Gardez `.env` dans `.gitignore` (déjà fait)
- Utilisez `.env.example` pour documenter (sans clés réelles)
- Régénérez votre clé si compromise

## 🆘 Dépannage

### Erreur: "Invalid API key"
**Solution:** Vérifiez que la clé est correcte dans `.env`

### Erreur: "Quota exceeded"
**Solution:** Vous avez dépassé 100 recherches ce mois. Options:
1. Attendre le mois suivant
2. Passer au plan payant
3. Utiliser DuckDuckGo (gratuit)

### Erreur: "Module 'serpapi' not found"
**Solution:** SerpAPI n'est pas une dépendance. Nous utilisons `requests` directement:
```powershell
pip install requests
```

## 💡 Conseils

### Pour débutants:
- ✅ Commencez **sans** SerpAPI (DuckDuckGo suffit pour apprendre)
- ✅ Ajoutez SerpAPI **plus tard** si vous voulez de meilleurs résultats
- ✅ Testez d'abord avec le crew de base

### Pour production:
- ✅ Utilisez SerpAPI pour de vrais projets
- ✅ Surveillez votre quota mensuel
- ✅ Considérez un plan payant si >100 recherches/mois

## 📚 Ressources

- **Documentation officielle:** [https://serpapi.com/docs](https://serpapi.com/docs)
- **Dashboard:** [https://serpapi.com/dashboard](https://serpapi.com/dashboard)
- **Pricing:** [https://serpapi.com/pricing](https://serpapi.com/pricing)

---

**Question?** Consultez la [documentation SerpAPI](https://serpapi.com/docs) ou utilisez DuckDuckGo (toujours gratuit!)
