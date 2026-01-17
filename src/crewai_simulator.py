"""
Simulateur CrewAI utilisant LangChain + Ollama
Imite l'architecture CrewAI pour compatibilité avec les exemples de cours
"""

import os
import yaml
from typing import List, Dict, Any, Callable
from functools import wraps
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# ============= Configuration =============
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


# ============= Classes de Base =============

class Agent:
    """Simule un agent CrewAI"""
    
    def __init__(self, role: str, goal: str, backstory: str, 
                 verbose: bool = True, tools: List = None, llm: Any = None):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.tools = tools or []
        self.llm = llm
        
    def __repr__(self):
        return f"Agent(role='{self.role}')"


class Task:
    """Simule une tâche CrewAI"""
    
    def __init__(self, description: str, expected_output: str, 
                 agent: Agent = None, context: List = None, output_file: str = None):
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.context = context or []
        self.output_file = output_file
        
    def __repr__(self):
        return f"Task(agent={self.agent.role if self.agent else 'None'})"


class Crew:
    """Simule une équipe CrewAI"""
    
    def __init__(self, agents: List[Agent], tasks: List[Task], 
                 verbose: bool = True, process: str = "sequential"):
        self.agents = agents
        self.tasks = tasks
        self.verbose = verbose
        self.process = process
        self.llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.7)
        
    def kickoff(self, inputs: Dict[str, Any] = None) -> str:
        """Lance l'exécution de l'équipe"""
        inputs = inputs or {}
        
        if self.verbose:
            print("=" * 70)
            print("🚀 DÉMARRAGE DE L'ÉQUIPE")
            print("=" * 70)
            print(f"📋 Agents: {len(self.agents)}")
            print(f"📝 Tâches: {len(self.tasks)}")
            print(f"⚙️  Processus: {self.process}")
            print(f"🤖 LLM: {OLLAMA_MODEL}")
            print("=" * 70)
            print()
        
        results = []
        context_history = ""
        
        for i, task in enumerate(self.tasks, 1):
            if self.verbose:
                print(f"\n{'='*70}")
                print(f"📌 TÂCHE {i}/{len(self.tasks)}: {task.agent.role if task.agent else 'Agent non assigné'}")
                print(f"{'='*70}")
            
            # Remplacer les variables dans la description
            description = task.description
            for key, value in inputs.items():
                description = description.replace(f"{{{key}}}", str(value))
            
            # Ajouter le contexte des tâches précédentes si spécifié
            full_context = context_history
            if task.context:
                for j, context_task in enumerate(task.context):
                    # Utiliser l'index de la boucle au lieu de chercher dans la liste
                    if j < len(results):
                        agent_role = context_task.agent.role if context_task.agent else "Agent"
                        full_context += f"\n\nContexte de '{agent_role}':\n{results[j]}"
            
            # Créer le prompt
            if full_context:
                prompt_text = f"""Tu es {task.agent.role}.

Ton objectif: {task.agent.goal}

Background: {task.agent.backstory}

Contexte des tâches précédentes:
{full_context}

Tâche à accomplir:
{description}

Output attendu: {task.expected_output}

Réponds de manière détaillée et professionnelle."""
            else:
                prompt_text = f"""Tu es {task.agent.role}.

Ton objectif: {task.agent.goal}

Background: {task.agent.backstory}

Tâche à accomplir:
{description}

Output attendu: {task.expected_output}

Réponds de manière détaillée et professionnelle."""
            
            # Exécuter avec le LLM
            if self.verbose:
                print(f"🤖 {task.agent.role} travaille...\n")
            
            # Utiliser les outils si disponibles
            if task.agent.tools:
                # Appeler les outils si nécessaire
                tool_results = []
                for tool in task.agent.tools:
                    if callable(tool):
                        try:
                            # Extraire les paramètres depuis les inputs
                            tool_result = tool.invoke(inputs)
                            tool_results.append(tool_result)
                        except Exception as e:
                            if self.verbose:
                                print(f"⚠️  Erreur outil: {e}")
                
                if tool_results:
                    prompt_text += f"\n\nRésultats des outils:\n" + "\n".join(tool_results)
            
            result = self.llm.invoke(prompt_text)
            results.append(result)
            context_history += f"\n\n=== {task.agent.role} ===\n{result}"
            
            if self.verbose:
                print(f"✅ Résultat:\n{result}")
            
            # Sauvegarder dans un fichier si spécifié
            if task.output_file:
                with open(task.output_file, 'w', encoding='utf-8') as f:
                    f.write(result)
                if self.verbose:
                    print(f"💾 Sauvegardé dans: {task.output_file}")
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("✨ ÉQUIPE TERMINÉE")
            print(f"{'='*70}\n")
        
        # Retourner le dernier résultat (généralement la synthèse finale)
        return results[-1] if results else ""


# ============= Décorateurs =============

def CrewBase(cls):
    """Décorateur de classe pour simuler @CrewBase de CrewAI"""
    
    # Charger les configurations YAML
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
    
    agents_config_path = os.path.join(config_dir, 'agents.yaml')
    tasks_config_path = os.path.join(config_dir, 'tasks.yaml')
    
    if os.path.exists(agents_config_path):
        with open(agents_config_path, 'r', encoding='utf-8') as f:
            cls.agents_config = yaml.safe_load(f)
    else:
        cls.agents_config = {}
    
    if os.path.exists(tasks_config_path):
        with open(tasks_config_path, 'r', encoding='utf-8') as f:
            cls.tasks_config = yaml.safe_load(f)
    else:
        cls.tasks_config = {}
    
    return cls


def agent(func: Callable) -> Callable:
    """Décorateur pour marquer une méthode comme agent"""
    func._is_agent = True
    return func


def task(func: Callable) -> Callable:
    """Décorateur pour marquer une méthode comme tâche"""
    func._is_task = True
    return func


def crew(func: Callable) -> Callable:
    """Décorateur pour marquer une méthode comme crew"""
    func._is_crew = True
    return func


# ============= Process Enum =============

class Process:
    """Simule l'enum Process de CrewAI"""
    sequential = "sequential"
    hierarchical = "hierarchical"


# ============= LLM Helper =============

class LLM:
    """Wrapper pour le LLM compatible avec la syntaxe CrewAI"""
    
    def __init__(self, model: str = None, temperature: float = 0.7, base_url: str = None):
        self.model = model or OLLAMA_MODEL
        self.temperature = temperature
        self.base_url = base_url or OLLAMA_BASE_URL
        self._llm = OllamaLLM(
            model=self.model,
            base_url=self.base_url,
            temperature=self.temperature
        )
    
    def __repr__(self):
        return f"LLM(model='{self.model}')"
