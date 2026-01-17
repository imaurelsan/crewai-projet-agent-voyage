from crewai import Task
from src.agents.travel_agents import (
    recherche_destination,
    planificateur_itineraire,
    expert_budget,
    expert_voyage
)

def task_recherche_destination(destination: str, interets: str, duree: int):
    """Tâche de recherche sur une destination"""
    return Task(
        description=f"""Recherchez des informations détaillées sur {destination} pour un voyage de {duree} jours.
        
        Concentrez-vous sur:
        1. Les attractions principales et activités liées à: {interets}
        2. La meilleure période pour visiter
        3. Les aspects culturels importants
        4. Les conseils pratiques (transport, sécurité, etc.)
        5. Les expériences uniques à ne pas manquer
        
        Fournissez une analyse complète et structurée.""",
        agent=recherche_destination,
        expected_output="Un rapport détaillé sur la destination avec toutes les informations essentielles"
    )

def task_planification_itineraire(destination: str, duree: int, interets: str):
    """Tâche de planification d'itinéraire"""
    return Task(
        description=f"""Créez un itinéraire détaillé jour par jour pour {destination} sur {duree} jours.
        
        L'itinéraire doit:
        1. Optimiser le temps et les déplacements
        2. Inclure les activités liées à: {interets}
        3. Équilibrer activités, repos et temps libre
        4. Prévoir les repas et hébergements
        5. Inclure des alternatives en cas de mauvais temps
        
        Utilisez les informations de la recherche de destination.""",
        agent=planificateur_itineraire,
        expected_output="Un itinéraire jour par jour détaillé et optimisé"
    )

def task_estimation_budget(destination: str, duree: int, niveau_confort: str):
    """Tâche d'estimation de budget"""
    return Task(
        description=f"""Estimez le budget total pour un voyage à {destination} de {duree} jours 
        avec un niveau de confort: {niveau_confort}.
        
        Incluez:
        1. Transport (aller-retour et sur place)
        2. Hébergement (basé sur le niveau de confort)
        3. Repas (petit-déjeuner, déjeuner, dîner)
        4. Activités et attractions
        5. Budget imprévu (10-15%)
        
        Fournissez un budget détaillé avec des fourchettes de prix.""",
        agent=expert_budget,
        expected_output="Un budget détaillé avec tous les postes de dépense et le total estimé"
    )

def task_recommandation_finale(destination: str, duree: int):
    """Tâche de synthèse et recommandation finale"""
    return Task(
        description=f"""Créez un guide de voyage complet pour {destination} ({duree} jours).
        
        Synthétisez toutes les informations:
        1. Résumé de la destination
        2. Itinéraire optimisé jour par jour
        3. Budget détaillé
        4. Conseils pratiques essentiels
        5. Recommandations personnalisées
        
        Le guide doit être clair, actionnable et inspirant.""",
        agent=expert_voyage,
        expected_output="Un guide de voyage complet et professionnel prêt à être utilisé"
    )
