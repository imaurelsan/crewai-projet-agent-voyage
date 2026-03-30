"""
Simulateur CrewAI utilisant LangChain + Groq
Imite l'architecture CrewAI pour compatibilité avec les exemples de cours
"""

import os
import re
import sys
from datetime import date
import yaml
from typing import List, Dict, Any, Callable, Optional, Type
from functools import wraps
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

# Permet d'exécuter `python src/crewai_simulator.py` tout en gardant les imports `src.*`
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ============= Configuration LLM =============
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

if LLM_PROVIDER == "openrouter":
    from langchain_openai import ChatOpenAI
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY non défini. Obtenez une clé sur https://openrouter.ai/keys")
else:  # groq par defaut
    from langchain_groq import ChatGroq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY non défini. Obtenez une clé sur https://console.groq.com")


# ============= Classes de Base =============

class BaseTool:
    """Outil custom minimaliste (style CrewAI) avec validation simple."""

    name: str = "custom_tool"
    description: str = "Custom tool"
    args_schema: Optional[Type[BaseModel]] = None

    def invoke(self, inputs: Dict[str, Any]) -> str:
        """Point d'entree unique compatible avec le simulateur."""
        payload = inputs
        if self.args_schema:
            model = self.args_schema(**inputs)
            payload = model.model_dump() if hasattr(model, "model_dump") else model.dict()
        return self._run(**payload)

    def _run(self, **kwargs: Any) -> str:
        raise NotImplementedError("Custom tool must implement _run().")


class SimpleMemory:
    """Memoire partagee simple en RAM (liste d'entrees)."""

    def __init__(self, max_items: int = 20):
        self.max_items = max_items
        self._items: List[Dict[str, str]] = []

    def add(self, role: str, content: str) -> None:
        self._items.append({"role": role, "content": content})
        if len(self._items) > self.max_items:
            self._items.pop(0)

    def get_context(self) -> str:
        if not self._items:
            return ""
        lines = [f"{item['role']}: {item['content']}" for item in self._items]
        return "\n".join(lines)

    def clear(self) -> None:
        self._items = []

