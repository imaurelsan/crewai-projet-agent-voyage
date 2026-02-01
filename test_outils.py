#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEST DES OUTILS - Permet de tester chaque outil individuellement

Ce fichier vous permet de comprendre comment fonctionne chaque outil
avant de les utiliser dans le crew complet.
"""

import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importer tous les outils
from src.tools import (
    get_weather,
    search_web,
    search_hotels,
    search_transport,
    search_activities,
    search_restaurants,
    plan_itinerary
)


def test_separator(title):
    """Affiche un séparateur visuel"""
    print("\n" + "="*70)
    print(f"🧪 TEST: {title}")
    print("="*70 + "\n")


def test_weather():
    """Test de l'outil météo"""
    test_separator("Outil Météo (get_weather)")
    
    # Tester avec Paris
    print("📍 Test avec Paris...")
    result = get_weather.invoke({"city": "Paris"})
    print(result)
    
    print("\n" + "-"*70)
    
    # Tester avec Tokyo
    print("\n📍 Test avec Tokyo...")
    result = get_weather.invoke({"city": "Tokyo"})
    print(result)


def test_search_web():
    """Test de l'outil de recherche web"""
    test_separator("Outil Recherche Web (search_web)")
    
    query = "meilleures attractions touristiques Paris"
    print(f"🔍 Recherche: '{query}'")
    result = search_web.invoke({"query": query})
    print(result)


def test_hotels():
    """Test de l'outil de recherche d'hôtels"""
    test_separator("Outil Recherche Hôtels (search_hotels)")
    
    # Test budget économique
    print("💰 Budget: économique")
    result = search_hotels.invoke({"city": "Paris", "budget": "économique"})
    print(result)
    
    print("\n" + "-"*70)
    
    # Test budget luxe
    print("\n💰 Budget: luxe")
    result = search_hotels.invoke({"city": "Tokyo", "budget": "luxe"})
    print(result)


def test_transport():
    """Test de l'outil de recherche de transport"""
    test_separator("Outil Recherche Transport (search_transport)")
    
    print("🚆 Recherche: Bruxelles → Paris (tous types)")
    result = search_transport.invoke({
        "origin": "Bruxelles",
        "destination": "Paris",
        "transport_type": "tous"
    })
    print(result)


def test_activities():
    """Test de l'outil de recherche d'activités"""
    test_separator("Outil Recherche Activités (search_activities)")
    
    # Test avec tous types
    print("🎭 Type: tous")
    result = search_activities.invoke({
        "city": "Paris",
        "activity_type": "tous"
    })
    print(result)
    
    print("\n" + "-"*70)
    
    # Test avec gastronomie
    print("\n🍽️ Type: gastronomie")
    result = search_activities.invoke({
        "city": "Tokyo",
        "activity_type": "gastronomie"
    })
    print(result)


def test_restaurants():
    """Test de l'outil de recherche de restaurants"""
    test_separator("Outil Recherche Restaurants (search_restaurants)")
    
    print("🍽️ Cuisine locale, budget moyen")
    result = search_restaurants.invoke({
        "city": "Paris",
        "cuisine_type": "locale",
        "budget": "moyen"
    })
    print(result)


def test_itinerary():
    """Test de l'outil de planification d'itinéraire"""
    test_separator("Outil Planification Itinéraire (plan_itinerary)")
    
    print("📅 Itinéraire pour 3 jours à Paris")
    result = plan_itinerary.invoke({
        "city": "Paris",
        "duration_days": 3,
        "interests": "culture"
    })
    print(result)


def menu():
    """Affiche le menu interactif"""
    print("\n" + "="*70)
    print("🧪 MENU DE TEST DES OUTILS")
    print("="*70)
    print("""
Choisissez un outil à tester:

1. 🌤️  Météo (get_weather)
2. 🔍 Recherche Web (search_web)
3. 🏨 Recherche Hôtels (search_hotels)
4. 🚆 Recherche Transport (search_transport)
5. 🎭 Recherche Activités (search_activities)
6. 🍽️  Recherche Restaurants (search_restaurants)
7. 📅 Planification Itinéraire (plan_itinerary)
8. 🎯 TESTER TOUS LES OUTILS
0. ❌ Quitter

""")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 TEST DES OUTILS DE VOYAGE")
    print("="*70)
    print("""
Ce programme vous permet de tester chaque outil individuellement
pour comprendre leur fonctionnement avant de les utiliser dans le crew.
""")
    
    while True:
        menu()
        
        choice = input("Votre choix (0-8): ").strip()
        
        if choice == "0":
            print("\n👋 Au revoir!\n")
            break
        elif choice == "1":
            test_weather()
        elif choice == "2":
            test_search_web()
        elif choice == "3":
            test_hotels()
        elif choice == "4":
            test_transport()
        elif choice == "5":
            test_activities()
        elif choice == "6":
            test_restaurants()
        elif choice == "7":
            test_itinerary()
        elif choice == "8":
            # Tester tous les outils
            print("\n🎯 EXÉCUTION DE TOUS LES TESTS...\n")
            test_weather()
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            test_search_web()
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            test_hotels()
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            test_transport()
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            test_activities()
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            test_restaurants()
            input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            test_itinerary()
            
            print("\n✅ Tous les tests terminés!")
        else:
            print("\n❌ Choix invalide. Veuillez choisir entre 0 et 8.")
        
        input("\n⏸️  Appuyez sur Entrée pour revenir au menu...")
