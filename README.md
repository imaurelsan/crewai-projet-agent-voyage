# 🌍 Projet CrewAI - Travel Planner Complet

## 📖 Tutoriel Complet - De Zéro à Héros

> **Guide complet pour débutants** : Ce README vous apprend à créer un système multi-agents de A à Z, avec explications détaillées de chaque concept.

Un système multi-agents de planification de voyage **professionnel** avec 8 outils spécialisés utilisant l'architecture CrewAI, LangChain et **Groq** (LLM ultra-rapide et 100% gratuit).

![Python Version](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Groq](https://img.shields.io/badge/LLM-Groq-purple)
![Tools](https://img.shields.io/badge/tools-8-orange)
![Agents](https://img.shields.io/badge/agents-6-brightgreen)

## 📋 Table des matières

### 🎓 Pour les débutants
- [📚 Qu'est-ce qu'on construit ?](#-quest-ce-quon-construit-)
- [🧠 Concepts clés à comprendre](#-concepts-clés-à-comprendre)
- [📖 Chronologie du projet](#-chronologie-du-projet-ce-qui-a-été-fait)
- [🛠️ Tutoriel complet - Mise en place](#️-tutoriel-complet---de-a-à-z)

### 🚀 Pour démarrer rapidement
- [⚡ Installation rapide](#-installation-rapide)
- [💻 Utilisation](#-utilisation)
- [🧪 Tests](#-tests)

### 📖 Documentation technique
- [🏗️ Architecture détaillée](#️-architecture-détaillée)
- [📁 Structure du projet](#-structure-du-projet)
- [🔧 Technologies utilisées](#-technologies-utilisées)
- [🆘 Résolution de problèmes](#-résolution-de-problèmes)

- [🆘 Résolution de problèmes](#-résolution-de-problèmes)

---

## 📚 Qu'est-ce qu'on construit ?

### 🎯 L'objectif final

Imaginez que vous voulez planifier un voyage à Paris pour 3 jours. Au lieu de chercher manuellement sur Google pendant des heures, vous avez une **équipe d'experts virtuels** qui travaillent pour vous :

1. 🔍 Un **chercheur** qui trouve les meilleures attractions
2. ☁️ Un **météorologue** qui vous dit quoi emporter
3. 🏨 Un **expert hôtelier** qui trouve les meilleurs hébergements
4. 🚆 Un **coordinateur transport** qui compare train/avion/bus
5. 🎭 Un **planificateur d'activités** qui crée votre itinéraire jour par jour
6. 🎯 Un **coordinateur** qui compile tout dans un guide PDF

**Résultat** : Un guide de voyage complet en 5 minutes au lieu de 3 heures de recherche !

### 💡 Ce que vous allez apprendre

En suivant ce README, vous comprendrez :

✅ **Les agents IA** : Comment créer des "assistants virtuels" spécialisés  
✅ **Les outils (tools)** : Comment donner des capacités aux agents  
✅ **LangChain** : Le framework pour orchestrer tout ça  
✅ **Groq** : Un LLM gratuit et ultra-rapide  
✅ **L'architecture multi-agents** : Comment faire travailler plusieurs IA ensemble  

---

## 🧠 Concepts clés à comprendre

### 1️⃣ Qu'est-ce qu'un Agent IA ?

**Simple :** Un agent est comme un **employé virtuel** avec :
- Un **rôle** (ex: "Expert en voyage")
- Un **objectif** (ex: "Trouver les meilleures attractions")
- Des **outils** (ex: Google, météo, etc.)
- Une **intelligence** (LLM = cerveau de l'agent)

**Exemple concret :**
```python
agent_meteo = Agent(
    role="Spécialiste Météo",                    # Son métier
    goal="Analyser la météo de la destination",   # Son objectif
    tools=[get_weather],                          # Ses outils
    llm=groq_llm                                  # Son cerveau (IA)
)
```

### 2️⃣ Qu'est-ce qu'un Outil (Tool) ?

**Simple :** Un outil est une **fonction Python** que l'agent peut utiliser.

**Exemple :** Au lieu que l'agent *invente* la météo, il utilise l'outil `get_weather()` qui appelle une vraie API météo.

```python
@tool
def get_weather(city: str) -> str:
    """Récupère la météo réelle d'une ville"""
    # Appelle l'API wttr.in
    return "Paris: 15°C, ensoleillé"
```

**Analogie :** C'est comme donner un **téléphone** à votre employé pour qu'il puisse appeler les experts.

### 3️⃣ Qu'est-ce qu'un LLM (Large Language Model) ?

**Simple :** C'est le **cerveau** de vos agents. 

- **Avant :** ChatGPT, GPT-4 (payants)
- **Maintenant :** Groq avec Llama 3.3 (gratuit et rapide !)

**Ce qu'il fait :** Comprend les instructions, raisonne, décide quand utiliser les outils.

### 4️⃣ Qu'est-ce que LangChain ?

**Simple :** Un framework Python qui simplifie la création d'agents IA.

**Sans LangChain :** Vous devez coder toute la logique à la main  
**Avec LangChain :** Vous utilisez des blocs pré-construits (comme des LEGO)

### 5️⃣ Qu'est-ce que CrewAI ?

**Simple :** Une architecture qui permet à **plusieurs agents de travailler ensemble** (comme une équipe).

**Notre projet :** On a créé un **simulateur CrewAI** compatible avec Python 3.13 (car le vrai CrewAI n'est pas encore compatible).

---

## 📖 Chronologie du projet (Ce qui a été fait)

### 📅 Phase 1 : Fondations (Semaine 1)

#### ✅ Étape 1 : Setup initial
- ✅ Installation Python 3.13
- ✅ Création environnement virtuel
- ✅ Installation des dépendances de base (LangChain, etc.)

#### ✅ Étape 2 : Choix du LLM
**Problème :** Quel "cerveau" utiliser pour nos agents ?

**Options considérées :**
- ❌ OpenAI GPT-4 → Payant (20$/mois)
- ❌ Ollama local → Trop lent (30+ min par tâche)
- ✅ **Groq** → **Gratuit + Ultra-rapide** ⚡

**Décision :** Migration vers Groq (10x plus rapide qu'Ollama)

#### ✅ Étape 3 : Simulateur CrewAI
**Problème :** CrewAI officiel incompatible avec Python 3.13

**Solution :** Création de `src/crewai_simulator.py`
- Simule les décorateurs `@agent`, `@task`, `@crew`
- Compatible Python 3.13
- Même syntaxe que le vrai CrewAI

---

### 📅 Phase 2 : Création des Outils (Semaine 2)

**Objectif :** Donner des capacités concrètes aux agents

#### 🛠️ Les 8 outils créés

| # | Outil | Fonction | API/Source | Fichier |
|---|-------|----------|-----------|---------|
| 1 | `get_weather` | Météo temps réel | wttr.in | `src/tools/travel_tools.py` |
| 2 | `search_web` | Recherche basique | DuckDuckGo | `src/tools/travel_tools.py` |
| 3 | `search_web_serpapi` | Recherche Google | SerpAPI | `src/tools/travel_tools.py` |
| 4 | `search_hotels` | Hôtels par budget | IA simulation | `src/tools/travel_tools.py` |
| 5 | `search_transport` | Train/avion/bus | IA simulation | `src/tools/travel_tools.py` |
| 6 | `search_activities` | Activités touristiques | Base connaissances | `src/tools/travel_tools.py` |
| 7 | `search_restaurants` | Restaurants filtres | Base connaissances | `src/tools/travel_tools.py` |
| 8 | `plan_itinerary` | Itinéraire jour/jour | Algorithme IA | `src/tools/travel_tools.py` |

**Fichiers créés :**
- ✅ `src/tools/travel_tools.py` (450 lignes avec commentaires)
- ✅ `src/tools/__init__.py` (exports)
- ✅ `test_outils.py` (menu interactif pour tester chaque outil)

**Pourquoi ces outils ?**

Chaque outil répond à un besoin précis du voyage :
- Météo → Savoir quoi emporter
- Hôtels → Où dormir selon budget
- Transport → Comment s'y rendre
- Activités → Quoi faire
- Restaurants → Où manger
- Itinéraire → Organiser les journées

---

### 📅 Phase 3 : Création des Agents (Semaine 3)

**Objectif :** Créer 6 agents spécialisés qui utilisent les outils

#### 🤖 Les 6 agents créés

| Agent | Rôle | Outils utilisés | Fichier |
|-------|------|----------------|---------|
| **Chercheur** | Recherche destinations | `search_web` | `src/crew_voyage_complet.py` |
| **Météorologue** | Analyse météo | `get_weather` | `src/crew_voyage_complet.py` |
| **Expert Hôtels** | Recommandations hébergement | `search_hotels` | `src/crew_voyage_complet.py` |
| **Coordinateur Transport** | Options transport | `search_transport` | `src/crew_voyage_complet.py` |
| **Planificateur** | Activités + restaurants | `search_activities`, `search_restaurants`, `plan_itinerary` | `src/crew_voyage_complet.py` |
| **Coordinateur** | Synthèse finale | Aucun (compilation) | `src/crew_voyage_complet.py` |

**Architecture du crew :**
```
1. Chercheur → 2. Météo → 3. Hôtels → 4. Transport → 5. Activités → 6. Synthèse
                                                                           ↓
                                                                  guide_voyage_complet.md
```

**Workflow séquentiel :**
Chaque agent attend que le précédent termine avant de commencer (processus séquentiel).

---

### 📅 Phase 4 : Migration Groq (30 janvier 2026)

**Problème identifié :** Ollama trop lent (30+ minutes pour un guide de voyage)

**Solution :** Migration complète vers Groq

#### Modifications effectuées (8 fichiers)

1. ✅ `requirements.txt` : `langchain-ollama` → `langchain-groq`
2. ✅ `src/config.py` : Variables `OLLAMA_*` → `GROQ_*`
3. ✅ `src/crewai_simulator.py` : `OllamaLLM` → `ChatGroq`
4. ✅ `src/agents/travel_agents.py` : Configuration Groq
5. ✅ `.env.example` : Template avec Groq
6. ✅ `exemple_simple.py` : Migration Groq
7. ✅ `multi_agents.py` : Migration Groq
8. ✅ `agent_meteo.py` : Migration Groq

#### Nouveaux fichiers créés

9. ✅ `GROQ_SETUP.md` : Guide obtention clé gratuite
10. ✅ `test_groq_config.py` : Test automatique configuration
11. ✅ `MIGRATION_SUMMARY.md` : Résumé technique migration

#### Résultats

- ⚡ **Vitesse** : 5 minutes au lieu de 30+ minutes
- 💰 **Coût** : 100% gratuit (quota généreux)
- 🎯 **Qualité** : Modèle 70B au lieu de 3B
- 💻 **Ressources** : 0% CPU/RAM (cloud)

---

### 📅 État actuel du projet

✅ **Fonctionnel à 100%**
- 6 agents opérationnels
- 8 outils testés
- Groq configuré et testé
- Documentation complète

🎯 **Prêt à l'emploi**
- Exécution : `python src/crew_voyage_complet.py`
- Génère un guide de voyage complet
- Export automatique en Markdown

---

## 🛠️ Tutoriel complet - De A à Z

### 🎓 Comprendre avant de commencer

**Ce qu'on va faire :**
1. Installer les outils nécessaires
2. Configurer Groq (cerveau gratuit de nos agents)
3. Tester les outils un par un
4. Lancer le crew complet
5. Obtenir un guide de voyage professionnel

**Temps estimé :** 30 minutes

---

### Étape 1 : Prérequis système

**Ce dont vous avez besoin :**

| Logiciel | Version | Pourquoi | Téléchargement |
|----------|---------|----------|----------------|
| **Python** | 3.13 | Langage du projet | [python.org](https://www.python.org/downloads/) |
| **PowerShell** | 5.1+ | Terminal Windows | Pré-installé Windows |
| **Compte Groq** | Gratuit | Cerveau des agents | [console.groq.com](https://console.groq.com) |

**Vérifier Python :**
```powershell
python --version
# Doit afficher: Python 3.13.x
```

Si Python n'est pas installé → [Guide installation Python](https://www.python.org/downloads/)

---

### Étape 2 : Récupérer le projet

**Option A : Cloner depuis GitHub (si disponible)**
```powershell
git clone <URL_DU_REPO>
cd crewai-projet-agent-voyage
```

**Option B : Télécharger directement**
1. Téléchargez le ZIP du projet
2. Extrayez dans `C:\Users\VotreNom\Desktop\crewai-projet-agent-voyage`
3. Ouvrez PowerShell dans ce dossier

**Vérifier :**
```powershell
dir
# Vous devez voir: src/, requirements.txt, README.md, etc.
```

---

### Étape 3 : Environnement virtuel Python

**Pourquoi ?** Pour isoler les dépendances du projet (bonnes pratiques).

**Création :**
```powershell
# Créer l'environnement virtuel
py -3.13 -m venv venv

# Activer l'environnement (IMPORTANT : à faire à chaque session)
.\venv\Scripts\Activate.ps1

# Votre terminal doit afficher (venv) au début de la ligne
```

**Problème courant :**
```
Execution Policy Error...
```

**Solution :**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Puis réessayez l'activation
```

---

### Étape 4 : Installer les dépendances

**Qu'est-ce qu'on installe ?**

| Package | Rôle | Taille |
|---------|------|--------|
| `langchain` | Framework agents IA | ~50MB |
| `langchain-groq` | Interface Groq | ~5MB |
| `requests` | Appels API (météo, web) | ~2MB |
| `python-dotenv` | Gestion variables env | ~1MB |
| Autres | Support (YAML, numpy, etc.) | ~100MB |

**Installation :**
```powershell
# (venv) doit être actif !
pip install -r requirements.txt

# Durée : 2-3 minutes
# Doit afficher: Successfully installed...
```

**Vérifier :**
```powershell
pip list | Select-String "groq"
# Doit afficher: langchain-groq
```

---

### Étape 5 : Configurer Groq (LE CERVEAU)

**C'est quoi Groq ?**
- LLM ultra-rapide (comme ChatGPT mais gratuit)
- Hébergé dans le cloud (pas d'installation)
- Quota gratuit généreux (30 req/min)

#### 5.1 Obtenir votre clé API gratuite

**Étapes détaillées :**

1. **Aller sur [console.groq.com](https://console.groq.com)**
   
2. **S'inscrire** (choix multiples):
   - Avec Google → Cliquez "Continue with Google"
   - Avec GitHub → Cliquez "Continue with GitHub"  
   - Avec email → Entrez email + mot de passe

3. **Créer une clé API :**
   - Dans le menu gauche → Cliquez "**API Keys**"
   - Cliquez le bouton "**Create API Key**"
   - Donnez un nom (ex: "Travel Agent Project")
   - Cliquez "**Submit**"

4. **COPIER LA CLÉ** (IMPORTANT):
   - La clé commence par `gsk_...`
   - **Copiez-la IMMÉDIATEMENT** (elle ne sera plus visible après)
   - Exemple: `gsk_NYuYTQVsR5RbF29cAKX9WGdyb3FY...`

#### 5.2 Configurer le fichier .env

**Le fichier .env contient vos secrets (clés API)**

```powershell
# Copier le template
copy .env.example .env

# Ouvrir le fichier avec un éditeur
notepad .env
```

**Modifier le fichier .env :**
```env
# Remplacez cette ligne:
GROQ_API_KEY=votre_clé_groq_ici

# Par votre vraie clé:
GROQ_API_KEY=gsk_NYuYTQVsR5RbF29cAKX9WGdyb3FY...

# Modèle à utiliser (ne changez pas):
GROQ_MODEL=llama-3.3-70b-versatile

# Provider (ne changez pas):
LLM_PROVIDER=groq
```

**Sauvegarder** et fermer Notepad.

#### 5.3 Tester la configuration

```powershell
python test_groq_config.py
```

**Résultat attendu :**
```
✅ Fichier .env trouvé
✅ GROQ_API_KEY trouvée
✅ langchain-groq installé
✅ ChatGroq initialisé
✅ Réponse reçue: Bonjour !

✅ TOUS LES TESTS SONT RÉUSSIS! 🎉
```

**Si erreur :**
- ❌ "GROQ_API_KEY non définie" → Vérifiez le fichier .env
- ❌ "Invalid API Key" → Clé incorrecte, recréez-en une
- ❌ "No module named groq" → `pip install langchain-groq`

---

### Étape 6 : Comprendre la structure du projet

**Fichiers importants :**

```
crewai-projet-agent-voyage/
│
├── src/                              # Code source principal
│   ├── tools/                        
│   │   ├── travel_tools.py          # ⭐ LES 8 OUTILS
│   │   └── __init__.py
│   │
│   ├── agents/
│   │   └── travel_agents.py         # Configuration agents
│   │
│   ├── crewai_simulator.py          # Simulateur CrewAI
│   └── crew_voyage_complet.py       # ⭐ LE CREW COMPLET (6 agents)
│
├── test_outils.py                   # 🧪 Tester les outils
├── test_groq_config.py              # 🧪 Tester Groq
├── exemple_simple.py                # 🎓 Exemple 1 agent
├── multi_agents.py                  # 🎓 Exemple 4 agents
│
├── .env                             # ⚙️ VOS CLÉS API (SECRET)
├── requirements.txt                 # 📦 Dépendances
└── README.md                        # 📖 Ce fichier
```

**Hiérarchie logique :**
1. **Outils** (`travel_tools.py`) → Capacités de base
2. **Agents** (`travel_agents.py`) → Utilisent les outils
3. **Crew** (`crew_voyage_complet.py`) → Orchestre les agents
4. **Simulateur** (`crewai_simulator.py`) → Fait tout fonctionner

---

### Étape 7 : Premiers tests

#### 7.1 Tester un outil individuel

**Menu interactif pour tester chaque outil :**

```powershell
python test_outils.py
```

**Ce que vous verrez :**
```
🧪 MENU DE TEST DES OUTILS
1. 🌤️  Météo
2. 🔍 Recherche Web
3. 🏨 Hôtels
...
Votre choix (0-8):
```

**Essayez :**
- Tapez `1` → Test météo (appelle API wttr.in)
- Tapez `8` → Teste TOUS les outils

**Ce que ça teste :**
- ✅ Les outils fonctionnent
- ✅ Les APIs répondent
- ✅ Le format de sortie est correct

#### 7.2 Tester un agent simple

**Exemple avec 1 seul agent :**

```powershell
python exemple_simple.py
```

**Ce qui se passe :**
1. L'agent se présente
2. Vous posez une question voyage
3. L'agent répond (utilise Groq)

**Exemple d'interaction :**
```
Posez votre question: Que faire à Paris en 2 jours ?

🤖 Expert répond:
Jour 1:
- Matin: Tour Eiffel
- Après-midi: Musée du Louvre
...
```

#### 7.3 Tester plusieurs agents

**Exemple avec 4 agents qui collaborent :**

```powershell
python multi_agents.py
```

**Ce qui se passe :**
1. Agent Destinations → Liste 3 attractions
2. Agent Météo → Analyse météo
3. Agent Budget → Estime les coûts
4. Agent Synthèse → Compile tout

**Durée :** ~2 minutes (avec Groq)

---

### Étape 8 : Lancer le CREW COMPLET ⭐

**C'est le cœur du projet : 6 agents + 8 outils**

```powershell
python src/crew_voyage_complet.py
```

**Ce qui va se passer :**

```
======================================================================
🌍 CREW DE VOYAGE COMPLET
======================================================================

📝 Informations nécessaires:

Destination (ex: Paris, Tokyo): Paris
Ville de départ (ex: Bruxelles): Lyon  
Durée du séjour en jours (ex: 3): 3
Budget (économique/moyen/luxe): moyen

🚀 Lancement du crew...

======================================================================
📌 TÂCHE 1/6: Chercheur de Destination
======================================================================
🤖 Chercheur travaille...
✅ Résultat: [Recherche des top attractions...]

======================================================================
📌 TÂCHE 2/6: Spécialiste Météo
======================================================================
🤖 Météorologue travaille...
✅ Résultat: [Analyse météo...]

... (continue avec les 6 agents)

✅ Guide de voyage sauvegardé: guide_voyage_complet.md
```

**Durée totale :** ~5 minutes (avec Groq)

**Résultat :** Un fichier `guide_voyage_complet.md` contenant:
- Top attractions
- Météo et recommandations
- Hôtels par budget
- Options transport
- Activités jour par jour
- Restaurants recommandés
- Itinéraire complet

---

### Étape 9 : Comprendre le résultat

**Ouvrez le fichier généré :**

```powershell
notepad guide_voyage_complet.md
```

**Structure du guide :**

```markdown
# Guide de Voyage - Paris (3 jours)

## 🔍 Recherche Destination
- Top 5 attractions incontournables
- Conseils pratiques
- Quartiers recommandés

## ☁️ Analyse Météo
- Températures prévues
- Vêtements à emporter
- Meilleures heures pour sortir

## 🏨 Hébergements Recommandés
- Budget moyen: Hôtel X (80€/nuit)
- Quartier: Marais
- Avantages: ...

## 🚆 Options de Transport
- Lyon → Paris
- TGV: 2h, 80€
- Avion: 1h, 150€
- Recommandation: TGV

## 🎭 Itinéraire Jour par Jour

### Jour 1
- Matin: Tour Eiffel
- Déjeuner: Restaurant Y
- Après-midi: Louvre
- Dîner: Restaurant Z

...
```

**Ce guide est prêt à imprimer ou partager !**

---

## ⚡ Installation rapide

Pour les développeurs expérimentés qui veulent aller vite:

```powershell
# Setup complet en 5 commandes
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Éditez .env avec votre GROQ_API_KEY
python test_groq_config.py
python src/crew_voyage_complet.py
```

---

## 💻 Utilisation

### Tests disponibles

```bash
# Test configuration Groq
python test_groq_config.py

# Test outils individuels (menu interactif)
python test_outils.py

# Exemple 1 agent simple
python exemple_simple.py

# Exemple 4 agents collaboratifs
python multi_agents.py

# CREW COMPLET - 6 agents + 8 outils
python src/crew_voyage_complet.py
```

### Personnaliser un voyage

Éditez les inputs dans `src/crew_voyage_complet.py`:

```python
inputs = {
    "destination": "Tokyo",      # Changez ici
    "origin": "Paris",           # Changez ici
    "duration": "5",             # Changez ici
    "budget": "luxe"             # économique/moyen/luxe
}
```

---

## 🧪 Tests

### Test 1 : Météo (30 secondes)

```powershell
python test_outils.py
# Choisir option 1
```

Teste : API wttr.in, format JSON, parsing

### Test 2 : Configuration Groq (10 secondes)

```powershell
python test_groq_config.py
```

Teste : Clé API, connexion, modèle

### Test 3 : Agent simple (1 minute)

```powershell
python exemple_simple.py
```

Teste : LLM Groq, prompts, réponses

### Test 4 : Crew complet (5 minutes)

```powershell
python src/crew_voyage_complet.py
```

Teste : 6 agents, 8 outils, workflow complet

---

## 🏗️ Architecture détaillée

### Vue d'ensemble du système

```
┌─────────────────────────────────────────────────────────────────┐
│                    UTILISATEUR                                   │
│              (pose une question voyage)                          │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              CREW DE VOYAGE COMPLET                              │
│              (src/crew_voyage_complet.py)                        │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Agent 1   │→│   Agent 2   │→│   Agent 3   │→ ...          │
│  │  Chercheur  │  │   Météo     │  │   Hôtels    │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                      │
│         ▼                ▼                ▼                      │
│  ┌─────────────────────────────────────────────────┐            │
│  │              BIBLIOTHÈQUE D'OUTILS                │            │
│  │          (src/tools/travel_tools.py)             │            │
│  ├─────────────────────────────────────────────────┤            │
│  │  get_weather  │  search_hotels  │  plan_itinerary│            │
│  │  search_web   │  search_transport│  etc...       │            │
│  └────┬────────┬────────┬──────────┬───────────────┘            │
│       │        │        │          │                             │
└───────┼────────┼────────┼──────────┼─────────────────────────────┘
        │        │        │          │
        ▼        ▼        ▼          ▼
   ┌────────┐┌─────────┐┌───────┐┌──────────┐
   │ wttr.in││DuckDuckGo││Groq   ││SerpAPI   │
   │  API   ││  (gratuit)││ LLM   ││(optionnel)│
   └────────┘└─────────┘└───────┘└──────────┘
        │        │        │          │
        └────────┴────────┴──────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │  GUIDE DE VOYAGE     │
          │  (Markdown)          │
          └──────────────────────┘
```

### Flux de données détaillé

**Étape 1 : Initialisation**
```python
# 1. Utilisateur lance le crew
python src/crew_voyage_complet.py

# 2. Le système charge:
- Configuration Groq (.env)
- Les 8 outils (travel_tools.py)
- Les 6 agents (crew_voyage_complet.py)
- Le simulateur CrewAI (crewai_simulator.py)
```

**Étape 2 : Collecte des inputs**
```python
inputs = {
    "destination": "Paris",
    "origin": "Bruxelles",
    "duration": "3",
    "budget": "moyen"
}
```

**Étape 3 : Exécution séquentielle**

| Ordre | Agent | Outil(s) utilisé(s) | Temps | Output |
|-------|-------|---------------------|-------|---------|
| 1 | Chercheur | `search_web` | ~30s | Top 5 attractions |
| 2 | Météorologue | `get_weather` | ~20s | Temp, conditions |
| 3 | Expert Hôtels | `search_hotels` | ~25s | Liste hôtels |
| 4 | Coordinateur Transport | `search_transport` | ~30s | Options voyage |
| 5 | Planificateur | `search_activities`<br>`search_restaurants`<br>`plan_itinerary` | ~90s | Itinéraire complet |
| 6 | Coordinateur | - | ~20s | Guide final |

**Total : ~5 minutes avec Groq** (vs 30+ min avec Ollama)

**Étape 4 : Génération du résultat**
```python
# Le coordinateur final compile tout et génère:
guide_voyage_complet.md
```

### Architecture des Outils

**Pattern utilisé : Decorator Pattern**

```python
from langchain_core.tools import tool

@tool
def nom_de_loutil(param1: str, param2: str = "default") -> str:
    """
    Description claire de ce que fait l'outil.
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
        
    Returns:
        Description du retour
    """
    # 1. Validation des inputs
    if not param1:
        return "Erreur: param1 requis"
    
    # 2. Logique métier
    result = faire_quelque_chose(param1, param2)
    
    # 3. Formattage du résultat
    return f"Résultat formatté: {result}"
```

**Exemple concret - get_weather:**

```python
@tool
def get_weather(city: str) -> str:
    """Récupère la météo actuelle d'une ville."""
    
    try:
        # 1. Appel API wttr.in
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=15)
        data = response.json()
        
        # 2. Extraction des données
        temp = data['current_condition'][0]['temp_C']
        conditions = data['current_condition'][0]['weatherDesc'][0]['value']
        
        # 3. Format lisible
        return f"{city}: {temp}°C, {conditions}"
        
    except Exception as e:
        return f"Erreur météo: {str(e)}"
```

### Architecture du Simulateur CrewAI

**Pourquoi un simulateur ?**
- ❌ CrewAI officiel incompatible Python 3.13
- ✅ Notre simulateur : même syntaxe, compatible 3.13

**Composants principaux:**

```python
# src/crewai_simulator.py

class Agent:
    """Simule un agent CrewAI"""
    def __init__(self, role, goal, backstory, tools, llm):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools  # Liste d'outils
        self.llm = llm      # Groq LLM

class Task:
    """Simule une tâche CrewAI"""
    def __init__(self, description, expected_output, agent, context):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.context = context  # Résultats des tâches précédentes

class Crew:
    """Orchestre les agents et tâches"""
    def __init__(self, agents, tasks, process):
        self.agents = agents
        self.tasks = tasks
        self.process = process  # "sequential"
        
    def kickoff(self, inputs):
        """Lance l'exécution séquentielle"""
        results = []
        context = ""
        
        for task in self.tasks:
            # 1. Construire le prompt
            prompt = self._build_prompt(task, context, inputs)
            
            # 2. Exécuter avec Groq
            if task.agent.tools:
                # Agent a des outils → peut les utiliser
                result = self._execute_with_tools(prompt, task.agent)
            else:
                # Agent sans outils → juste raisonne
                result = task.agent.llm.invoke(prompt)
            
            # 3. Sauvegarder le contexte
            context += f"\n{result}"
            results.append(result)
        
        return context
```

### Provider LLM : Groq

**Configuration actuelle:**

```python
# src/config.py
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
LLM_PROVIDER = "groq"

# Initialisation dans chaque agent
from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0.7  # Créativité modérée
)
```

**Modèles disponibles:**

| Modèle | Paramètres | Vitesse | Usage recommandé |
|--------|-----------|---------|------------------|
| `llama-3.3-70b-versatile` | 70B | Rapide | **Actuel** - Meilleur équilibre |
| `llama-3.1-8b-instant` | 8B | Ultra-rapide | Prototypage |
| `mixtral-8x7b-32768` | 56B | Rapide | Longs contextes |
| `gemma2-9b-it` | 9B | Très rapide | Usage général |

**Performances Groq:**
- ⚡ Tokens/seconde : ~500-1000 (vs ~20-50 Ollama)
- ⏱️ Latence : ~200ms (vs ~5-10s Ollama)
- 💰 Quota gratuit : 30 req/min, 14400 req/jour

---

## 📁 Structure du projet

### Organisation complète

```
crewai-projet-agent-voyage/
│
├── 📁 config/                      # Configuration YAML
│   ├── agents.yaml                # Définition des agents (rôles, objectifs)
│   └── tasks.yaml                 # Définition des tâches
│
├── 📁 src/                         # Code source principal
│   ├── crewai_simulator.py        # 🎭 Simulateur CrewAI (Agent, Task, Crew)
│   ├── config.py                  # ⚙️ Configuration (Groq, API keys)
│   │
│   ├── 📁 agents/
│   │   ├── __init__.py
│   │   └── travel_agents.py       # 🤖 5 agents de base
│   │
│   ├── 📁 tasks/
│   │   ├── __init__.py
│   │   └── travel_tasks.py        # 📝 Définition des tâches
│   │
│   ├── 📁 tools/                   # ⭐ BIBLIOTHÈQUE D'OUTILS
│   │   ├── __init__.py            # Exports
│   │   └── travel_tools.py        # 🛠️ 8 outils professionnels
│   │
│   ├── crew_voyage.py             # 🚀 Crew basique (5 agents)
│   ├── crew_voyage_complet.py     # 🚀 Crew complet (6 agents + 8 outils)
│   └── main.py                    # 🎯 Point d'entrée API
│
├── 📁 api/
│   ├── __init__.py
│   └── main.py                    # 🌐 API FastAPI (future)
│
├── 🧪 Tests & Exemples
│   ├── test_groq_config.py        # ✅ Test configuration Groq
│   ├── test_outils.py             # ✅ Test menu interactif outils
│   ├── test_meteo_interactif.py   # ✅ Test agent météo
│   ├── test_outils_rapide.py      # ✅ Test rapide
│   ├── exemple_simple.py          # 🎓 1 agent simple
│   ├── multi_agents.py            # 🎓 4 agents collaboratifs
│   └── agent_meteo.py             # 🎓 Agent météo standalone
│
├── 📄 Configuration
│   ├── .env                       # 🔐 Clés API (SECRET - pas sur GitHub)
│   ├── .env.example               # 📋 Template .env
│   ├── requirements.txt           # 📦 Dépendances Python
│   └── .gitignore                 # 🚫 Fichiers à ignorer
│
├── 📚 Documentation
│   ├── README.md                  # 📖 Ce fichier (guide complet)
│   ├── GUIDE_DEVELOPPEMENT.md     # 📘 Guide débutants
│   ├── GROQ_SETUP.md              # ⚡ Setup Groq
│   ├── MIGRATION_SUMMARY.md       # 📊 Résumé migration Ollama→Groq
│   ├── QUICKSTART.md              # 🚀 Démarrage rapide
│   ├── CONTRIBUTING.md            # 🤝 Guide contribution
│   ├── GITHUB_GUIDE.md            # 🐙 Guide GitHub
│   └── SERPAPI_GUIDE.md           # 🔍 Setup SerpAPI
│
├── 📄 Résultats générés
│   ├── voyage_plan.md             # Exemple sortie crew basique
│   └── guide_voyage_complet.md    # Exemple sortie crew complet
│
└── 📜 Métadonnées
    ├── LICENSE                    # MIT License
    └── PROJET_INFO.md             # Infos projet
```

### Fichiers clés expliqués

| Fichier | Rôle | Importance |
|---------|------|-----------|
| `src/tools/travel_tools.py` | ⭐⭐⭐ | Les 8 outils que les agents utilisent |
| `src/crew_voyage_complet.py` | ⭐⭐⭐ | Crew principal avec 6 agents |
| `src/crewai_simulator.py` | ⭐⭐⭐ | Cœur de l'architecture CrewAI |
| `src/config.py` | ⭐⭐ | Configuration Groq et variables |
| `.env` | ⭐⭐⭐ | VOS clés API (à ne JAMAIS partager) |
| `test_outils.py` | ⭐⭐ | Tester chaque outil individuellement |
| `requirements.txt` | ⭐⭐ | Toutes les dépendances Python |

### Taille du projet

```
Lignes de code (approximatif):
- src/tools/travel_tools.py:     ~450 lignes
- src/crew_voyage_complet.py:    ~350 lignes
- src/crewai_simulator.py:       ~250 lignes
- Tests et exemples:             ~500 lignes
- Documentation:                 ~2000 lignes

Total: ~3500 lignes de code et documentation
```

---

## 🔧 Technologies utilisées

### Stack complet

#### 🐍 Langage & Environnement

| Technologie | Version | Rôle |
|-------------|---------|------|
| **Python** | 3.13 | Langage principal |
| **venv** | natif | Environnement virtuel |
| **PowerShell** | 5.1+ | Terminal Windows |

#### 🤖 IA & LLM

| Technologie | Version | Rôle | Coût |
|-------------|---------|------|------|
| **Groq** | API Cloud | LLM ultra-rapide | **Gratuit** |
| **LangChain** | 1.2.4 | Framework agents IA | Gratuit |
| **langchain-groq** | 0.1.0+ | Connecteur Groq | Gratuit |
| **langchain-core** | 1.2.4 | Tools, prompts | Gratuit |

#### 🌐 APIs & Services

| Service | Fonction | Limite gratuite | Payant ? |
|---------|----------|-----------------|----------|
| **wttr.in** | Météo mondiale | Illimité | Non |
| **DuckDuckGo** | Recherche web | Illimité | Non |
| **SerpAPI** | Google search | 100/mois | Optionnel |
| **Groq** | LLM | 30 req/min | Non |

#### 📦 Bibliothèques Python

| Package | Version | Usage |
|---------|---------|-------|
| `requests` | 2.32.5 | Appels API HTTP |
| `python-dotenv` | 1.0.0+ | Variables d'environnement |
| `pyyaml` | 6.0.3 | Config YAML |
| `pydantic` | 2.6.0+ | Validation données |
| `numpy` | 2.4.1 | Calculs (optionnel) |

### Dépendances complètes

```txt
# requirements.txt
langchain==1.2.4              # Framework agents
langchain-groq>=0.1.0         # Interface Groq
langchain-community==0.0.38   # Outils communauté
langchain-core>=1.2.0         # Core LangChain
python-dotenv>=1.0.0          # .env
requests>=2.32.0              # HTTP
pyyaml>=6.0.0                 # YAML
pydantic>=2.6.0               # Validation
numpy==2.4.1                  # Calculs
```

### Pourquoi ces choix technologiques?

#### ✅ Pourquoi Groq (au lieu d'Ollama ou OpenAI) ?

| Critère | Groq | Ollama | OpenAI |
|---------|------|--------|--------|
| **Vitesse** | ⚡⚡⚡⚡⚡ (500-1000 tok/s) | ⚡⚡ (20-50 tok/s) | ⚡⚡⚡⚡ (100-200 tok/s) |
| **Coût** | **Gratuit** | **Gratuit** | Payant (20$/mois) |
| **Installation** | Aucune (cloud) | 2GB téléchargement | Aucune (cloud) |
| **Ressources PC** | 0% CPU/RAM | 50-100% CPU/RAM | 0% CPU/RAM |
| **Modèle** | Llama 3.3 70B | Llama 3.2 3B | GPT-4 Turbo |
| **Quota** | 30 req/min | Illimité | 3 req/min (gratuit) |

**Décision:** Groq = Meilleur compromis vitesse/gratuité

#### ✅ Pourquoi LangChain?

**Alternatives considérées:**
- ❌ Coder tout à la main → Trop complexe
- ❌ LlamaIndex → Axé recherche documentaire
- ✅ **LangChain** → Framework complet pour agents

**Avantages:**
- Abstraction des LLMs (facile de changer Groq → OpenAI)
- Tools (@tool decorator)
- Gestion du contexte automatique
- Documentation riche

#### ✅ Pourquoi Python 3.13?

- Version la plus récente (janvier 2026)
- Performances améliorées (~25% plus rapide)
- async/await natif amélioré
- Typage fort (type hints)

---

## 💻 Utilisation

### Exemple 1 : Crew complet avec outils (6 agents) ⭐ RECOMMANDÉ

```powershell
python src/crew_voyage_complet.py
```

**Entrée :**
```
Quelle destination voulez-vous explorer? Paris
D'où partez-vous? Bruxelles
Combien de jours voulez-vous rester? 5
Quel est votre budget? (économique/moyen/luxe) moyen
```

**Sortie :**
- Guide de voyage complet avec météo
- Recommandations d'hôtels par budget
- Options de transport (train, avion, bus)
- Activités touristiques personnalisées
- Restaurants avec filtres
- Itinéraire jour par jour
- Fichier généré : `guide_voyage_complet.md`

### Exemple 2 : Tester les outils individuellement 🧪

```powershell
python test_outils.py
```

**Menu interactif pour tester :**
- 🌤️ Météo d'une ville
- 🔍 Recherche web
- 🏨 Recherche d'hôtels
- 🚆 Options de transport
- 🎭 Activités touristiques
- 🍽️ Recherche de restaurants
- 📅 Planification d'itinéraire
- 🎯 Tous les outils en une fois

### Exemple 3 : Crew basique (5 agents)

```powershell
python src/crew_voyage.py
```

**Sortie :**
- Plan de voyage de base
- Fichier généré : `voyage_plan.md`

### Exemple 2 : Agent météo seul

```powershell
python agent_meteo.py
```

**Questions possibles :**
```
- Quel temps fait-il à Tokyo ?
- Compare la météo entre Paris et Londres
- Quelle est la différence de température entre Cotonou et Paris ?
```

### Exemple 3 : Agent simple (démonstration)

```powershell
python exemple_simple.py
```

### Exemple 4 : Multi-agents basique

```powershell
python multi_agents.py
```

## 📁 Structure du projet

```
crewai-projet-agent-voyage/
│
├── config/                    # Configuration YAML
│   ├── agents.yaml           # Définition des agents (rôles, objectifs)
│   └── tasks.yaml            # Définition des tâches
│
├── src/                       # Code source principal
│   ├── crewai_simulator.py   # Simulateur CrewAI (Agent, Task, Crew)
│   ├── crew_voyage.py        # Crew basique (5 agents)
│   ├── crew_voyage_complet.py # Crew complet (6 agents + 8 outils) ⭐
│   ├── main.py               # Point d'entrée alternatif
│   └── tools/                # Bibliothèque d'outils
│       ├── __init__.py       # Exports des outils
│       └── travel_tools.py   # 8 outils professionnels ⭐
│
├── agent_meteo.py            # Agent météo standalone
├── exemple_simple.py         # Exemple 1 agent
├── multi_agents.py           # Exemple 4 agents
├── test_meteo_interactif.py  # Tests agent météo
├── test_outils.py            # Tests des 8 outils (menu interactif) ⭐
│
├── .env                       # Variables d'environnement
├── requirements.txt           # Dépendances Python
├── README.md                  # Ce fichier
├── GUIDE_DEVELOPPEMENT.md    # Guide détaillé pour débutants
└── voyage_plan.md            # Exemple de sortie générée
```

## 📚 Documentation

- **[README.md](README.md)** : Vue d'ensemble et installation
- **[GUIDE_DEVELOPPEMENT.md](GUIDE_DEVELOPPEMENT.md)** : Guide complet pour débutants
- **[config/agents.yaml](config/agents.yaml)** : Configuration des agents
- **[config/tasks.yaml](config/tasks.yaml)** : Configuration des tâches

## 🔧 Technologies utilisées

| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.13 | Langage principal |
| Groq | API Cloud | LLM ultra-rapide et gratuit |
| LangChain | 1.2.4 | Framework d'agents |
| langchain-groq | 0.1.0+ | Intégration Groq |
| requests | 2.32.5 | Appels API (météo, web) |
| pyyaml | 6.0.3 | Configuration YAML |
| SerpAPI | optionnel | Recherche Google (100/mois gratuit) |

## 📖 Comment la solution a été développée (pour débutants)

### 1️⃣ Comprendre les outils (tools)

Les **outils** sont des **fonctions Python** que vous créez pour donner des capacités spécifiques à vos agents.

**Exemple simple :**
```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Obtient la météo d'une ville."""
    # Code pour appeler l'API météo
    return "Météo: 15°C, nuageux"
```

**Comment ça marche ?**
1. Vous décorez une fonction avec `@tool`
2. Vous ajoutez une description claire (docstring)
3. L'agent peut maintenant "appeler" cette fonction
4. Le résultat est utilisé pour répondre à l'utilisateur

### 2️⃣ Créer des outils avancés

Dans notre projet, nous avons créé **8 outils** dans [src/tools/travel_tools.py](src/tools/travel_tools.py) :

**Pourquoi 8 outils ?**
- Chaque outil a une **responsabilité unique** (principe SOLID)
- Cela permet de **combiner** les outils pour des tâches complexes
- Facile à **tester** et **déboguer** individuellement

**Exemple d'outil complet :**
```python
@tool
def search_hotels(city: str, budget: str = "moyen") -> str:
    """
    Recherche d'hôtels dans une ville selon le budget.
    
    Args:
        city: Nom de la ville
        budget: 'économique', 'moyen', ou 'luxe'
    
    Returns:
        Liste d'hôtels avec prix et emplacements
    """
    # Logique de recherche basée sur le budget
    if budget == "économique":
        return "Hôtels économiques: Ibis (50-70€), B&B (40-60€)..."
    # ...
```

### 3️⃣ Assigner des outils aux agents

Chaque agent reçoit **seulement les outils dont il a besoin** :

```python
@agent
def weather_specialist(self) -> Agent:
    return Agent(
        role="Spécialiste Météo",
        goal="Fournir des prévisions météo précises",
        tools=[get_weather],  # ← Un seul outil !
        llm=self.llm
    )

@agent
def activity_planner(self) -> Agent:
    return Agent(
        role="Planificateur d'Activités",
        goal="Créer un itinéraire personnalisé",
        tools=[  # ← Plusieurs outils !
            search_activities,
            search_restaurants,
            plan_itinerary
        ],
        llm=self.llm
    )
```

**Pourquoi cette approche ?**
- ✅ Chaque agent est **spécialisé**
- ✅ Évite la **surcharge d'information**
- ✅ Plus facile à **maintenir** et **tester**

### 4️⃣ Workflow du crew

**Étape par étape :**

1. **L'utilisateur pose une question**
   ```
   "Je veux visiter Paris pendant 5 jours"
   ```

2. **Agent 1 (Recherche)** utilise `search_web`
   ```
   Trouve: "Tour Eiffel, Louvre, Montmartre..."
   ```

3. **Agent 2 (Météo)** utilise `get_weather`
   ```
   Trouve: "15°C, ensoleillé"
   ```

4. **Agent 3 (Hébergement)** utilise `search_hotels`
   ```
   Trouve: "Hôtel Ibis 70€/nuit, Le Marais"
   ```

5. **Agent 4 (Transport)** utilise `search_transport`
   ```
   Trouve: "Bruxelles→Paris: Thalys 2h, 80€"
   ```

6. **Agent 5 (Activités)** utilise 3 outils
   ```
   - search_activities: "Musées, monuments"
   - search_restaurants: "Restaurants français"
   - plan_itinerary: "Jour 1: ..., Jour 2: ..."
   ```

7. **Agent 6 (Coordination)** combine tout
   ```
   Crée le guide final en Markdown
   ```

### 5️⃣ APIs gratuites vs payantes

**Gratuites (utilisées par défaut) :**
- ☁️ **wttr.in** : Météo mondiale
- 🔍 **DuckDuckGo** : Recherche web

**Payantes (optionnelles) :**
- 🔍 **SerpAPI** : Recherche Google avancée (100 gratuit/mois)
  - Plus précis pour les attractions touristiques
  - Résultats en temps réel

**Comment ajouter SerpAPI ?**
```powershell
# 1. Créer un compte sur https://serpapi.com/
# 2. Copier votre clé API
# 3. Ajouter dans .env
SERPAPI_API_KEY=votre_clé_ici

# 4. L'outil search_web_serpapi sera automatiquement activé
```

## 🎓 Concepts clés

### Architecture CrewAI

Notre projet utilise une architecture **multi-agents** où chaque agent a :
- **Un rôle spécifique** (role)
- **Un objectif** (goal)
- **Une histoire** (backstory)
- **Des outils** (tools, optionnel)

### Décorateurs

```python
@CrewBase     # Classe de base avec config YAML
@agent        # Méthode qui retourne un Agent
@task         # Méthode qui retourne une Task
@crew         # Méthode qui retourne un Crew
```

### Processus séquentiel

Les tâches s'exécutent dans l'ordre, chaque agent recevant le contexte des agents précédents.

## 🆘 Résolution de problèmes

### Erreur : "No module named 'crewai'"

**Solution :** Nous n'utilisons pas le vrai package CrewAI (incompatible Python 3.13). Utilisez notre simulateur dans `src/crewai_simulator.py`.

### Erreur : "Invalid API Key" ou "GROQ_API_KEY non défini"

**Solution :**
```powershell
# 1. Vérifiez que votre fichier .env existe
dir .env

# 2. Vérifiez que la clé est bien définie
type .env
# Doit contenir: GROQ_API_KEY=gsk_...

# 3. Si la clé n'est pas valide, recréez-en une sur:
# https://console.groq.com
```

> 💡 **Guide complet** : Voir [GROQ_SETUP.md](GROQ_SETUP.md) pour obtenir votre clé gratuite

### Erreur : "Rate limit exceeded"

**Solution :** Vous avez dépassé le quota gratuit de Groq (30 requêtes/minute). Attendez 1 minute et réessayez.

### Erreur : "timeout" sur l'API météo

**Solution :** L'API wttr.in peut être lente. Le timeout est configuré à 15 secondes. Augmentez-le si nécessaire dans `src/tools/travel_tools.py`.

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push sur la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

Projet créé dans le cadre d'un cours sur CrewAI et les agents intelligents.

## 🙏 Remerciements

- [CrewAI](https://www.crewai.com/) pour l'inspiration architecturale
- [LangChain](https://www.langchain.com/) pour le framework
- [Groq](https://groq.com/) pour le LLM ultra-rapide et gratuit
- [wttr.in](https://wttr.in/) pour l'API météo gratuite
- [SerpAPI](https://serpapi.com/) pour l'API de recherche Google

---

⭐ Si ce projet vous a aidé, n'hésitez pas à lui donner une étoile sur GitHub !
