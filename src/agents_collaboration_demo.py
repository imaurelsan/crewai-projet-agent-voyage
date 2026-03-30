"""Démo exécutable: orchestration collaboration + MCP filesystem."""

from pathlib import Path

from src.agents_collaboration import (
    AskQuestionTool,
    CollaborationOrchestrator,
    DelegateWorkTool,
    MCPFilesystemTool,
    ROLE_MANAGER,
    ROLE_RESEARCHER,
    build_best_practice_agents,
)
from src.crewai_simulator import Process


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent

    mcp_fs = MCPFilesystemTool(root_dir=str(repo_root))
    agents = build_best_practice_agents(mcp_tool=mcp_fs)
    orchestrator = CollaborationOrchestrator(
        agents=agents,
        process=Process.hierarchical,
        memory=True,
    )

    delegate_tool = DelegateWorkTool(orchestrator, owner_role=ROLE_MANAGER)
    ask_tool = AskQuestionTool(orchestrator, owner_role=ROLE_MANAGER)

    mcp_files = mcp_fs.invoke({"action": "list_directory", "path": "config"})
    delegated = delegate_tool.invoke(
        {
            "task": "Analyse les fichiers de config et résume les points clés agents/tasks.",
            "coworker_role": ROLE_RESEARCHER,
            "context": mcp_files,
        }
    )
    expert_q = ask_tool.invoke(
        {
            "question": "Quels risques de collaboration vois-tu dans cette configuration ?",
            "coworker_role": ROLE_RESEARCHER,
            "context": delegated,
        }
    )

    print("\n=== Delegate Work Tool ===\n")
    print(delegated)
    print("\n=== Ask Question Tool ===\n")
    print(expert_q)

    print("\n=== Pattern 1: Research-Write-Edit ===\n")
    print(orchestrator.run_research_write_edit("Agents Collaboration best practices 2026"))

    print("\n=== Pattern 2: Collaborative Single Task ===\n")
    print(
        orchestrator.run_collaborative_single_task(
            "Créer une stratégie go-to-market pour un assistant voyage IA B2C"
        )
    )

    print("\n=== Pattern 3: Hierarchical Collaboration ===\n")
    print(
        orchestrator.run_hierarchical(
            "Livrer un plan d'exécution de 90 jours pour scaler un produit d'agents IA"
        )
    )


if __name__ == "__main__":
    main()
