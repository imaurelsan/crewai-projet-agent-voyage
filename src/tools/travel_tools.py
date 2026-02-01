#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Outils pour les agents de voyage
Chaque outil est une fonction décorée avec @tool qui peut être utilisée par les agents
"""

import os
import requests
from typing import Optional
from langchain_core.tools import tool
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()


# ============================================================================
# 1. OUTIL MÉTÉO (déjà créé, mais on l'importe ici pour centraliser)
# ============================================================================

@tool
def get_weather(city: str) -> str:
    """
    Récupère la météo actuelle pour une ville donnée.
    
    Pourquoi cet outil ?
    - Aide à planifier les vêtements à emporter
    - Recommande les meilleures activités selon la météo
    
    Args:
        city: Le nom de la ville (ex: "Paris", "Tokyo", "New York")
    
    Returns:
        Un rapport météo avec température, conditions, humidité et vent
        
    Exemple:
        >>> get_weather("Paris")
        "Météo à Paris: 🌡️ 15°C (ressenti 13°C)..."
    """
    try:
        # API gratuite wttr.in - format JSON
        url = f"https://wttr.in/{city}?format=j1"
        
        # Faire la requête HTTP avec timeout de 15 secondes
        response = requests.get(url, timeout=15)
        
        # Vérifier que la requête a réussi (code 200 = OK)
        if response.status_code == 200:
            # Convertir la réponse en JSON (dictionnaire Python)
            data = response.json()
            
            # Extraire les données actuelles
            current = data['current_condition'][0]
            
            # Récupérer chaque information
            temp_c = current['temp_C']
            feels_like = current['FeelsLikeC']
            weather_desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind_speed = current['windspeedKmph']
            
            # Formater le résultat de manière lisible
            return f"""Météo à {city}:
🌡️ {temp_c}°C (ressenti {feels_like}°C)
☁️ {weather_desc}
💧 Humidité: {humidity}%
💨 Vent: {wind_speed} km/h"""
        else:
            return f"Météo non disponible pour {city}"
    except Exception as e:
        # En cas d'erreur, retourner un message informatif
        return f"Erreur lors de la récupération de la météo: {str(e)}"


# ============================================================================
# 2. OUTIL DE RECHERCHE WEB (Version gratuite - DuckDuckGo)
# ============================================================================

@tool
def search_web(query: str, num_results: int = 5) -> str:
    """
    Effectue une recherche web pour trouver des informations actuelles.
    
    Pourquoi cet outil ?
    - Trouve des informations à jour sur les destinations
    - Recherche des événements actuels
    - Découvre des nouveaux lieux
    
    Args:
        query: La requête de recherche (ex: "meilleures attractions Paris 2026")
        num_results: Nombre de résultats à retourner (par défaut: 5)
    
    Returns:
        Une liste de résultats avec titres et descriptions
        
    Note:
        Utilise DuckDuckGo (gratuit, pas de clé API nécessaire)
        Pour des résultats plus avancés, voir search_web_serpapi()
    """
    try:
        # On utilise l'API HTML de DuckDuckGo (gratuite)
        # Note: Pour un usage en production, préférer SerpAPI (payant mais fiable)
        
        # URL de l'API DuckDuckGo Instant Answer
        url = "https://api.duckduckgo.com/"
        
        # Paramètres de la requête
        params = {
            'q': query,              # La requête de recherche
            'format': 'json',        # Format de réponse en JSON
            'no_html': 1,            # Pas de HTML dans les résultats
            'skip_disambig': 1       # Éviter les pages de désambiguïsation
        }
        
        # Faire la requête
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Construire le résultat
            results = []
            
            # AbstractText = résumé principal
            if data.get('AbstractText'):
                results.append(f"📌 Résumé: {data['AbstractText']}")
            
            # RelatedTopics = sujets connexes
            for topic in data.get('RelatedTopics', [])[:num_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append(f"• {topic['Text']}")
            
            if results:
                return "\n\n".join(results)
            else:
                return f"Aucun résultat trouvé pour: {query}"
        else:
            return "Erreur lors de la recherche web"
            
    except Exception as e:
        return f"Erreur de recherche: {str(e)}"


# ============================================================================
# 3. OUTIL DE RECHERCHE WEB AVANCÉ (SerpAPI - PAYANT mais puissant)
# ============================================================================

@tool
def search_web_serpapi(query: str, num_results: int = 5) -> str:
    """
    Recherche web avancée avec SerpAPI (nécessite une clé API).
    
    Pourquoi SerpAPI ?
    - Résultats Google de qualité
    - Données structurées
    - Fiable et rapide
    - Support de Google Maps, Shopping, etc.
    
    Args:
        query: Requête de recherche
        num_results: Nombre de résultats
    
    Returns:
        Résultats de recherche formatés
        
    Configuration requise:
        - Créer un compte sur https://serpapi.com/ (100 recherches gratuites/mois)
        - Ajouter SERPAPI_API_KEY dans le fichier .env
        
    Exemple dans .env:
        SERPAPI_API_KEY=votre_clé_ici
    """
    # Récupérer la clé API depuis les variables d'environnement
    api_key = os.getenv('SERPAPI_API_KEY')
    
    # Vérifier que la clé existe
    if not api_key:
        return """❌ SERPAPI_API_KEY non configurée.
        
