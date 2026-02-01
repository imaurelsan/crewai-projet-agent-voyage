#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CREW DE VOYAGE COMPLET - Version avancée avec outils multiples

Ce fichier crée un crew de 6 agents spécialisés qui utilisent
différents outils pour créer un plan de voyage ultra-complet.

Chaque agent a un rôle spécifique et des outils dédiés.
"""

import os
import sys

# Ajouter le répertoire parent au path Python
# Cela permet d'importer les modules depuis src/
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.crewai_simulator import Agent, Crew, Task, Process, CrewBase, agent, crew, task, LLM

# Importer tous nos nouveaux outils
from src.tools import (
    get_weather,
    search_web,
    search_hotels,
    search_transport,
    search_activities,
    search_restaurants,
    plan_itinerary
)


# ============================================================================
# CLASSE DU CREW - Architecture @CrewBase comme dans les cours
# ============================================================================

@CrewBase
class CompleteTravelCrew():
    """
    Crew complet de planification de voyage avec 6 agents spécialisés.
    
    Agents:
        1. Destination Researcher (recherche générale)
        2. Weather Specialist (météo)
        3. Accommodation Expert (hébergement)
        4. Transport Coordinator (transports)
        5. Activity Planner (activités)
        6. Trip Coordinator (coordination finale)
    
    Chaque agent a des outils spécifiques pour accomplir sa mission.
    """
    
    # Configuration des agents et tâches (chargée depuis YAML)
    agents_config: dict
    tasks_config: dict
    
    def __init__(self):
        """Initialiser le crew avec le modèle LLM"""
        # Créer une instance du LLM (modèle de langage)
        self.llm = LLM(model="llama3.2:3b", temperature=0.7)
    
    
    # ========================================================================
    # AGENTS - Chaque agent est une fonction décorée par @agent
    # ========================================================================
    
    @agent
    def destination_researcher(self) -> Agent:
        """
        Agent 1: Chercheur de destination
        
        Rôle: Rechercher des informations générales sur la destination
        Outils: search_web (recherche web gratuite)
        """
        return Agent(
            role="Chercheur de Destination",
            goal="Trouver les meilleures informations sur la destination et ses attractions",
            backstory="""Vous êtes un expert en voyages avec 15 ans d'expérience.
            Vous excellez dans la recherche d'informations complètes et fiables sur n'importe quelle destination.
            Vous connaissez les meilleures sources d'information et savez distinguer les attractions touristiques
            des véritables joyaux cachés.""",
            verbose=True,
            tools=[search_web],  # ✨ Cet agent peut faire des recherches web
            llm=self.llm
        )
    
    @agent
    def weather_specialist(self) -> Agent:
        """
        Agent 2: Spécialiste météo
        
        Rôle: Analyser la météo et donner des recommandations
        Outils: get_weather (API météo gratuite)
        """
        return Agent(
            role="Spécialiste Météo",
            goal="Analyser la météo actuelle et donner des conseils pratiques pour le voyage",
            backstory="""Vous êtes un météorologue passionné avec 10 ans d'expérience.
            Vous aidez les voyageurs à préparer leur voyage en fonction du climat.
            Vous donnez des conseils sur les vêtements, les activités adaptées à la météo,
            et les meilleures périodes pour visiter.""",
            verbose=True,
            tools=[get_weather],  # ✨ Cet agent peut récupérer la météo
            llm=self.llm
        )
    
    @agent
    def accommodation_expert(self) -> Agent:
        """
        Agent 3: Expert en hébergement
        
        Rôle: Trouver les meilleurs hébergements selon le budget
        Outils: search_hotels (recherche d'hôtels)
        """
        return Agent(
            role="Expert en Hébergement",
            goal="Recommander les meilleurs hébergements adaptés au budget et aux préférences",
            backstory="""Vous êtes un expert en hôtellerie avec une connaissance approfondie
            des hébergements dans le monde entier. Vous savez trouver le meilleur rapport
            qualité-prix et connaissez les meilleurs quartiers où séjourner.
            Vous tenez compte du confort, de l'emplacement et du budget.""",
            verbose=True,
            tools=[search_hotels],  # ✨ Cet agent peut chercher des hôtels
            llm=self.llm
        )
    
    @agent
    def transport_coordinator(self) -> Agent:
        """
        Agent 4: Coordinateur de transport
        
        Rôle: Planifier tous les déplacements (trains, avions, transports locaux)
        Outils: search_transport (recherche de moyens de transport)
        """
        return Agent(
            role="Coordinateur de Transport",
            goal="Optimiser tous les déplacements et trouver les meilleures options de transport",
            backstory="""Vous êtes un expert en logistique de voyage avec une connaissance
            approfondie des systèmes de transport dans le monde entier. Vous savez comment
            optimiser les trajets, trouver les meilleurs prix et choisir le mode de transport
            le plus adapté selon la situation.""",
            verbose=True,
            tools=[search_transport],  # ✨ Cet agent peut chercher des transports
            llm=self.llm
        )
    
    @agent
    def activity_planner(self) -> Agent:
        """
        Agent 5: Planificateur d'activités
        
        Rôle: Trouver et organiser toutes les activités et visites
        Outils: search_activities, search_restaurants, plan_itinerary
        """
        return Agent(
            role="Planificateur d'Activités",
            goal="Créer un programme d'activités enrichissant et adapté aux intérêts du voyageur",
            backstory="""Vous êtes un organisateur de voyages créatif qui connaît
            toutes les meilleures activités, restaurants et expériences locales.
            Vous savez créer des itinéraires équilibrés qui mélangent culture,
            gastronomie et détente.""",
            verbose=True,
            tools=[
                search_activities,   # ✨ Recherche d'activités
                search_restaurants,  # ✨ Recherche de restaurants
                plan_itinerary      # ✨ Planification d'itinéraire
            ],
            llm=self.llm
        )
    
    @agent
    def trip_coordinator(self) -> Agent:
        """
        Agent 6: Coordinateur de voyage (final)
        
        Rôle: Synthétiser toutes les informations en un plan cohérent
        Outils: Aucun (utilise les résultats des autres agents)
        """
        return Agent(
            role="Coordinateur de Voyage",
            goal="Créer un plan de voyage complet et cohérent en synthétisant toutes les informations",
            backstory="""Vous êtes un coordinateur de voyage senior avec une expertise
            dans la création d'itinéraires parfaitement organisés. Vous excellez dans
            la synthèse d'informations complexes pour créer un plan de voyage clair,
            détaillé et facile à suivre.""",
            verbose=True,
            # Pas d'outils - cet agent coordonne les résultats des autres
            llm=self.llm
        )
    
    
    # ========================================================================
    # TÂCHES - Une tâche par agent
    # ========================================================================
    
    @task
    def research_destination_task(self) -> Task:
        """Tâche 1: Rechercher la destination"""
        return Task(
            description="""
            Rechercher des informations complètes sur {destination}.
            
            Utiliser l'outil search_web pour trouver:
            - Les attractions principales
            - L'histoire et la culture
            - Les quartiers intéressants
            - Les conseils pratiques
            - Ce qu'il faut absolument voir
            
            Fournir un résumé complet et engageant.
            """,
            expected_output="""
            Un rapport détaillé avec:
            - Top 5 des attractions incontournables
            - Aperçu culturel et historique
            - Quartiers recommandés
            - Conseils de voyage pratiques
            """,
            agent=self.destination_researcher()
        )
    
    @task
    def analyze_weather_task(self) -> Task:
        """Tâche 2: Analyser la météo"""
        return Task(
            description="""
            Analyser la météo actuelle à {destination}.
            
            Utiliser l'outil get_weather et fournir:
            - Conditions actuelles
            - Conseils vestimentaires
            - Activités recommandées selon la météo
            - Meilleures heures pour sortir
            """,
            expected_output="""
            Un rapport météo avec:
            - Température et conditions actuelles
            - Liste de vêtements à emporter
            - Recommandations d'activités adaptées
            """,
            agent=self.weather_specialist()
        )
    
    @task
    def find_accommodation_task(self) -> Task:
        """Tâche 3: Trouver un hébergement"""
        return Task(
            description="""
            Trouver les meilleurs hébergements à {destination} pour un budget {budget}.
            
            Utiliser l'outil search_hotels et recommander:
            - Types d'hébergement adaptés
            - Quartiers où séjourner
            - Fourchette de prix
            - Conseils de réservation
            """,
            expected_output="""
            Recommandations d'hébergement avec:
            - 3-5 options selon le budget
            - Quartiers recommandés
            - Estimation des prix
            - Conseils pratiques
            """,
            agent=self.accommodation_expert()
        )
    
    @task
    def plan_transport_task(self) -> Task:
        """Tâche 4: Planifier les transports"""
        return Task(
            description="""
            Planifier les transports pour se rendre à {destination} depuis {origin}.
            
            Utiliser l'outil search_transport et analyser:
            - Meilleures options (train, avion, bus)
            - Comparaison des prix et durées
            - Transports locaux sur place
            - Conseils de réservation
            """,
            expected_output="""
            Plan de transport avec:
            - Options pour aller à destination
            - Comparatif des moyens de transport
            - Infos sur les transports locaux
            - Conseils de réservation
            """,
            agent=self.transport_coordinator()
        )
    
    @task
    def create_activities_task(self) -> Task:
        """Tâche 5: Créer le programme d'activités"""
        return Task(
            description="""
            Créer un programme complet d'activités à {destination} pour {duration} jours.
            
            Utiliser les outils:
            - search_activities: pour trouver les activités
            - search_restaurants: pour les recommandations culinaires
            - plan_itinerary: pour créer un itinéraire jour par jour
            
            Créer un programme équilibré et enrichissant.
            """,
            expected_output="""
            Programme d'activités avec:
            - Itinéraire jour par jour
            - Activités recommandées chaque jour
            - Restaurants suggérés
            - Équilibre culture/détente/gastronomie
            """,
            agent=self.activity_planner()
        )
    
    @task
    def coordinate_trip_task(self) -> Task:
        """Tâche 6: Coordination finale du voyage"""
        return Task(
            description="""
            Synthétiser toutes les informations précédentes et créer un guide de voyage complet.
            
            Combiner les résultats de:
            - La recherche sur la destination
            - L'analyse météo
            - Les recommandations d'hébergement
            - Le plan de transport
            - Le programme d'activités
            
            Créer un document final clair, bien organisé et facile à suivre.
            """,
            expected_output="""
            Guide de voyage complet avec:
            1. Vue d'ensemble de la destination
            2. Informations météo et vêtements
            3. Hébergement recommandé
            4. Plan de transport
            5. Itinéraire jour par jour
            6. Checklist avant le départ
            7. Budget estimé total
            """,
            agent=self.trip_coordinator(),
            output_file='guide_voyage_complet.md'  # ✨ Sauvegarde automatique
        )
    
    
    # ========================================================================
    # CREW - Assembler tous les agents et tâches
    # ========================================================================
    
    @crew
    def crew(self) -> Crew:
        """
        Créer l'équipe complète avec tous les agents et tâches.
        
        Processus: Sequential (séquentiel)
        = Les tâches s'exécutent dans l'ordre, chaque agent recevant
          le contexte des agents précédents.
        """
        return Crew(
            # Liste de tous les agents (dans l'ordre d'exécution)
            agents=[
                self.destination_researcher(),
                self.weather_specialist(),
                self.accommodation_expert(),
                self.transport_coordinator(),
                self.activity_planner(),
                self.trip_coordinator()
            ],
            # Liste de toutes les tâches (dans l'ordre d'exécution)
            tasks=[
                self.research_destination_task(),
                self.analyze_weather_task(),
                self.find_accommodation_task(),
                self.plan_transport_task(),
                self.create_activities_task(),
                self.coordinate_trip_task()
            ],
            # Processus séquentiel: une tâche après l'autre
            process=Process.sequential,
            # Mode verbose: affiche tous les détails
            verbose=True
        )


