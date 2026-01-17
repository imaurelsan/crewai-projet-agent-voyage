# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer à ce projet ! Voici comment vous pouvez aider.

## 📋 Comment contribuer ?

### 🐛 Signaler un bug

1. Vérifier que le bug n'a pas déjà été signalé dans les [Issues](../../issues)
2. Ouvrir une nouvelle issue avec le template "Bug Report"
3. Inclure :
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu vs actuel
   - Version de Python et Ollama
   - Message d'erreur complet

### 💡 Proposer une fonctionnalité

1. Ouvrir une issue avec le template "Feature Request"
2. Expliquer :
   - Le besoin / problème à résoudre
   - La solution proposée
   - Les alternatives envisagées

### 🔧 Soumettre du code

#### 1. Fork et clone

```bash
# Fork sur GitHub
# Puis cloner votre fork
git clone https://github.com/<votre-username>/crewai-projet-agent-voyage.git
cd crewai-projet-agent-voyage
```

#### 2. Créer une branche

```bash
git checkout -b feature/ma-fonctionnalite
# ou
git checkout -b fix/mon-correctif
```

#### 3. Installer en mode développement

```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### 4. Faire vos modifications

- Suivre le style de code existant
- Commenter le code complexe
- Ajouter des docstrings aux fonctions

#### 5. Tester

```powershell
# Tester les agents
python exemple_simple.py
python agent_meteo.py
python src/crew_voyage.py

# Vérifier qu'il n'y a pas d'erreurs
```

#### 6. Commit

```bash
git add .
git commit -m "type: Description courte

Description détaillée si nécessaire."
```

**Types de commit :**
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage (pas de changement de code)
- `refactor:` Refactoring
- `test:` Ajout de tests
- `chore:` Maintenance

**Exemples :**
```
feat: Ajout agent de transport avec calcul d'itinéraire
fix: Correction timeout API météo (15s → 30s)
docs: Ajout section FAQ dans GUIDE_DEVELOPPEMENT.md
```

#### 7. Push et Pull Request

```bash
git push origin feature/ma-fonctionnalite
```

Sur GitHub :
1. Aller sur votre fork
2. Cliquer "Compare & pull request"
3. Remplir le template de PR
4. Attendre la review

## 📝 Standards de code

### Style Python

Suivre [PEP 8](https://pep8.org/) :

```python
# ✅ Bon
def get_weather(city: str) -> str:
    """Récupère la météo pour une ville."""
    pass

# ❌ Mauvais
def getWeather(city):
    pass
```

### Documentation

Toutes les fonctions publiques doivent avoir un docstring :

```python
def my_function(param1: str, param2: int) -> bool:
    """
    Description courte.
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
    
    Returns:
        Description de ce qui est retourné
    
    Raises:
        ValueError: Quand lever cette exception
    """
    pass
```

### Imports

Organiser les imports dans cet ordre :

```python
# 1. Bibliothèque standard
import os
import sys

# 2. Bibliothèques tierces
from langchain_ollama import OllamaLLM
import requests

# 3. Imports locaux
from src.crewai_simulator import Agent
```

## 🎯 Priorités actuelles

Contributions particulièrement bienvenues :

- [ ] **Tests automatisés** : Ajouter des tests unitaires
- [ ] **Nouveaux agents** : Transport, hébergement, sécurité
- [ ] **Nouveaux outils** : Recherche web, traduction
- [ ] **Documentation** : Traductions (EN, ES)
- [ ] **Optimisation** : Améliorer les prompts
- [ ] **API REST** : Adapter api/main.py pour LangChain

## ❓ Questions ?

- Ouvrir une [Discussion](../../discussions)
- Rejoindre notre Discord (si applicable)
- Contacter les mainteneurs

## 🏆 Contributeurs

Un grand merci à tous les contributeurs !

<!-- Généré automatiquement par all-contributors -->

## 📜 Code de conduite

En participant à ce projet, vous acceptez de respecter notre [Code de Conduite](CODE_OF_CONDUCT.md).

Résumé :
- ✅ Être respectueux et inclusif
- ✅ Accepter les critiques constructives
- ✅ Se concentrer sur le bien du projet
- ❌ Harcèlement, insultes, discrimination

---

**Merci de contribuer ! 🎉**
