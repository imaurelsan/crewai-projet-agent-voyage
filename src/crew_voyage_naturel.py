#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CREW DE VOYAGE - VERSION PROMPT NATUREL
Comme le fait le prof: Un seul prompt en langage naturel
"""

import sys
import os
from dotenv import load_dotenv

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.crewai_simulator import CrewBase, Agent, Task, Crew, Process
from src.tools import all_tools
from langchain_groq import ChatGroq

load_dotenv()

# Configuration Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY non définie dans .env")

llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0.7)


class NaturalLanguageTravelCrew(CrewBase):
    """
    Crew qui accepte un prompt en langage naturel
    au lieu d'un formulaire structuré
    """
    
    def __init__(self):
        self.llm = llm
    
    @staticmethod
    def agent_extracteur() -> Agent:
        """
        AGENT SPÉCIAL: Extrait les informations du texte libre
        
        Rôle: Analyser le prompt utilisateur et extraire:
        - Destination
        - Dates / durée
        - Budget
        - Préférences (musées, gastronomie, etc.)
        """
        return Agent(
            role="Extracteur d'Informations",
            goal="Analyser le texte libre de l'utilisateur et extraire toutes les informations de voyage",
            backstory="""
            Vous êtes un expert en traitement du langage naturel spécialisé dans l'analyse 
            de demandes de voyage. Vous savez identifier les destinations, dates, budgets, 
            et préférences dans n'importe quelle formulation, même imprécise.
            """,
            verbose=True,
            llm=llm,
            tools=[]  # Pas d'outils, juste de l'analyse
        )
    
    @staticmethod
    def agent_chercheur() -> Agent:
        """Agent qui recherche les informations sur la destination"""
        return Agent(
            role="Chercheur de Destination",
            goal="Trouver les meilleures attractions et informations pratiques",
            backstory="""
            Vous êtes un expert en voyage avec 15 ans d'expérience. 
            Vous connaissez toutes les destinations et savez trouver les meilleures attractions.
            """,
            verbose=True,
            llm=llm,
            tools=[all_tools[1]]  # search_web
        )
    
    @staticmethod
    def agent_meteo() -> Agent:
        """Agent météo"""
        return Agent(
            role="Spécialiste Météo",
            goal="Analyser la météo et donner des recommandations",
            backstory="""
            Vous êtes un météorologue expert qui analyse les conditions 
            et donne des conseils vestimentaires pratiques.
            """,
            verbose=True,
            llm=llm,
            tools=[all_tools[0]]  # get_weather
        )
    
    @staticmethod
    def agent_planificateur() -> Agent:
        """Agent qui crée l'itinéraire complet"""
        return Agent(
            role="Planificateur de Voyage",
            goal="Créer un itinéraire jour par jour personnalisé",
            backstory="""
            Vous êtes un expert en planification de voyages. Vous créez des itinéraires 
            détaillés en tenant compte des préférences, du budget et de la météo.
            """,
            verbose=True,
            llm=llm,
            tools=[all_tools[3], all_tools[4], all_tools[5], all_tools[6], all_tools[7]]
            # search_hotels, search_transport, search_activities, search_restaurants, plan_itinerary
        )
    
    @staticmethod
    def agent_coordinateur() -> Agent:
        """Agent qui compile le guide final"""
        return Agent(
            role="Coordinateur de Voyage",
            goal="Créer un guide de voyage complet et bien formaté",
            backstory="""
            Vous êtes un expert en rédaction de guides de voyage. Vous savez compiler 
            toutes les informations en un document clair, structuré et actionable.
            """,
            verbose=True,
            llm=llm,
            tools=[]
        )
    
    @staticmethod
    def task_extraction(agent: Agent, user_prompt: str) -> Task:
        """
        TÂCHE 1: Extraire les informations du prompt naturel
        """
        return Task(
            description=f"""
            Analysez cette demande de voyage de l'utilisateur et extrayez toutes les informations pertinentes:
            
            "{user_prompt}"
            
            Identifiez et extrayez:
            1. Destination(s)
            2. Dates ou durée du voyage
            3. Ville de départ (si mentionnée)
            4. Budget (si mentionné, estimez sinon)
            5. Préférences (musées, gastronomie, nature, etc.)
            6. Nombre de personnes (si mentionné)
            7. Type de voyage (famille, solo, couple, amis)
            
            Si une information n'est pas mentionnée, faites une supposition raisonnable
            en vous basant sur le contexte.
            
            Formatez votre réponse ainsi:
            - Destination: ...
            - Durée: ... jours
            - Départ: ...
            - Budget: économique/moyen/luxe
            - Préférences: ...
            - Type: ...
            """,
            expected_output="Liste structurée des informations extraites du prompt utilisateur",
            agent=agent
        )
    
    @staticmethod
    def task_recherche(agent: Agent) -> Task:
        """TÂCHE 2: Rechercher les attractions"""
        return Task(
            description="""
            En vous basant sur les informations extraites, recherchez:
            - Les 5 meilleures attractions de la destination
            - Les quartiers recommandés
            - Les conseils pratiques
            
            Utilisez l'outil search_web pour trouver des informations actualisées.
            """,
            expected_output="Liste des top attractions avec descriptions et conseils",
            agent=agent,
            context=[]
        )
    
    @staticmethod
    def task_meteo(agent: Agent) -> Task:
        """TÂCHE 3: Analyser la météo"""
        return Task(
            description="""
            Analysez la météo actuelle de la destination et donnez:
            - Température et conditions
            - Vêtements à emporter
            - Meilleures heures pour sortir
            
            Utilisez l'outil get_weather.
            """,
            expected_output="Rapport météo avec recommandations vestimentaires",
            agent=agent,
            context=[]
        )
    
    @staticmethod
    def task_planification(agent: Agent) -> Task:
        """TÂCHE 4: Créer l'itinéraire complet"""
        return Task(
            description="""
            Créez un itinéraire complet jour par jour en tenant compte:
            - Des préférences mentionnées par l'utilisateur
            - Du budget
            - De la météo
            - De la durée
            
            Incluez:
            - Hébergements recommandés
            - Options de transport
            - Activités par jour
            - Restaurants suggérés
            
            Utilisez tous vos outils disponibles.
            """,
            expected_output="Itinéraire détaillé jour par jour avec hébergement, transport, activités et restaurants",
            agent=agent,
            context=[]
        )
    
    @staticmethod
    def task_coordination(agent: Agent, output_file: str = "guide_voyage_naturel.md") -> Task:
        """TÂCHE 5: Compiler le guide final"""
        return Task(
            description="""
            Compilez toutes les informations précédentes en un guide de voyage complet et bien structuré.
            
            Le guide doit inclure:
            1. Résumé du voyage (destination, dates, budget)
            2. Informations extraites de la demande
            3. Top attractions
            4. Météo et recommandations
            5. Itinéraire jour par jour détaillé
            6. Conseils pratiques
            
            Formatez en Markdown avec des emojis et une structure claire.
            """,
            expected_output="Guide de voyage complet en Markdown",
            agent=agent,
            output_file=output_file,
            context=[]
        )
    
    def crew(self, user_prompt: str) -> Crew:
        """
        Crée le crew avec prompt en langage naturel
        """
        # Créer les agents
        extracteur = self.agent_extracteur()
        chercheur = self.agent_chercheur()
        meteo = self.agent_meteo()
        planificateur = self.agent_planificateur()
        coordinateur = self.agent_coordinateur()
        
        # Créer les tâches
        task1 = self.task_extraction(extracteur, user_prompt)
        task2 = self.task_recherche(chercheur)
        task3 = self.task_meteo(meteo)
        task4 = self.task_planification(planificateur)
        task5 = self.task_coordination(coordinateur)
        
        # Lier le contexte (chaque tâche reçoit les résultats précédents)
        task2.context = [task1]
        task3.context = [task1]
        task4.context = [task1, task2, task3]
        task5.context = [task1, task2, task3, task4]
        
        return Crew(
            agents=[extracteur, chercheur, meteo, planificateur, coordinateur],
            tasks=[task1, task2, task3, task4, task5],
            verbose=True,
            process=Process.sequential
        )