Pour utiliser cet outil:
1. Créer un compte sur https://serpapi.com/
2. Copier votre clé API
3. Ajouter dans .env: SERPAPI_API_KEY=votre_clé_ici"""
    
    try:
        # URL de l'API SerpAPI
        url = "https://serpapi.com/search"
        
        # Paramètres de la requête
        params = {
            'q': query,                    # Requête
            'api_key': api_key,           # Clé API
            'num': num_results,           # Nombre de résultats
            'engine': 'google',           # Moteur de recherche
            'hl': 'fr',                   # Langue française
            'gl': 'fr'                    # Géolocalisation France
        }
        
        # Faire la requête
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extraire les résultats organiques
            results = []
            for result in data.get('organic_results', []):
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                link = result.get('link', '')
                
                results.append(f"📌 {title}\n{snippet}\n🔗 {link}")
            
            if results:
                return "\n\n".join(results)
            else:
                return "Aucun résultat trouvé"
        else:
            return f"Erreur SerpAPI: {response.status_code}"
            
    except Exception as e:
        return f"Erreur: {str(e)}"


# ============================================================================
# 4. OUTIL DE RECHERCHE D'HÔTELS (Version simplifiée gratuite)
# ============================================================================

@tool
def search_hotels(city: str, budget: str = "moyen") -> str:
    """
    Recherche d'hôtels dans une ville avec estimation de prix.
    
    Pourquoi cet outil ?
    - Trouve des hébergements adaptés au budget
    - Compare les prix
    - Recommande les quartiers
    
    Args:
        city: Ville de destination
        budget: "économique", "moyen" ou "luxe"
    
    Returns:
        Recommandations d'hôtels avec fourchettes de prix
        
    Note:
        Version simplifiée avec estimations générales.
        Pour des prix réels en temps réel, utiliser l'API Booking.com ou Amadeus
    """
    # Mapping des budgets (prix moyens par nuit en EUR)
    budget_ranges = {
        'économique': (30, 60),
        'moyen': (60, 120),
        'luxe': (120, 300)
    }
    
    # Normaliser le budget
    budget = budget.lower()
    if budget not in budget_ranges:
        budget = 'moyen'
    
    min_price, max_price = budget_ranges[budget]
    
    # Recommandations générales (pour avoir des données réelles, il faudrait une API)
    return f"""🏨 Recommandations d'hébergement à {city} (Budget: {budget})

💰 Fourchette de prix: {min_price}€ - {max_price}€ par nuit

📍 Types d'hébergement recommandés:
{'• Auberges de jeunesse' if budget == 'économique' else ''}
{'• Hôtels 2-3 étoiles' if budget == 'économique' or budget == 'moyen' else ''}
{'• Hôtels 3-4 étoiles' if budget == 'moyen' else ''}
{'• Hôtels 4-5 étoiles' if budget == 'luxe' else ''}
{'• Hôtels boutique et resorts' if budget == 'luxe' else ''}

💡 Conseils:
- Réserver 2-3 mois à l'avance pour les meilleurs prix
- Comparer sur Booking.com, Hotels.com et Airbnb
- Vérifier les avis récents (TripAdvisor)
- Privilégier les quartiers centraux ou bien desservis par les transports

🔍 Pour des résultats en temps réel, utilisez search_web_serpapi() avec:
   "hotels {city} prix {budget}"
