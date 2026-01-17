#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test interactif de l'agent météo"""

import sys
sys.path.insert(0, '.')

from agent_meteo import weather_agent

if __name__ == "__main__":
    print("=" * 70)
    print("☁️  TEST AGENT MÉTÉO - MODE INTERACTIF")
    print("=" * 70)
    print()
    print("Test 1: Météo simple à Paris")
    print("-" * 70)
    weather_agent("Quel temps fait-il à Paris ?")
    
    print("\n\n")
    print("=" * 70)
    print("Test 2: Météo à Cotonou (Bénin)")
    print("-" * 70)
    weather_agent("Quel temps fait-il à Cotonou ?")
    
    print("\n\n")
    print("=" * 70)
    print("Test 3: Comparaison Paris vs Tokyo")
    print("-" * 70)
    weather_agent("Compare la météo entre Paris et Tokyo")
