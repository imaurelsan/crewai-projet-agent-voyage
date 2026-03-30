"""
Système d'orchestration de collaboration entre agents + intégration MCP FileSystem.

Implémente:
- Delegate Work Tool (déléguer à un autre agent)
- Ask Question Tool (questionner un expert)
- Patterns de collaboration (RWE, collaborative, hiérarchique)
- Intégration MCP locale de type FileSystem
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from src.crewai_simulator import Agent, BaseTool, Crew, Process, SimpleMemory

ROLE_RESEARCHER = "Research Specialist"
ROLE_WRITER = "Content Writer"
ROLE_EDITOR = "Editor"
ROLE_MANAGER = "Project Manager"


class DelegateWorkInput(BaseModel):
    task: str = Field(..., description="Tâche à déléguer")
    coworker_role: str = Field(..., description="Rôle cible")
    context: str = Field(default="", description="Contexte optionnel")


class AskQuestionInput(BaseModel):
    question: str = Field(..., description="Question à poser")
    coworker_role: str = Field(..., description="Rôle cible")
    context: str = Field(default="", description="Contexte optionnel")


class MCPFilesystemInput(BaseModel):
    action: str = Field(..., description="Action: list_directory ou read_file")
    path: str = Field(default=".", description="Chemin relatif à la racine MCP")
    max_chars: int = Field(default=4000, ge=200, le=20000)


class MCPFilesystemTool(BaseTool):
    name = "mcp_filesystem"
    description = "MCP FileSystem local: lister un dossier ou lire un fichier"
    args_schema = MCPFilesystemInput

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()

    def _resolve_path(self, relative_path: str) -> Path:
        target = (self.root_dir / relative_path).resolve()
        if self.root_dir not in target.parents and target != self.root_dir:
            raise ValueError("Accès refusé: chemin hors racine MCP")
        return target

    def _run(self, action: str, path: str = ".", max_chars: int = 4000) -> str:
        target = self._resolve_path(path)

        if action == "list_directory":
            if not target.exists() or not target.is_dir():
                return f"[MCP] Dossier introuvable: {path}"
            items = []
            for child in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                suffix = "/" if child.is_dir() else ""
                items.append(f"- {child.relative_to(self.root_dir)}{suffix}")
            joined = "\n".join(items)
            return f"[MCP:list_directory]\n{joined[:max_chars]}"

        if action == "read_file":
            if not target.exists() or not target.is_file():
                return f"[MCP] Fichier introuvable: {path}"
            content = target.read_text(encoding="utf-8", errors="ignore")
            return f"[MCP:read_file] {path}\n{content[:max_chars]}"

        return "[MCP] Action non supportée. Utilisez list_directory ou read_file."


class CollaborationOrchestrator:
    """Orchestrateur de collaboration entre agents avec mémoire partagée."""

    def __init__(self, agents: List[Agent], process: str = Process.sequential, memory: bool = True):
        self.agents_by_role: Dict[str, Agent] = {agent.role: agent for agent in agents}
        self.process = process
        self.memory = SimpleMemory(max_items=30) if memory else None
        self.execution_crew = Crew(agents=agents, tasks=[], verbose=False, process=process, memory=False)

    def _memory_context(self) -> str:
        if not self.memory:
            return ""
        return self.memory.get_context()

    def _run_agent(self, role: str, instruction: str, context: str = "") -> str:
        agent = self.agents_by_role.get(role)
        if not agent:
            return f"Agent introuvable: {role}"

        prompt = f"""Rôle: {agent.role}
Objectif: {agent.goal}
Backstory: {agent.backstory}

Mémoire partagée:
{self._memory_context()}

Contexte:
{context}

Instruction:
{instruction}