if __name__ == "__main__":
    print("=" * 70)
    print("🌍 CREW DE VOYAGE - VERSION LANGAGE NATUREL")
    print("=" * 70)
    print("""
Ce crew fonctionne avec un prompt en langage naturel
(comme le fait votre prof).

Exemples de prompts:
- "Je vais à Paris demain pour 3 jours, budget 500€, j'aime les musées"
- "Voyage à Tokyo du 15 au 20 février, couple, on adore la gastronomie"
- "Week-end à Londres, on part de Bruxelles, budget moyen"
""")
    
    print("\n" + "=" * 70)
    user_prompt = input("📝 Décrivez votre voyage en une phrase: ").strip()
    
    if not user_prompt:
        print("\n⚠️  Pas de prompt fourni, utilisation d'un exemple:")
        user_prompt = "Je vais à Paris demain pour 3 jours, budget moyen, j'adore les musées et la gastronomie"
        print(f"📝 Prompt: {user_prompt}")
    
    print("\n🚀 Lancement du crew...\n")
    
    # Créer et lancer le crew
    travel_crew = NaturalLanguageTravelCrew()
    crew = travel_crew.crew(user_prompt)
    
    try:
        result = crew.kickoff()
        
        print("\n" + "=" * 70)
        print("✅ GUIDE DE VOYAGE GÉNÉRÉ!")
        print("=" * 70)
        print(f"📄 Fichier: guide_voyage_naturel.md")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
