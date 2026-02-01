"""
Module d'outils pour les agents de voyage
Regroupe tous les outils disponibles pour enrichir les agents
"""

# Importer tous les outils depuis travel_tools.py
from .travel_tools import (
    get_weather,              # Météo actuelle
    search_web,               # Recherche web gratuite
    search_web_serpapi,       # Recherche web avancée (payant)
    search_hotels,            # Recherche d'hôtels
    search_transport,         # Recherche de transports
    search_activities,        # Recherche d'activités
    search_restaurants,       # Recherche de restaurants
    plan_itinerary,          # Planification d'itinéraire
    all_tools                 # Liste complète
)

# Liste des outils exportés (visible quand on fait "from src.tools import *")
__all__ = [
    'get_weather',
    'search_web',
    'search_web_serpapi',
    'search_hotels',
    'search_transport',
    'search_activities',
    'search_restaurants',
    'plan_itinerary',
    'all_tools'
]
