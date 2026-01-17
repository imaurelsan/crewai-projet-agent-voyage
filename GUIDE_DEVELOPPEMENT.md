# 📘 Guide de Développement - Pour Débutants

Ce guide vous explique **étape par étape** comment fonctionne le projet et comment le développer, même si vous débutez en programmation.

## 📚 Table des matières

1. [Prérequis et installation](#1-prérequis-et-installation)
2. [Concepts de base](#2-concepts-de-base)
3. [Architecture du projet](#3-architecture-du-projet)
4. [Créer votre premier agent](#4-créer-votre-premier-agent)
5. [Ajouter des outils à un agent](#5-ajouter-des-outils-à-un-agent)
6. [Créer un Crew complet](#6-créer-un-crew-complet)
7. [Personnaliser la configuration](#7-personnaliser-la-configuration)
8. [Déboguer votre code](#8-déboguer-votre-code)
9. [Aller plus loin](#9-aller-plus-loin)

---

## 1. Prérequis et installation

### 🔧 Ce dont vous avez besoin

1. **Python 3.13** - Le langage de programmation
2. **Ollama** - Le serveur qui fait tourner l'intelligence artificielle localement
3. **Un éditeur de code** - VS Code recommandé (gratuit)

### 📥 Installation pas à pas

#### Étape 1 : Installer Python 3.13

```powershell
# Télécharger depuis https://www.python.org/downloads/
# Cocher "Add Python to PATH" lors de l'installation
# Vérifier l'installation :
py -3.13 --version
# Devrait afficher : Python 3.13.x
```

#### Étape 2 : Installer Ollama

```powershell
# Télécharger depuis https://ollama.ai/download
# Installer le fichier téléchargé
# Vérifier l'installation :
ollama --version
# Devrait afficher : ollama version 0.x.x
```

#### Étape 3 : Télécharger le modèle IA

```powershell
# Télécharger le modèle Llama 3.2 (2GB)
ollama pull llama3.2:3b

# Vérifier qu'il est bien installé
ollama list
# Devrait afficher : llama3.2:3b
```

#### Étape 4 : Créer l'environnement virtuel

```powershell
# Se placer dans le dossier du projet
cd C:\chemin\vers\crewai-projet-agent-voyage

# Créer un environnement virtuel (venv)
py -3.13 -m venv venv

# Activer l'environnement
.\venv\Scripts\Activate.ps1

# Votre terminal devrait maintenant afficher (venv) au début
```

**💡 C'est quoi un environnement virtuel ?**
C'est comme une bulle isolée pour votre projet. Toutes les bibliothèques installées ici ne pollueront pas le reste de votre système.

#### Étape 5 : Installer les dépendances

```powershell
# Installer toutes les bibliothèques nécessaires
pip install -r requirements.txt

# Cela installe :
# - langchain : framework pour créer des agents
# - langchain-ollama : pour connecter Ollama
# - requests : pour faire des requêtes HTTP (météo)
# - python-dotenv : pour gérer les variables d'environnement
# - pyyaml : pour lire les fichiers de configuration
```

#### Étape 6 : Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

**💡 C'est quoi un fichier .env ?**
C'est un fichier qui contient des paramètres de configuration. Comme ça, on ne met pas les paramètres directement dans le code.

---

## 2. Concepts de base

### 🤖 Qu'est-ce qu'un Agent ?

Un **agent** est comme un employé virtuel spécialisé. Il a :
- **Un rôle** : par exemple "Expert en voyages"
- **Un objectif** : ce qu'il doit accomplir
- **Une histoire** (backstory) : son expérience
- **Des outils** (optionnel) : des fonctions qu'il peut utiliser

**Exemple concret :**
```python
agent_meteo = Agent(
    role="Spécialiste Météo",
    goal="Fournir des infos météo précises",
    backstory="Vous êtes un météorologue avec 10 ans d'expérience",
    tools=[get_weather]  # Il peut utiliser cet outil
)
```

### 📋 Qu'est-ce qu'une Task (tâche) ?

Une **task** est une mission donnée à un agent.

```python
tache_meteo = Task(
    description="Analyser la météo à Paris",
    expected_output="Un rapport météo détaillé",
    agent=agent_meteo  # Quel agent fait cette tâche
)
```

### 👥 Qu'est-ce qu'un Crew ?

Un **crew** est une équipe d'agents qui travaillent ensemble.

```python
crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[task1, task2, task3],
    process=Process.sequential  # Les tâches se font dans l'ordre
)
```

### 🔄 Processus séquentiel

Les tâches s'exécutent **dans l'ordre** :
```
Agent 1 → Agent 2 → Agent 3 → Résultat final
```

Chaque agent reçoit les résultats des agents précédents.

---

## 3. Architecture du projet

### 📂 Structure des dossiers

```
crewai-projet-agent-voyage/
│
├── config/                    # 📁 Configuration
│   ├── agents.yaml           # Définition des agents
│   └── tasks.yaml            # Définition des tâches
│
├── src/                       # 📁 Code source
│   ├── crewai_simulator.py   # Le "moteur" qui fait tourner les agents
│   └── crew_voyage.py        # Votre crew principal
│
├── agent_meteo.py            # Exemple d'agent simple
├── exemple_simple.py         # Exemple minimal
├── .env                       # Variables de configuration
└── requirements.txt           # Liste des bibliothèques
```

### 🎯 Fichiers importants

| Fichier | Rôle | Quand le modifier |
|---------|------|-------------------|
| `config/agents.yaml` | Définit les agents (rôle, objectif) | Pour changer la personnalité d'un agent |
| `config/tasks.yaml` | Définit les tâches | Pour changer ce que font les agents |
| `src/crew_voyage.py` | Crew principal | Pour ajouter/retirer des agents |
| `.env` | Configuration | Pour changer le modèle IA |

---

## 4. Créer votre premier agent

### Étape 1 : Agent simple (sans framework)

Créez un fichier `mon_premier_agent.py` :

```python
# 1. Importer les bibliothèques
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# 2. Charger les variables d'environnement
load_dotenv()

# 3. Créer le modèle IA
llm = OllamaLLM(
    model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.7  # Plus c'est élevé, plus c'est créatif
)

# 4. Créer le prompt (instructions pour l'IA)
prompt = ChatPromptTemplate.from_template("""
Tu es un guide touristique expert.
Recommande 3 activités à faire à {ville}.
Sois concis et enthousiaste.
""")

# 5. Créer la chaîne (prompt + IA)
chain = prompt | llm

# 6. Utiliser l'agent
if __name__ == "__main__":
    ville = input("Quelle ville voulez-vous visiter ? ")
    resultat = chain.invoke({"ville": ville})
    print("\n" + "="*50)
    print(resultat)
    print("="*50)
```

**Tester :**
```powershell
python mon_premier_agent.py
```

### Étape 2 : Comprendre le code

```python
# ChatPromptTemplate = Le "script" que va suivre l'IA
prompt = ChatPromptTemplate.from_template("...")

# | = Pipe, ça connecte le prompt à l'IA
chain = prompt | llm

# invoke = Lancer l'agent avec des paramètres
resultat = chain.invoke({"ville": "Paris"})
```

**💡 Astuce :** La `temperature` contrôle la créativité :
- `0.0` = Réponses identiques et prévisibles
- `1.0` = Réponses très créatives et variées

---

## 5. Ajouter des outils à un agent

### Qu'est-ce qu'un outil ?

Un **outil** est une fonction Python que l'agent peut appeler. Exemple : récupérer la météo, chercher sur Google, lire un fichier.

### Créer un outil simple

Créez `agent_avec_outil.py` :

```python
from langchain_core.tools import tool
from langchain_ollama import OllamaLLM
import requests

# 1. Créer l'outil avec le décorateur @tool
@tool
def get_weather(city: str) -> str:
    """Récupère la météo actuelle pour une ville"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            return f"""Météo à {city}:
🌡️ {current['temp_C']}°C
☁️ {current['weatherDesc'][0]['value']}
💧 Humidité: {current['humidity']}%"""
        else:
            return f"Météo non disponible pour {city}"
    except Exception as e:
        return f"Erreur: {str(e)}"

# 2. Utiliser l'outil
if __name__ == "__main__":
    city = input("Quelle ville ? ")
    
    # Appeler directement l'outil
    result = get_weather.invoke({"city": city})
    print(result)
```

**💡 Le décorateur `@tool` :**
- Transforme une fonction normale en "outil" pour les agents
- L'IA pourra décider quand utiliser cet outil
- Le docstring (""") est important : il explique à l'IA ce que fait l'outil

---

## 6. Créer un Crew complet

### Architecture CrewAI

Notre projet utilise des **décorateurs** pour organiser le code comme dans CrewAI :

```python
@CrewBase      # Marque la classe comme un Crew
class MonCrew():
    
    @agent     # Marque une méthode comme agent
    def mon_agent(self):
        return Agent(...)
    
    @task      # Marque une méthode comme tâche
    def ma_tache(self):
        return Task(...)
    
    @crew      # Marque une méthode comme crew
    def crew(self):
        return Crew(...)
```

### Créer un mini-crew

Créez `mini_crew.py` :

```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.crewai_simulator import Agent, Task, Crew, Process, CrewBase, agent, task, crew, LLM

@CrewBase
class MiniCrew():
    """Mon premier crew"""
    
    def __init__(self):
        self.llm = LLM(model="llama3.2:3b")
    
    @agent
    def guide(self) -> Agent:
        """Agent guide touristique"""
        return Agent(
            role="Guide Touristique",
            goal="Recommander les meilleures attractions",
            backstory="Vous êtes un guide avec 10 ans d'expérience",
            llm=self.llm
        )
    
    @agent
    def chef(self) -> Agent:
        """Agent expert culinaire"""
        return Agent(
            role="Chef Cuisinier",
            goal="Recommander les meilleurs restaurants",
            backstory="Vous êtes un chef étoilé qui connaît tous les restaurants",
            llm=self.llm
        )
    
    @task
    def attractions_task(self) -> Task:
        """Trouver les attractions"""
        return Task(
            description="Liste 3 attractions principales à {ville}",
            expected_output="Une liste de 3 attractions avec descriptions",
            agent=self.guide()
        )
    
    @task
    def restaurants_task(self) -> Task:
        """Trouver les restaurants"""
        return Task(
            description="Recommande 3 restaurants à {ville}",
            expected_output="Une liste de 3 restaurants avec spécialités",
            agent=self.chef()
        )
    
    @crew
    def crew(self) -> Crew:
        """Créer l'équipe"""
        return Crew(
            agents=[self.guide(), self.chef()],
            tasks=[self.attractions_task(), self.restaurants_task()],
            process=Process.sequential,
            verbose=True
        )

# Utilisation
if __name__ == "__main__":
    ville = input("Quelle ville ? ")
    
    mon_crew = MiniCrew()
    resultat = mon_crew.crew().kickoff(inputs={'ville': ville})
    
    print("\n" + "="*70)
    print("RÉSULTAT FINAL")
    print("="*70)
    print(resultat)
```

**Tester :**
```powershell
python mini_crew.py
```

---

## 7. Personnaliser la configuration

### Modifier les agents (agents.yaml)

Ouvrez `config/agents.yaml` :

```yaml
mon_agent:
  role: "Expert en Quelque Chose"
  goal: "Atteindre cet objectif"
  backstory: |
    Vous êtes un expert avec X années d'expérience.
    Vous êtes passionné par votre domaine.
```

**Conseils :**
- Le `role` doit être court et clair
- Le `goal` doit être spécifique
- Le `backstory` donne de la personnalité

### Modifier les tâches (tasks.yaml)

Ouvrez `config/tasks.yaml` :

```yaml
ma_tache:
  description: |
    Fais ceci et cela pour {variable}.
    Inclue:
    - Point 1
    - Point 2
  expected_output: |
    Un rapport détaillé avec ces sections:
    - Section 1
    - Section 2
```

**Conseils :**
- Utilisez `{variable}` pour les paramètres dynamiques
- Soyez précis sur ce que vous attendez
- Le `expected_output` guide l'IA sur le format

---

## 8. Déboguer votre code

### Erreurs courantes

#### Erreur 1 : "ModuleNotFoundError"

```python
ModuleNotFoundError: No module named 'langchain'
```

**Solution :**
```powershell
# Vérifier que le venv est activé (doit afficher (venv))
.\venv\Scripts\Activate.ps1

# Réinstaller les dépendances
pip install -r requirements.txt
```

#### Erreur 2 : "Ollama connection refused"

```python
requests.exceptions.ConnectionError: ... connection refused
```

**Solution :**
```powershell
# Vérifier qu'Ollama tourne
ollama list

# Si pas de réponse, relancer Ollama
# Sous Windows: chercher "Ollama" dans le menu démarrer
```

#### Erreur 3 : Réponse vide ou incohérente

**Causes possibles :**
- Le prompt n'est pas assez clair
- Le `backstory` ne correspond pas à la tâche
- La `temperature` est trop élevée

**Solution :**
```python
# Rendre le prompt plus précis
description = """
Analyse PRÉCISÉMENT la météo à {ville}.
Format attendu:
1. Température actuelle
2. Conditions (soleil, pluie, etc.)
3. Recommandation vestimentaire
"""

# Baisser la temperature
llm = OllamaLLM(model="llama3.2:3b", temperature=0.3)
```

### Mode debug

Ajoutez des prints pour voir ce qui se passe :

```python
print(f"🔍 Prompt envoyé: {prompt_text}")
print(f"🤖 Réponse IA: {result}")
```

---

## 9. Aller plus loin

### Idées de nouveaux agents

1. **Agent de Transport**
   - Trouve les meilleurs moyens de transport
   - Estime les temps de trajet
   - Compare les prix

2. **Agent d'Hébergement**
   - Recommande des hôtels/Airbnb
   - Compare les prix
   - Vérifie les avis

3. **Agent de Sécurité**
   - Informe sur les précautions à prendre
   - Zones à éviter
   - Vaccins nécessaires

### Ajouter un nouvel outil

Exemple : Recherche Google

```python
@tool
def search_google(query: str) -> str:
    """Recherche sur Google"""
    # Nécessite une clé API Google
    # Voir: https://developers.google.com/custom-search/
    pass
```

### Modifier le processus

Au lieu de `Process.sequential`, vous pourriez :
- Créer un processus parallèle (tous les agents en même temps)
- Créer un processus conditionnel (si X alors Y)

**Exemple conceptuel :**
```python
# Aujourd'hui: séquentiel
Agent1 → Agent2 → Agent3

# Parallèle (à implémenter)
Agent1 ↘
        → Agent3
Agent2 ↗

# Conditionnel (à implémenter)
Agent1 → Si budget > 1000€ → AgentLuxe
      → Sinon → AgentEconomique
```

### Exporter vers une API

Pour créer une API web, utilisez FastAPI :

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/planifier-voyage")
def planifier(destination: str):
    crew = TravelCrew()
    result = crew.crew().kickoff(inputs={'destination': destination})
    return {"plan": result}

# Lancer avec: uvicorn api.main:app --reload
```

---

## 📚 Ressources supplémentaires

### Documentation officielle

- [LangChain](https://python.langchain.com/docs/get_started/introduction)
- [Ollama](https://github.com/ollama/ollama)
- [CrewAI](https://docs.crewai.com/)

### Tutoriels recommandés

- [Python pour débutants](https://www.python.org/about/gettingstarted/)
- [YAML expliqué](https://yaml.org/spec/1.2/spec.html)
- [Comprendre les LLMs](https://en.wikipedia.org/wiki/Large_language_model)

### Communautés

- Discord LangChain
- Forum CrewAI
- Stack Overflow (tag: langchain)

---

## 🎓 Exercices pratiques

### Exercice 1 : Modifier un agent

**Objectif :** Changer la personnalité de l'agent météo

1. Ouvrir `config/agents.yaml`
2. Modifier le `backstory` de `weather_specialist`
3. Tester avec `python agent_meteo.py`

### Exercice 2 : Ajouter une tâche

**Objectif :** Créer une tâche "activités nocturnes"

1. Ouvrir `config/tasks.yaml`
2. Ajouter une nouvelle tâche :
```yaml
nightlife_task:
  description: "Recommande 3 activités nocturnes à {destination}"
  expected_output: "Liste de bars, clubs et spectacles"
```
3. Créer l'agent et la tâche dans `src/crew_voyage.py`

### Exercice 3 : Créer votre propre crew

**Objectif :** Crew pour planifier un anniversaire

Agents nécessaires :
- Agent Restaurant
- Agent Cadeaux
- Agent Animation
- Agent Coordinateur

---

## ❓ FAQ - Questions fréquentes

**Q: Pourquoi Python 3.13 spécifiquement ?**
R: Les versions plus récentes (3.14+) ne sont pas compatibles avec certaines bibliothèques. 3.13 est le sweet spot.

**Q: Ollama consomme-t-il beaucoup de ressources ?**
R: Avec llama3.2:3b, comptez environ 4GB de RAM. C'est raisonnable pour un PC moderne.

**Q: Peut-on utiliser ChatGPT au lieu d'Ollama ?**
R: Oui, mais il faut une clé API OpenAI (payant). Modifiez le `LLM()` en conséquence.

**Q: Les réponses sont lentes, c'est normal ?**
R: Oui, Ollama en local est plus lent que les API cloud. Soyez patient (5-30 secondes par réponse).

**Q: Comment contribuer au projet ?**
R: Fork sur GitHub, faites vos modifications, puis créez une Pull Request.

---

🎉 **Félicitations !** Vous savez maintenant créer des agents intelligents et des crews complets. Bonne exploration ! 🚀