class Agent:
    """Simule un agent CrewAI"""
    
    def __init__(self, role: str, goal: str, backstory: str, 
                 verbose: bool = True, tools: List = None, llm: Any = None,
                 allow_delegation: bool = False):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose
        self.tools = tools or []
        self.llm = llm
        self.allow_delegation = allow_delegation
        
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
                 verbose: bool = True, process: str = "sequential", memory: bool = False):
        self.agents = agents
        self.tasks = tasks
        self.verbose = verbose
        self.process = process
        self.memory = SimpleMemory() if memory else None
        
        # Configuration du LLM selon le provider
        if LLM_PROVIDER == "openrouter":
            self.llm = ChatOpenAI(
                api_key=OPENROUTER_API_KEY,
                model=OPENROUTER_MODEL,
                base_url="https://openrouter.ai/api/v1",
                temperature=0.3,
                max_tokens=800
            )
        else:
            self.llm = ChatGroq(
                api_key=GROQ_API_KEY,
                model=GROQ_MODEL,
                temperature=0.3,
                max_tokens=800
            )
        
    def kickoff(self, inputs: Dict[str, Any] = None) -> str:
        """Lance l'exécution de l'équipe"""
        inputs = inputs or {}
        
        if self.verbose:
            print("="* 70)
            print("🚀 DÉMARRAGE DE L'ÉQUIPE")
            print("=" * 70)
            print(f"📋 Agents: {len(self.agents)}")
            print(f"📝 Tâches: {len(self.tasks)}")
            print(f"⚙️  Processus: {self.process}")
            print(f"🤖 LLM: {GROQ_MODEL} (Groq - ultra-rapide!)")
            print("=" * 70)
            print()
        
        results = []
        context_history = ""

        if self.memory:
            shared_memory = self.memory.get_context()
            if shared_memory and self.verbose:
                print("🧠 Memoire partagee activee")
        
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
            
            # Créer le prompt (optimisé pour bien suivre les instructions)
            # Extraire les infos clés pour les mettre en avant
            destination = inputs.get("destination", "destination inconnue")
            duration = inputs.get("duration", "3")
            budget = inputs.get("budget", "moyen")
            origin = inputs.get("origin", "origine inconnue")
            
            if full_context:
                prompt_text = f"""Rôle: {task.agent.role}
Objectif: {task.agent.goal}

INFORMATIONS IMPORTANTES:
- Destination: {destination}
- Durée: {duration} jours
- Budget: {budget}
- Départ: {origin}

Contexte: {full_context[-1500:]}

Tâche: {description}

IMPORTANT: Concentre-toi UNIQUEMENT sur {destination}. Ne propose JAMAIS d'autres destinations."""
            else:
                prompt_text = f"""Rôle: {task.agent.role}
Objectif: {task.agent.goal}

INFORMATIONS IMPORTANTES:
- Destination: {destination}
- Durée: {duration} jours
- Budget: {budget}
- Départ: {origin}

Tâche: {description}

IMPORTANT: Concentre-toi UNIQUEMENT sur {destination}. Ne propose JAMAIS d'autres destinations."""
            
            # Exécuter avec le LLM
            if self.verbose:
                print(f"🤖 {task.agent.role} travaille...\n")
            
            # Utiliser les outils si disponibles
            if task.agent.tools:
                # Appeler les outils si nécessaire
                tool_results = []
                for tool in task.agent.tools:
                    try:
                        if hasattr(tool, "args_schema") and tool.args_schema:
                            required_fields = [
                                name
                                for name, field in tool.args_schema.model_fields.items()
                                if field.is_required()
                            ]
                            if any(field not in inputs for field in required_fields):
                                continue
                        if hasattr(tool, "invoke"):
                            tool_result = tool.invoke(inputs)
                            tool_results.append(tool_result)
                        elif callable(tool):
                            tool_result = tool(inputs)
                            tool_results.append(tool_result)
                    except Exception as e:
                        if self.verbose:
                            print(f"⚠️  Erreur outil: {e}")
                
                if tool_results:
                    prompt_text += f"\n\nRésultats des outils:\n" + "\n".join(tool_results)
            
            result = self.llm.invoke(prompt_text)
            result_text = result.content if hasattr(result, "content") else str(result)
            results.append(result_text)
            context_history += f"\n\n=== {task.agent.role} ===\n{result_text}"

            if self.memory:
                self.memory.add(task.agent.role, result_text)
            
            if self.verbose:
                print(f"✅ Résultat:\n{result_text}")
            
            # Sauvegarder dans un fichier si spécifié
            if task.output_file:
                with open(task.output_file, 'w', encoding='utf-8') as f:
                    f.write(result_text)
                if self.verbose:
                    print(f"💾 Sauvegardé dans: {task.output_file}")
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("✨ ÉQUIPE TERMINÉE")
            print(f"{'='*70}\n")
        
        # Retourner le dernier résultat (généralement la synthèse finale)
        return results[-1] if results else ""


