# 🌍 Projet CrewAI - Agent de Voyage Intelligent

Un système multi-agents de planification de voyage utilisant l'architecture CrewAI avec LangChain et Ollama (100% local et gratuit).

![Python Version](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

## 📋 Table des matières

- [Aperçu du projet](#aperçu-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation rapide](#installation-rapide)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Documentation](#documentation)
- [Contribution](#contribution)

## 🎯 Aperçu du projet

Ce projet simule un **crew d'agents intelligents** travaillant ensemble pour planifier des voyages personnalisés. Il utilise une architecture inspirée de CrewAI mais adaptée pour fonctionner avec **Ollama** (LLM local gratuit) et **LangChain**.

### Pourquoi ce projet ?

- ✅ **100% gratuit** : Pas de clé API payante requise
- ✅ **100% local** : Vos données restent sur votre machine
- ✅ **Architecture professionnelle** : Inspirée de CrewAI (compatible avec les cours)
- ✅ **Extensible** : Ajoutez facilement de nouveaux agents et outils

## ✨ Fonctionnalités

### 🤖 5 Agents spécialisés

1. **Chercheur de destinations** 🔍
   - Trouve les meilleures attractions
   - Recommande des quartiers et activités
   - Conseils pratiques de voyage

2. **Spécialiste Météo** ☁️
   - Données météo en temps réel (API wttr.in)
   - Comparaison entre villes
   - Recommandations vestimentaires

3. **Expert en Gastronomie** 🍽️
   - Spécialités locales à essayer
   - Meilleurs restaurants
   - Budget alimentaire estimé

4. **Planificateur de Budget** 💰
   - Estimation détaillée des coûts
   - Options économique/moyen/luxe
   - Hébergement, transport, activités

5. **Coordinateur de Voyage** 🎯
   - Synthèse de toutes les informations
   - Création d'itinéraire complet
   - Export en fichier Markdown

### 🛠️ Outils disponibles

- **get_weather** : Récupération météo en temps réel
- **compare_weather** : Comparaison entre deux villes
- Architecture extensible pour ajouter vos propres outils

## 🏗️ Architecture

```python
@CrewBase
class TravelCrew():
    @agent
    def researcher(self) -> Agent:
        # Configuration depuis agents.yaml
        
    @task
    def research_task(self) -> Task:
        # Configuration depuis tasks.yaml
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[...],
            tasks=[...],
            process=Process.sequential
        )
```

**Processus d'exécution :**
```
1. Recherche → 2. Météo → 3. Gastronomie → 4. Budget → 5. Coordination
                                                              ↓
                                                      voyage_plan.md
```

## 🚀 Installation rapide

### Prérequis

- **Python 3.13** ([Télécharger](https://www.python.org/downloads/))
- **Ollama** ([Télécharger](https://ollama.ai/download))

### Étapes d'installation

```powershell
# 1. Cloner le projet
git clone <votre-repo>
cd crewai-projet-agent-voyage

# 2. Créer l'environnement virtuel
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Télécharger le modèle Ollama (2GB)
ollama pull llama3.2:3b

# 5. Configurer les variables d'environnement
# Créer un fichier .env avec :
# OLLAMA_MODEL=llama3.2:3b
# OLLAMA_BASE_URL=http://localhost:11434
```

## 💻 Utilisation

### Exemple 1 : Crew complet (5 agents)

```powershell
python src/crew_voyage.py
```

**Entrée :**
```
Quelle destination voulez-vous explorer? Paris
```

**Sortie :**
- Plan de voyage détaillé sur 7 jours
- Budget estimé (économique/moyen/luxe)
- Recommandations gastronomiques
- Analyse météo
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
│   ├── crew_voyage.py        # Crew principal (5 agents)
│   └── main.py               # Point d'entrée alternatif
│
├── agent_meteo.py            # Agent météo standalone
├── exemple_simple.py         # Exemple 1 agent
├── multi_agents.py           # Exemple 4 agents
├── test_meteo_interactif.py  # Tests agent météo
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
| Ollama | 0.14.1 | Serveur LLM local |
| LangChain | 1.2.4 | Framework d'agents |
| langchain-ollama | 1.0.1 | Intégration Ollama |
| requests | 2.32.5 | API météo |
| pyyaml | 6.0.3 | Configuration YAML |

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

### Erreur : "Ollama connection refused"

**Solution :**
```powershell
# Vérifier qu'Ollama est lancé
ollama --version
ollama list

# Redémarrer Ollama si nécessaire
```

### Erreur : "timeout" sur l'API météo

**Solution :** L'API wttr.in peut être lente. Le timeout est configuré à 15 secondes. Augmentez-le si nécessaire dans `agent_meteo.py`.

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
- [Ollama](https://ollama.ai/) pour le LLM local gratuit
- [wttr.in](https://wttr.in/) pour l'API météo gratuite

---

⭐ Si ce projet vous a aidé, n'hésitez pas à lui donner une étoile sur GitHub !