"""


# ============================================================================
# 5. OUTIL DE RECHERCHE DE TRANSPORTS (Trains, vols, etc.)
# ============================================================================

@tool
def search_transport(origin: str, destination: str, transport_type: str = "train") -> str:
    """
    Recherche d'options de transport entre deux villes.
    
    Pourquoi cet outil ?
    - Compare les moyens de transport
    - Estime les durées de trajet
    - Donne des fourchettes de prix
    
    Args:
        origin: Ville de départ
        destination: Ville d'arrivée
        transport_type: "train", "avion", "bus" ou "tous"
    
    Returns:
        Informations sur les options de transport disponibles
        
    Note:
        Version avec estimations générales.
        Pour des prix réels: API SNCF, Skyscanner, etc.
    """
    # Normaliser le type de transport
    transport_type = transport_type.lower()
    
    result = f"""🚆 Options de transport: {origin} → {destination}

"""
    
    # Recommandations selon le type
    if transport_type in ['train', 'tous']:
        result += """🚄 TRAIN
• Avantages: Confortable, écologique, centre-ville à centre-ville
• Réservation: SNCF, Trainline, Omio
• Conseil: Réserver à l'avance pour les meilleurs prix

"""
    
    if transport_type in ['avion', 'tous']:
        result += """✈️ AVION
• Avantages: Rapide pour longues distances
• Réservation: Skyscanner, Google Flights, Kayak
• Conseil: Comparer les aéroports secondaires

"""
    
    if transport_type in ['bus', 'tous']:
        result += """🚌 BUS
• Avantages: Économique
• Réservation: FlixBus, BlaBlaBus, Eurolines
• Conseil: Option la moins chère mais plus longue

"""
    
    result += f"""
💡 Pour trouver les meilleurs prix:
1. Utiliser search_web_serpapi("{origin} {destination} {transport_type} prix")
2. Comparer sur Google Flights / Trainline / Rome2Rio
3. Vérifier les offres promotionnelles
4. Être flexible sur les dates (+/- 3 jours)
"""
    
    return result


# ============================================================================
# 6. OUTIL DE RECHERCHE D'ACTIVITÉS TOURISTIQUES
# ============================================================================

@tool
def search_activities(city: str, activity_type: str = "tous") -> str:
    """
    Recherche d'activités et attractions touristiques dans une ville.
    
    Pourquoi cet outil ?
    - Découvre les activités locales
    - Filtre par type d'intérêt
    - Suggère des expériences uniques
    
    Args:
        city: Ville de destination
        activity_type: Type d'activité ("musées", "nature", "gastronomie", "sport", "tous")
    
    Returns:
        Liste d'activités recommandées
        
    Note:
        Pour des informations détaillées, combiner avec search_web()
    """
    # Normaliser le type
    activity_type = activity_type.lower()
    
    result = f"""🎭 Activités à {city}

"""
    
    # Catégories d'activités
    if activity_type in ['musées', 'culture', 'tous']:
        result += """🏛️ CULTURE & MUSÉES
• Visiter les musées principaux (billets coupe-file recommandés)
• Tours guidés du patrimoine historique
• Expositions temporaires

"""
    
    if activity_type in ['nature', 'plein air', 'tous']:
        result += """🌳 NATURE & PLEIN AIR
• Parcs et jardins publics
• Randonnées urbaines
• Pique-niques et espaces verts

"""
    
    if activity_type in ['gastronomie', 'food', 'tous']:
        result += """🍽️ GASTRONOMIE
• Food tours et dégustations
• Cours de cuisine locale
• Marchés alimentaires traditionnels

"""
    
    if activity_type in ['sport', 'aventure', 'tous']:
        result += """⚽ SPORT & AVENTURE
• Activités sportives (vélo, kayak, etc.)
• Événements sportifs locaux
• Expériences d'aventure

"""
    
    result += """
💡 Ressources recommandées:
• TripAdvisor: Avis et classements
• GetYourGuide: Réservation d'activités
• Airbnb Experiences: Expériences locales uniques

🔍 Pour plus de détails, utiliser:
   search_web_serpapi(f"meilleures activités {city} {activity_type}")