def run_telegram_bot(crew_factory: Callable[[], Crew], token: Optional[str] = None) -> None:
    """Handler Telegram minimaliste (polling) qui envoie le texte a un crew.

    Usage:
        from src.crewai_simulator import run_telegram_bot
        from src.crew_voyage_complet import CompleteTravelCrew

        run_telegram_bot(lambda: CompleteTravelCrew().crew())
    """
    token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN non defini. Ajoutez-le dans votre .env."
        )
    try:
        from telegram import Update
        from telegram.ext import Application, MessageHandler, filters
    except Exception as exc:
        raise ImportError(
            "Installez python-telegram-bot: pip install python-telegram-bot"
        ) from exc

    def _extract_travel_inputs(text: str) -> Dict[str, str]:
        """Extraction naive des infos depuis un texte libre (version debutant)."""
        data: Dict[str, str] = {}

        months = {
            "janvier": 1,
            "fevrier": 2,
            "février": 2,
            "mars": 3,
            "avril": 4,
            "mai": 5,
            "juin": 6,
            "juillet": 7,
            "aout": 8,
            "août": 8,
            "septembre": 9,
            "octobre": 10,
            "novembre": 11,
            "decembre": 12,
            "décembre": 12,
        }

        def _parse_date(day_str: str, month_str: str) -> date:
            year = date.today().year
            month = months.get(month_str.lower())
            if not month:
                return None
            return date(year, month, int(day_str))

        # Destination
        match = re.search(r"\bje vais\s+(?:au|a|à|aux|en)\s+([^,\.\n]+)", text, re.IGNORECASE)
        if match:
            data["destination"] = match.group(1).strip()

        # Origine
        match = re.search(r"\bje pars\s+de\s+([^,\.\n]+)", text, re.IGNORECASE)
        if match:
            data["origin"] = match.group(1).strip()

        # Duree
        match = re.search(r"\b(pour|pendant)\s+(\d+)\s+jours\b", text, re.IGNORECASE)
        if match:
            data["duration"] = match.group(2).strip()

        # Dates debut/fin (ex: "le 28 fevrier" / "je reviens le 31 mars")
        start_match = re.search(r"\ble\s+(\d{1,2})\s+([a-zA-Zéûîôàù]+)", text, re.IGNORECASE)
        end_match = re.search(r"\bje reviens\s+le\s+(\d{1,2})\s+([a-zA-Zéûîôàù]+)", text, re.IGNORECASE)
        if start_match and end_match and "duration" not in data:
            start_date = _parse_date(start_match.group(1), start_match.group(2))
            end_date = _parse_date(end_match.group(1), end_match.group(2))
            if start_date and end_date:
                if end_date < start_date:
                    end_date = date(start_date.year + 1, end_date.month, end_date.day)
                duration_days = (end_date - start_date).days + 1
                if duration_days > 0:
                    data["duration"] = str(duration_days)

        # Budget (mot ou montant)
        match = re.search(r"\bbudget\s+(\d+)\s*€?", text, re.IGNORECASE)
        if match:
            amount = int(match.group(1))
            if amount < 800:
                data["budget"] = "economique"
            elif amount < 2000:
                data["budget"] = "moyen"
            else:
                data["budget"] = "luxe"
        else:
            match = re.search(r"\bbudget\s+(economique|économique|moyen|luxe)\b", text, re.IGNORECASE)
            if match:
                data["budget"] = match.group(1).replace("é", "e").lower()

        return data

    def _split_telegram_message(text: str, max_len: int = 3500) -> List[str]:
        """Decoupe un long message pour respecter la limite Telegram."""
        if len(text) <= max_len:
            return [text]
        parts = []
        start = 0
        while start < len(text):
            parts.append(text[start:start + max_len])
            start += max_len
        return parts

    async def handle_message(update: Update, context) -> None:
        user_text = update.message.text if update.message else ""
        if not user_text:
            return

        await update.message.reply_text("🤖 Je prepare votre voyage...")

        inputs = {"user_request": user_text}
        extracted = _extract_travel_inputs(user_text)
        if extracted:
            inputs.update(extracted)

        # Valeurs par defaut si une info manque
        inputs.setdefault("destination", "destination inconnue")
        inputs.setdefault("origin", "origine inconnue")
        inputs.setdefault("duration", "3")
        inputs.setdefault("budget", "moyen")

        try:
            crew = crew_factory(inputs)
        except TypeError:
            crew = crew_factory()

        if hasattr(crew, "verbose"):
            crew.verbose = False  # Desactiver logs pour economiser tokens

        try:
            result = crew.kickoff(inputs=inputs)
            result_text = result.content if hasattr(result, "content") else str(result)
            for chunk in _split_telegram_message(result_text):
                await update.message.reply_text(chunk)
        except Exception as exc:
            print(f"\n❌ ERREUR BOT: {type(exc).__name__}")
            print(f"📝 Message: {str(exc)}")
            import traceback
            traceback.print_exc()
            
            message = str(exc)
            if "rate_limit" in message.lower() or "RateLimitError" in message or "429" in message:
                await update.message.reply_text(
                    "⚠️ Limite Groq atteinte. Reessayez dans quelques minutes."
                )
            else:
                await update.message.reply_text(
                    f"⚠️ Erreur: {type(exc).__name__}"
                )

    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()


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
    
    def __init__(self, model: str = None, temperature: float = 0.7, api_key: str = None):
        self.model = model or GROQ_MODEL
        self.temperature = temperature
        self.api_key = api_key or GROQ_API_KEY
        self._llm = ChatGroq(
            api_key=self.api_key,
            model=self.model,
            temperature=self.temperature
        )
    
    def __repr__(self):
        return f"LLM(model='{self.model}')"


class DirectFlowAdapter:
    """Flow direct: un seul appel LLM avec contraintes strictes (haute précision, faible complexité)."""

    def __init__(self):
        self.verbose = False
        self._llm = Crew(agents=[], tasks=[], verbose=False).llm

    def kickoff(self, inputs: Dict[str, Any] = None) -> str:
        inputs = inputs or {}
        destination = inputs.get("destination", "destination inconnue")
        origin = inputs.get("origin", "origine inconnue")
        duration = inputs.get("duration", "3")
        budget = inputs.get("budget", "moyen")
        request = inputs.get("user_request", "Prépare un plan de voyage")

        prompt = f"""Tu dois produire une réponse précise et concise.

Demande utilisateur: {request}
Contraintes obligatoires:
- Destination: {destination}
- Départ: {origin}
- Durée: {duration} jours
- Budget: {budget}

Donne un plan clair en sections: transport, hébergement, activités, budget estimatif.
Ne propose aucune autre destination que {destination}."""

        result = self._llm.invoke(prompt)
        return result.content if hasattr(result, "content") else str(result)