Réponds de manière concise, précise et actionnable."""

        response = self.execution_crew.llm.invoke(prompt)
        text = response.content if hasattr(response, "content") else str(response)
        if self.memory:
            self.memory.add(agent.role, text)
        return text

    def delegate(self, from_role: str, coworker_role: str, task: str, context: str = "") -> str:
        owner = self.agents_by_role.get(from_role)
        if not owner:
            return f"Agent source introuvable: {from_role}"
        if not owner.allow_delegation:
            return f"Délégation refusée: {from_role} n'a pas allow_delegation=True"

        instruction = f"Tâche déléguée par {from_role}: {task}"
        return self._run_agent(coworker_role, instruction, context=context)

    def ask_question(self, from_role: str, coworker_role: str, question: str, context: str = "") -> str:
        owner = self.agents_by_role.get(from_role)
        if not owner:
            return f"Agent source introuvable: {from_role}"
        if not owner.allow_delegation:
            return f"Question refusée: {from_role} n'a pas allow_delegation=True"

        instruction = f"Question d'un collègue ({from_role}): {question}"
        return self._run_agent(coworker_role, instruction, context=context)

    def run_research_write_edit(self, topic: str) -> str:
        research = self._run_agent(
            ROLE_RESEARCHER,
            f"Recherche les derniers développements sur: {topic}. Donne des points structurés.",
        )
        draft = self._run_agent(
            ROLE_WRITER,
            "Rédige un article de 600-800 mots basé sur la recherche.",
            context=research,
        )
        edited = self._run_agent(
            ROLE_EDITOR,
            "Édite et améliore la clarté, le flow, et la qualité de publication.",
            context=draft,
        )
        return edited

    def run_collaborative_single_task(self, brief: str) -> str:
        writer_role = ROLE_WRITER
        market_analysis = self.delegate(
            from_role=writer_role,
            coworker_role=ROLE_RESEARCHER,
            task="Fournis analyse marché + concurrents + signaux produits",
            context=brief,
        )
        expert_answer = self.ask_question(
            from_role=writer_role,
            coworker_role=ROLE_RESEARCHER,
            question="Quelles sont les 3 hypothèses les plus risquées à valider ?",
            context=brief,
        )
        return self._run_agent(
            writer_role,
            "Produis une stratégie marketing complète et structurée.",
            context=f"Brief:\n{brief}\n\nAnalyse déléguée:\n{market_analysis}\n\nQ/R expert:\n{expert_answer}",
        )

    def run_hierarchical(self, project_goal: str) -> str:
        manager = ROLE_MANAGER
        research = self.delegate(
            from_role=manager,
            coworker_role=ROLE_RESEARCHER,
            task="Collecte les faits clés et insights marché.",
            context=project_goal,
        )
        writing = self.delegate(
            from_role=manager,
            coworker_role=ROLE_WRITER,
            task="Rédige un plan exécutable en 5 étapes.",
            context=f"Objectif:\n{project_goal}\n\nDonnées recherche:\n{research}",
        )
        return self._run_agent(
            manager,
            "Synthétise et valide le plan final. Mets les priorités et risques.",
            context=f"Research:\n{research}\n\nDraft:\n{writing}",
        )


class DelegateWorkTool(BaseTool):
    name = "delegate_work"
    description = "Délègue une tâche à un autre agent"
    args_schema = DelegateWorkInput

    def __init__(self, orchestrator: CollaborationOrchestrator, owner_role: str):
        self.orchestrator = orchestrator
        self.owner_role = owner_role

    def _run(self, task: str, coworker_role: str, context: str = "") -> str:
        return self.orchestrator.delegate(
            from_role=self.owner_role,
            coworker_role=coworker_role,
            task=task,
            context=context,
        )


class AskQuestionTool(BaseTool):
    name = "ask_question"
    description = "Pose une question ciblée à un agent expert"
    args_schema = AskQuestionInput

    def __init__(self, orchestrator: CollaborationOrchestrator, owner_role: str):
        self.orchestrator = orchestrator
        self.owner_role = owner_role

    def _run(self, question: str, coworker_role: str, context: str = "") -> str:
        return self.orchestrator.ask_question(
            from_role=self.owner_role,
            coworker_role=coworker_role,
            question=question,
            context=context,
        )


class CollaborationCrewAdapter:
    """Adaptateur compatible `kickoff(inputs=...)` pour usage direct dans Telegram."""

    def __init__(self, orchestrator: CollaborationOrchestrator):
        self.orchestrator = orchestrator
        self.verbose = False

    def kickoff(self, inputs: Optional[Dict[str, str]] = None) -> str:
        inputs = inputs or {}
        destination = inputs.get("destination", "destination inconnue")
        duration = inputs.get("duration", "3")
        budget = inputs.get("budget", "moyen")
        origin = inputs.get("origin", "origine inconnue")
        request = inputs.get("user_request", "Prépare un voyage complet")

        project_goal = (
            f"Demande utilisateur: {request}\n"
            f"Contraintes: destination={destination}, durée={duration} jours, "
            f"budget={budget}, départ={origin}."
        )
        return self.orchestrator.run_hierarchical(project_goal)


def build_best_practice_agents(mcp_tool: Optional[MCPFilesystemTool] = None) -> List[Agent]:
    """Définitions claires des rôles + délégation stratégique."""
    researcher_tools = [mcp_tool] if mcp_tool else []

    researcher = Agent(
        role=ROLE_RESEARCHER,
        goal="Conduire une recherche fiable et structurée",
        backstory="Analyste rigoureux, spécialiste benchmark et données factuelles.",
        allow_delegation=False,
        tools=researcher_tools,
        verbose=False,
    )

    writer = Agent(
        role=ROLE_WRITER,
        goal="Transformer la recherche en contenu clair et actionnable",
        backstory="Rédacteur technique orienté clarté et impact business.",
        allow_delegation=True,
        verbose=False,
    )

    editor = Agent(
        role=ROLE_EDITOR,
        goal="Améliorer lisibilité, cohérence, qualité finale",
        backstory="Éditeur senior focalisé qualité publication.",
        allow_delegation=False,
        verbose=False,
    )

    manager = Agent(
        role=ROLE_MANAGER,
        goal="Coordonner l'équipe, déléguer, arbitrer les priorités",
        backstory="Manager expérimenté en exécution multi-agents.",
        allow_delegation=True,
        verbose=False,
    )

    return [manager, researcher, writer, editor]


def create_collaboration_crew(root_dir: str) -> CollaborationCrewAdapter:
    """Factory prête pour Telegram: collaboration + MCP filesystem."""
    mcp_tool = MCPFilesystemTool(root_dir=root_dir)
    agents = build_best_practice_agents(mcp_tool=mcp_tool)
    orchestrator = CollaborationOrchestrator(
        agents=agents,
        process=Process.hierarchical,
        memory=True,
    )
    return CollaborationCrewAdapter(orchestrator)
