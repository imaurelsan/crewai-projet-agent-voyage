#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crew de voyage utilisant l'architecture CrewAI
Compatible avec les exemples de cours
"""

import os
import sys
from typing import List

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.crewai_simulator import Agent, Crew, Task, Process, LLM, CrewBase, agent, crew, task
from langchain_core.tools import tool
import requests


# ============= OUTILS =============

@tool
def get_weather(city: str) -> str:
    """Récupère la météo actuelle pour une ville"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            temp_c = current['temp_C']
            feels_like = current['FeelsLikeC']
            weather_desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind_speed = current['windspeedKmph']
            
            return f"""Météo à {city}:
🌡️ {temp_c}°C (ressenti {feels_like}°C)
☁️ {weather_desc}
💧 Humidité: {humidity}%
💨 Vent: {wind_speed} km/h"""
        else:
            return f"Météo non disponible pour {city}"
    except Exception as e:
        return f"Erreur météo: {str(e)}"


# ============= CLASSE CREW =============

@CrewBase
class TravelCrew():
    """Crew de planification de voyage"""
    
    agents_config: dict
    tasks_config: dict
    
    def __init__(self):
        # Initialiser le LLM
        self.llm = LLM(model="llama3.2:3b", temperature=0.7)
    
    @agent
    def researcher(self) -> Agent:
        """Agent chercheur de destinations"""
        config = self.agents_config.get('researcher', {})
        return Agent(
            role=config.get('role', 'Researcher'),
            goal=config.get('goal', ''),
            backstory=config.get('backstory', ''),
            verbose=True,
            llm=self.llm
        )
    
    @agent
    def weather_specialist(self) -> Agent:
        """Agent spécialiste météo"""
        config = self.agents_config.get('weather_specialist', {})
        return Agent(
            role=config.get('role', 'Weather Specialist'),
            goal=config.get('goal', ''),
            backstory=config.get('backstory', ''),
            verbose=True,
            tools=[get_weather],
            llm=self.llm
        )
    
    @agent
    def gastronomy_expert(self) -> Agent:
        """Agent expert en gastronomie"""
        config = self.agents_config.get('gastronomy_expert', {})
        return Agent(
            role=config.get('role', 'Gastronomy Expert'),
            goal=config.get('goal', ''),
            backstory=config.get('backstory', ''),
            verbose=True,
            llm=self.llm
        )
    
    @agent
    def budget_planner(self) -> Agent:
        """Agent planificateur de budget"""
        config = self.agents_config.get('budget_planner', {})
        return Agent(
            role=config.get('role', 'Budget Planner'),
            goal=config.get('goal', ''),
            backstory=config.get('backstory', ''),
            verbose=True,
            llm=self.llm
        )
    
    @agent
    def coordinator(self) -> Agent:
        """Agent coordinateur"""
        config = self.agents_config.get('coordinator', {})
        return Agent(
            role=config.get('role', 'Travel Coordinator'),
            goal=config.get('goal', ''),
            backstory=config.get('backstory', ''),
            verbose=True,
            llm=self.llm
        )
    
    # ============= TASKS =============
    
    @task
    def research_task(self) -> Task:
        """Tâche de recherche"""
        config = self.tasks_config.get('research_task', {})
        return Task(
            description=config.get('description', ''),
            expected_output=config.get('expected_output', ''),
            agent=self.researcher()
        )
    
    @task
    def weather_task(self) -> Task:
        """Tâche météo"""
        config = self.tasks_config.get('weather_task', {})
        return Task(
            description=config.get('description', ''),
            expected_output=config.get('expected_output', ''),
            agent=self.weather_specialist()
        )
    
    @task
    def gastronomy_task(self) -> Task:
        """Tâche gastronomie"""
        config = self.tasks_config.get('gastronomy_task', {})
        return Task(
            description=config.get('description', ''),
            expected_output=config.get('expected_output', ''),
            agent=self.gastronomy_expert()
        )
    
    @task
    def budget_task(self) -> Task:
        """Tâche budget"""
        config = self.tasks_config.get('budget_task', {})
        return Task(
            description=config.get('description', ''),
            expected_output=config.get('expected_output', ''),
            agent=self.budget_planner()
        )
    
    @task
    def coordination_task(self) -> Task:
        """Tâche de coordination finale"""
        config = self.tasks_config.get('coordination_task', {})
        return Task(
            description=config.get('description', ''),
            expected_output=config.get('expected_output', ''),
            agent=self.coordinator(),
            output_file='voyage_plan.md'
        )
    
    # ============= CREW =============
    
    @crew
    def crew(self) -> Crew:
        """Crée l'équipe de voyage"""
        return Crew(
            agents=[
                self.researcher(),
                self.weather_specialist(),
                self.gastronomy_expert(),
                self.budget_planner(),
                self.coordinator()
            ],
            tasks=[
                self.research_task(),
                self.weather_task(),
                self.gastronomy_task(),
                self.budget_task(),
                self.coordination_task()
            ],
            process=Process.sequential,
            verbose=True
        )


# ============= MAIN =============

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌍 CREW DE PLANIFICATION DE VOYAGE")
    print("="*70 + "\n")
    
    # Demander la destination
    destination = input("Quelle destination voulez-vous explorer? (ou Entrée pour Tokyo): ").strip()
    if not destination:
        destination = "Tokyo"
    
    print(f"\n📍 Destination choisie: {destination}\n")
    
    # Créer et lancer le crew
    travel_crew = TravelCrew()
    result = travel_crew.crew().kickoff(inputs={'destination': destination})
    
    print("\n" + "="*70)
    print("📋 RÉSULTAT FINAL")
    print("="*70 + "\n")
    print(result)
    print(f"\n💾 Plan complet sauvegardé dans: voyage_plan.md\n")