"""
    
    return result


# ============================================================================
# 7. OUTIL DE RECHERCHE DE RESTAURANTS AVANCÉ
# ============================================================================

@tool
def search_restaurants(city: str, cuisine_type: str = "locale", budget: str = "moyen") -> str:
    """
    Recherche de restaurants selon critères spécifiques.
    
    Pourquoi cet outil ?
    - Trouve les meilleurs restaurants
    - Filtre par type de cuisine et budget
    - Recommande des expériences culinaires
    
    Args:
        city: Ville de destination
        cuisine_type: Type de cuisine ("locale", "italienne", "asiatique", "végétarienne", etc.)
        budget: "économique", "moyen" ou "gastronomique"
    
    Returns:
        Recommandations de restaurants avec informations pratiques
    """
    # Fourchettes de prix
    budget_info = {
        'économique': '10-20€ par personne',
        'moyen': '20-40€ par personne',
        'gastronomique': '50€+ par personne'
    }
    
    budget = budget.lower()
    if budget not in budget_info:
        budget = 'moyen'
    
    result = f"""🍽️ Restaurants à {city}

📍 Type de cuisine: {cuisine_type}
💰 Budget: {budget_info[budget]}

🌟 RECOMMANDATIONS:

"""
    
    if cuisine_type.lower() == "locale":
        result += f"""🥘 CUISINE LOCALE
• Privilégier les restaurants fréquentés par les locaux
• Éviter les zones trop touristiques
• Demander les spécialités régionales

"""
    
    result += """💡 CONSEILS:
✓ Vérifier les avis récents sur Google Maps et TripAdvisor
✓ Réserver à l'avance pour les restaurants populaires
✓ Essayer les marchés locaux pour une expérience authentique
✓ Demander des recommandations à l'hôtel

📱 APPLICATIONS UTILES:
• TheFork / LaFourchette: Réservations et réductions
• Google Maps: Avis et horaires
• TripAdvisor: Classements et photos

🔍 Pour des recommandations précises:
   search_web_serpapi(f"meilleurs restaurants {cuisine_type} {city} {budget}")
"""
    
    return result


# ============================================================================
# 8. OUTIL DE PLANIFICATION D'ITINÉRAIRE
# ============================================================================

@tool
def plan_itinerary(city: str, duration_days: int, interests: str = "général") -> str:
    """
    Crée un itinéraire jour par jour pour une ville.
    
    Pourquoi cet outil ?
    - Optimise le temps de visite
    - Groupe les attractions par zone géographique
    - Propose un planning réaliste
    
    Args:
        city: Ville à visiter
        duration_days: Nombre de jours de séjour
        interests: Centres d'intérêt ("culture", "gastronomie", "nature", "général")
    
    Returns:
        Itinéraire suggéré jour par jour
    """
    result = f"""🗓️ ITINÉRAIRE POUR {city} ({duration_days} jour{'s' if duration_days > 1 else ''})

Centres d'intérêt: {interests}

"""
    
    # Suggestions par jour
    for day in range(1, duration_days + 1):
        result += f"""📅 JOUR {day}:
Matin (9h-12h):
• Visiter les attractions principales (moins de foule)
• Prendre un petit-déjeuner local

Midi (12h-14h):
• Déjeuner dans un restaurant recommandé
• Pause détente

Après-midi (14h-18h):
• Continuer les visites ou activités
• Shopping / découverte des quartiers

Soir (18h-22h):
• Dîner avec vue ou expérience culinaire
• Sortie culturelle (spectacle, concert) ou promenade

"""
    
    result += """
💡 CONSEILS DE PLANIFICATION:
✓ Grouper les attractions par zone pour optimiser les déplacements
✓ Prévoir des temps de repos (éviter la surcharge)
✓ Laisser de la flexibilité pour les découvertes spontanées
✓ Vérifier les jours de fermeture des musées
✓ Réserver les activités populaires à l'avance

🔍 Pour personnaliser davantage:
   - Utiliser search_activities() pour chaque jour
   - Consulter search_restaurants() pour les repas
   - Vérifier get_weather() pour adapter le programme
"""
    
    return result


# ============================================================================
# LISTE DE TOUS LES OUTILS (pour import facile)
# ============================================================================

# Cette liste permet d'importer tous les outils facilement dans crew_voyage.py
all_tools = [
    get_weather,
    search_web,
    search_web_serpapi,
    search_hotels,
    search_transport,
    search_activities,
    search_restaurants,
    plan_itinerary
]
