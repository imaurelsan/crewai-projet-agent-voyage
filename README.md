# CrewAI Travel Planner — Structured Output, Collaboration & MCP

Projet pédagogique (débutant-friendly) qui implémente un système multi-agents complet autour de 3 briques:

1. Structured output (format de réponse exploitable)
2. Agents collaboration (délégation + questions inter-agents)
3. Intégration MCP (FileSystem local)

Le projet reste compatible Python 3.13 via un simulateur CrewAI maison.

## Ce qui a été implémenté

### 1) Structured Output (rappel)
- Support d'un flux orienté données structurées (type Pydantic) côté orchestration.
- Objectif: produire des sorties plus fiables et faciles à réutiliser (API, UI, stockage).

### 2) Agents Collaboration (nouveau)
Implémentation des patterns recommandés:

- **Clear role definition**: rôles spécialisés et non ambigus
- **Strategic delegation**: `allow_delegation=True` pour les coordinateurs, `False` pour les spécialistes
- **Context sharing**: transmission de contexte entre étapes
- **Clear task descriptions**: instructions explicites et actionnables

Nouveaux composants:
- [src/agents_collaboration.py](src/agents_collaboration.py)
	- `CollaborationOrchestrator`
	- `DelegateWorkTool`
	- `AskQuestionTool`
	- Patterns:
		- Research → Write → Edit
		- Collaborative Single Task
		- Hierarchical Collaboration (manager + spécialistes)

### 3) MCP Integration (nouveau)
Intégration d'un MCP **FileSystem local**:

- `MCPFilesystemTool` dans [src/agents_collaboration.py](src/agents_collaboration.py)
- Actions supportées:
	- `list_directory`
	- `read_file`
- Sécurisation par racine (empêche l'accès hors dossier autorisé)

### 4) Base simulateur enrichie
- `Agent` supporte désormais `allow_delegation` dans [src/crewai_simulator.py](src/crewai_simulator.py)

## Architecture rapide

- [src/crewai_simulator.py](src/crewai_simulator.py): simulateur CrewAI, mémoire partagée, bot Telegram
- [src/crew_voyage_complet.py](src/crew_voyage_complet.py): crew voyage historique
- [src/agents_collaboration.py](src/agents_collaboration.py): orchestration collaboration + MCP
- [src/agents_collaboration_demo.py](src/agents_collaboration_demo.py): démo complète exécutable
- [src/tools/travel_tools.py](src/tools/travel_tools.py): outils métier voyage

## Routing automatique Complexité x Précision

Le bot Telegram applique une matrice de décision inspirée de la doc CrewAI pour choisir l'orchestration:

- **Low complexity (1-4), Low precision (1-4)** → `Simple Crew`
- **Low complexity (1-4), High precision (5-10)** → `Direct Flow` (appel LLM direct, contraintes strictes)
- **High complexity (5-10), Low precision (1-4)** → `Complex Crew` (crew voyage complet)
- **High complexity (5-10), High precision (5-10)** → `Orchestrated Flow` (collaboration hiérarchique + MCP)

Implémentation:
- `OrchestrationRouter` dans [src/crewai_simulator.py](src/crewai_simulator.py)
- `DirectFlowAdapter` dans [src/crewai_simulator.py](src/crewai_simulator.py)
- `CollaborationCrewAdapter` dans [src/agents_collaboration.py](src/agents_collaboration.py)

## Installation

```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install python-telegram-bot langchain-openai
```

Configurer [.env](.env):
- `LLM_PROVIDER=groq` ou `openrouter`
- clé API correspondante
- `TELEGRAM_BOT_TOKEN` pour le bot

## Exécution

### A. Bot Telegram (cas d'usage voyage)

```powershell
.\venv\Scripts\python.exe src/crewai_simulator.py
```

Par défaut, ce lancement active maintenant le mode collaboration:
- Delegate Work Tool
- Ask Question Tool
- Orchestration hiérarchique
- MCP FileSystem local

Exemple message:
`Je vais au Senegal le 28 fevrier, je reviens le 31 mars, budget 4000€, je pars de Paris.`

### B. Démo Agents Collaboration + MCP

```powershell
.\venv\Scripts\python.exe src/agents_collaboration_demo.py
```

La démo exécute:
1. Delegate Work Tool
2. Ask Question Tool
3. Pattern Research-Write-Edit
4. Pattern Collaborative Single Task
5. Pattern Hiérarchique

## Best practices appliquées

- Rôles complémentaires (pas de chevauchement)
- Délégation uniquement pour rôles coordinateurs
- Spécialistes focalisés sur leur expertise
- Context sharing contrôlé entre étapes
- Mémoire partagée pour continuité inter-agents
- Tâches explicites avec résultats attendus
- Intégration MCP outillée et sécurisée

## Dépannage

- Rate limit Groq: basculer vers OpenRouter dans [.env](.env)
- Conflit Telegram `getUpdates`: garder une seule instance du bot
- Erreur import: lancer les commandes depuis la racine du repo

## Résumé intégral du travail

Ce projet implémente maintenant un système d'orchestration multi-agents complet:

- **Structured Output** pour des réponses exploitables
- **Collaboration inter-agents** avec délégation + questions expert
- **Processus séquentiel et hiérarchique** selon la complexité
- **MCP FileSystem** intégré pour connecter les agents à des ressources locales

Tu peux l'utiliser tel quel pour apprendre les patterns CrewAI de collaboration, puis le faire évoluer vers d'autres MCP (HTTP/SSE, outils distants, marketplace AMP).