# ============================================================================
# POINT D'ENTRÉE - Code exécuté quand on lance le fichier
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌍 CREW DE VOYAGE COMPLET - Version Avancée avec Outils")
    print("="*70 + "\n")
    
    print("Ce crew utilise 6 agents spécialisés et 8 outils différents")
    print("pour créer un plan de voyage ultra-complet.\n")
    
    # Demander les informations au utilisateur
    print("📝 Informations nécessaires:\n")
    
    destination = input("Destination (ex: Paris, Tokyo): ").strip() or "Paris"
    origin = input("Ville de départ (ex: Bruxelles): ").strip() or "Bruxelles"
    duration = input("Durée du séjour en jours (ex: 3): ").strip() or "3"
    budget = input("Budget (économique/moyen/luxe): ").strip().lower() or "moyen"
    
    print(f"\n📍 Récapitulatif:")
    print(f"   • Destination: {destination}")
    print(f"   • Départ: {origin}")
    print(f"   • Durée: {duration} jours")
    print(f"   • Budget: {budget}")
    print(f"\n🚀 Lancement du crew...\n")
    
    # Créer et lancer le crew
    travel_crew = CompleteTravelCrew()
    
    # Préparer les inputs (paramètres) pour le crew
    inputs = {
        'destination': destination,
        'origin': origin,
        'duration': duration,
        'budget': budget
    }
    
    # Lancer le crew avec kickoff()
    result = travel_crew.crew().kickoff(inputs=inputs)
    
    # Afficher le résultat final
    print("\n" + "="*70)
    print("✨ GUIDE DE VOYAGE FINAL")
    print("="*70 + "\n")
    print(result)
    print(f"\n💾 Guide complet sauvegardé dans: guide_voyage_complet.md\n")
