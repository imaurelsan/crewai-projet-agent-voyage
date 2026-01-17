from crewai import Crew, Process
from src.tasks.travel_tasks import (
    task_recherche_destination,
    task_planification_itineraire,
    task_estimation_budget,
    task_recommandation_finale
)
from src.agents.travel_agents import (
    recherche_destination,
    planificateur_itineraire,
    expert_budget,
    expert_voyage
)

class TravelCrew:
    """Crew pour la planification de voyages"""
    
    def __init__(self):
        self.agents = [
            recherche_destination,
            planificateur_itineraire,
            expert_budget,
            expert_voyage
        ]
    
    def planifier_voyage(
        self,
        destination: str,
        duree: int,
        interets: str,
        niveau_confort: str = "moyen"
    ):
        """
        Planifie un voyage complet
        
        Args:
            destination: La destination souhaitée
            duree: Nombre de jours du voyage
            interets: Centres d'intérêt du voyageur
            niveau_confort: budget/moyen/confort/luxe
        
        Returns:
            Le guide de voyage complet
        """
        # Créer les tâches
        tasks = [
            task_recherche_destination(destination, interets, duree),
            task_planification_itineraire(destination, duree, interets),
            task_estimation_budget(destination, duree, niveau_confort),
            task_recommandation_finale(destination, duree)
        ]
        
        # Créer le crew
        crew = Crew(
            agents=self.agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=2
        )
        
        # Exécuter le crew
        result = crew.kickoff()
        
        return result
