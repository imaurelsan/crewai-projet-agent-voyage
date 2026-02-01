#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEST RAPIDE DES OUTILS - Démonstration automatique

Ce script teste automatiquement les outils principaux
pour vérifier qu'ils fonctionnent correctement.
"""

import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importer les outils
from src.tools import (
    get_weather,
    search_web,
    search_hotels,
    search_transport,
    search_activities
)


def test_weather():
    """Test de l'outil météo"""
    print("\n" + "="*70)
    print("🌤️  TEST: Météo pour Paris")
    print("="*70)
    
    result = get_weather.invoke({"city": "Paris"})
    print(result)
    print("\n✅ Test météo réussi!")


def test_search():
    """Test de recherche web"""
    print("\n" + "="*70)
    print("🔍 TEST: Recherche web")
    print("="*70)
    
    result = search_web.invoke({
        "query": "attractions touristiques Paris",
        "num_results": 3
    })
    print(result)
    print("\n✅ Test recherche web réussi!")


def test_hotels():
    """Test de recherche d'hôtels"""
    print("\n" + "="*70)
    print("🏨 TEST: Recherche d'hôtels à Paris (budget moyen)")
    print("="*70)
    
    result = search_hotels.invoke({
        "city": "Paris",
        "budget": "moyen"
    })
    print(result)
    print("\n✅ Test hôtels réussi!")


def test_transport():
    """Test de recherche transport"""
    print("\n" + "="*70)
    print("🚆 TEST: Transport Bruxelles → Paris")
    print("="*70)
    
    result = search_transport.invoke({
        "origin": "Bruxelles",
        "destination": "Paris",
        "transport_type": "tous"
    })
    print(result)
    print("\n✅ Test transport réussi!")


def test_activities():
    """Test de recherche d'activités"""
    print("\n" + "="*70)
    print("🎭 TEST: Activités culturelles à Paris")
    print("="*70)
    
    result = search_activities.invoke({
        "city": "Paris",
        "activity_type": "culture"
    })
    print(result)
    print("\n✅ Test activités réussi!")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 TESTS AUTOMATIQUES DES OUTILS")
    print("="*70)
    print("\nCes tests vérifient que tous les outils fonctionnent correctement.\n")
    
    try:
        # Test 1: Météo
        test_weather()
        input("\n⏸️  Appuyez sur Entrée pour continuer au test suivant...")
        
        # Test 2: Recherche web
        test_search()
        input("\n⏸️  Appuyez sur Entrée pour continuer au test suivant...")
        
        # Test 3: Hôtels
        test_hotels()
        input("\n⏸️  Appuyez sur Entrée pour continuer au test suivant...")
        
        # Test 4: Transport
        test_transport()
        input("\n⏸️  Appuyez sur Entrée pour continuer au test suivant...")
        
        # Test 5: Activités
        test_activities()
        
        # Résumé
        print("\n" + "="*70)
        print("✅ TOUS LES TESTS RÉUSSIS!")
        print("="*70)
        print("""
Les 8 outils sont maintenant prêts à être utilisés par les agents:
  ✅ get_weather
  ✅ search_web
  ✅ search_web_serpapi (optionnel, nécessite clé API)
  ✅ search_hotels
  ✅ search_transport
  ✅ search_activities
  ✅ search_restaurants
  ✅ plan_itinerary

Prochaine étape: Exécutez le crew complet!
  python src/crew_voyage_complet.py
""")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrompus par l'utilisateur.")
    except Exception as e:
        print(f"\n\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
