# 🚀 Démarrage Rapide

Si vous voulez juste tester le projet rapidement sans lire toute la documentation.

## Installation Express (5 minutes)

```powershell
# 1. Cloner le repo
git clone <votre-repo>
cd crewai-projet-agent-voyage

# 2. Installer Python 3.13 et Ollama
# Python: https://www.python.org/downloads/
# Ollama: https://ollama.ai/download

# 3. Setup
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull llama3.2:3b

# 4. Configurer .env
echo "OLLAMA_MODEL=llama3.2:3b" > .env
echo "OLLAMA_BASE_URL=http://localhost:11434" >> .env

# 5. Lancer !
python src/crew_voyage.py
```

## Exemples de commandes

```powershell
# Crew complet (5 agents)
python src/crew_voyage.py

# Agent météo seul
python agent_meteo.py

# Exemple simple
python exemple_simple.py

# Multi-agents (4 agents)
python multi_agents.py
```

## Structure minimale à connaître

```
config/          # Configuration YAML des agents
src/             # Code source principal
agent_meteo.py   # Agent météo standalone
.env             # Votre configuration
```

## Besoin d'aide ?

- 📘 [GUIDE_DEVELOPPEMENT.md](GUIDE_DEVELOPPEMENT.md) - Guide complet pour débutants
- 📖 [README.md](README.md) - Documentation complète
- ❓ Issues GitHub - Posez vos questions