class OrchestrationRouter:
    """Route automatiquement vers Crew ou Flow selon complexité x précision."""

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.last_decision = "unknown"

    @staticmethod
    def _score_complexity(inputs: Dict[str, Any]) -> int:
        text = (inputs.get("user_request") or "").lower()
        score = 1
        constraints = [
            "destination", "origin", "duration", "budget"
        ]
        score += sum(1 for key in constraints if inputs.get(key) and "inconnue" not in str(inputs.get(key)).lower())

        complexity_keywords = [
            "compar", "plusieurs", "multi", "itiner", "itinér", "optimis", "risque", "scenario", "scénario",
            "roadmap", "90 jours", "phase", "coord", "hiérarch"
        ]
        if any(keyword in text for keyword in complexity_keywords):
            score += 3

        if len(text) > 220:
            score += 1

        return max(1, min(score, 10))

    @staticmethod
    def _score_precision(inputs: Dict[str, Any]) -> int:
        text = (inputs.get("user_request") or "").lower()
        score = 1

        if inputs.get("destination") and "inconnue" not in str(inputs.get("destination")).lower():
            score += 2
        if inputs.get("duration") and str(inputs.get("duration")).isdigit():
            score += 2
        if inputs.get("budget") and "inconnu" not in str(inputs.get("budget")).lower():
            score += 2
        if inputs.get("origin") and "inconnue" not in str(inputs.get("origin")).lower():
            score += 1

        precision_keywords = ["exact", "précis", "precis", "contraintes", "budget", "dates", "éviter", "uniquement"]
        if any(keyword in text for keyword in precision_keywords):
            score += 2

        return max(1, min(score, 10))

    def __call__(self, inputs: Dict[str, Any] = None):
        inputs = inputs or {}
        complexity = self._score_complexity(inputs)
        precision = self._score_precision(inputs)

        if complexity <= 4 and precision <= 4:
            self.last_decision = "simple_crew"
            agent = Agent(
                role="Assistant Voyage",
                goal="Fournir un plan de voyage simple",
                backstory="Assistant orienté réponses rapides",
                verbose=False,
            )
            task = Task(
                description="Créer un plan simple pour {destination}, {duration} jours, budget {budget}.",
                expected_output="Plan simple en 4 sections",
                agent=agent,
            )
            return Crew(agents=[agent], tasks=[task], verbose=False)

        if complexity <= 4 and precision >= 5:
            self.last_decision = "direct_flow"
            return DirectFlowAdapter()

        if complexity >= 5 and precision <= 4:
            self.last_decision = "complex_crew"
            from src.crew_voyage_complet import CompleteTravelCrew
            return CompleteTravelCrew().crew()

        self.last_decision = "orchestrated_flow"
        from src.agents_collaboration import create_collaboration_crew
        return create_collaboration_crew(self.project_root)


# ============= Point d'entrée pour le bot Telegram =============

if __name__ == "__main__":
    print("🤖 Démarrage du bot Telegram...")
    if LLM_PROVIDER == "openrouter":
        print(f"📡 Provider: OpenRouter")
        print(f"📡 Modèle: {OPENROUTER_MODEL}")
    else:
        print(f"📡 Provider: Groq")
        print(f"📡 Modèle: {GROQ_MODEL}")
    
    try:
        print("🧭 Mode auto-routing actif (complexité x précision)")
        router = OrchestrationRouter(PROJECT_ROOT)
        run_telegram_bot(router)
    except Exception as routing_error:
        print(f"⚠️ Auto-routing indisponible: {routing_error}")
        print("↩️ Fallback vers crew simple...")

        def simple_crew(_inputs: Dict[str, Any] = None):
            agent = Agent(
                role="Planificateur de voyage",
                goal="Créer un plan de voyage simple",
                backstory="Expert en voyages",
                verbose=False
            )
            task = Task(
                description="Crée un plan pour: {destination}, durée: {duration} jours, budget: {budget}",
                expected_output="Un guide concis",
                agent=agent
            )
            return Crew(agents=[agent], tasks=[task], verbose=False)

        run_telegram_bot(simple_crew)
