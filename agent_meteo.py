#!/usr/bin/env python
"""Agent Weather Specialist avec outils pour récupérer la météo réelle"""

import os
import requests
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

load_dotenv()

# Configuration
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Initialiser le LLM
llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0.7)

print(f"✅ Weather Specialist Agent - Modèle: {OLLAMA_MODEL}\n")

# ============= OUTILS MÉTÉO =============

@tool
def get_weather(city: str) -> str:
    """
    Récupère la météo actuelle pour une ville.
    
    Args:
        city: Le nom de la ville (ex: Paris, Tokyo, New York)
    
    Returns:
        Les informations météo actuelles
    """
    try:
        # Utiliser wttr.in - API météo gratuite
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
            
            result = f"""Météo actuelle à {city}:
🌡️ Température: {temp_c}°C (ressenti {feels_like}°C)
☁️ Conditions: {weather_desc}
💧 Humidité: {humidity}%
💨 Vent: {wind_speed} km/h"""
            
            return result
        else:
            return f"❌ Impossible de récupérer la météo pour {city}"
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

@tool
def compare_weather(city1: str, city2: str) -> str:
    """
    Compare la météo actuelle entre deux villes.
    
    Args:
        city1: Première ville
        city2: Deuxième ville
    
    Returns:
        Comparaison des conditions météo
    """
    try:
        # Récupérer la météo des deux villes
        url1 = f"https://wttr.in/{city1}?format=j1"
        url2 = f"https://wttr.in/{city2}?format=j1"
        
        response1 = requests.get(url1, timeout=15)
        response2 = requests.get(url2, timeout=15)
        
        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()['current_condition'][0]
            data2 = response2.json()['current_condition'][0]
            
            temp1 = int(data1['temp_C'])
            temp2 = int(data2['temp_C'])
            
            result = f"""Comparaison météo entre {city1} et {city2}:

📍 {city1}:
   🌡️ {temp1}°C ({data1['weatherDesc'][0]['value']})
   💧 Humidité: {data1['humidity']}%
   💨 Vent: {data1['windspeedKmph']} km/h

📍 {city2}:
   🌡️ {temp2}°C ({data2['weatherDesc'][0]['value']})
   💧 Humidité: {data2['humidity']}%
   💨 Vent: {data2['windspeedKmph']} km/h

📊 Différence de température: {abs(temp1 - temp2)}°C
{'🔥 ' + city1 + ' est plus chaud' if temp1 > temp2 else '❄️ ' + city2 + ' est plus chaud' if temp2 > temp1 else '⚖️ Température identique'}"""
            
            return result
        else:
            return f"❌ Impossible de comparer les météos"
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

# Liste des outils disponibles
tools = [get_weather, compare_weather]

# ============= AGENT MÉTÉO =============

# Note: LangChain avec Ollama ne supporte pas encore nativement le function calling
# On va donc créer un système simple où l'agent décide quelle fonction appeler

def weather_agent(question: str):
    """
    Agent météo qui peut utiliser des outils
    """
    print(f"{'='*70}")
    print(f"☁️ WEATHER SPECIALIST AGENT")
    print(f"{'='*70}\n")
    print(f"❓ Question: {question}\n")
    
    # Analyser la question pour déterminer quelle fonction utiliser
    question_lower = question.lower()
    
    # Détecter si c'est une comparaison
    if any(word in question_lower for word in ['compare', 'comparer', 'différence', 'vs', 'versus', 'entre']):
        print("🔍 Détection: Comparaison de météo demandée\n")
        
        # Extraire les villes (simple parsing)
        words = question.replace(',', ' ').replace('et', ' ').split()
        cities = []
        for i, word in enumerate(words):
            if word.lower() in ['entre', 'et', 'vs', 'versus', 'compare', 'comparer']:
                continue
            if len(word) > 2 and word[0].isupper():
                cities.append(word)
        
        if len(cities) >= 2:
            print(f"🌍 Villes détectées: {cities[0]} et {cities[1]}\n")
            print("🤖 L'agent appelle l'outil compare_weather...\n")
            result = compare_weather.invoke({"city1": cities[0], "city2": cities[1]})
            
            print(f"{'='*70}")
            print("✅ RÉSULTAT")
            print(f"{'='*70}\n")
            print(result)
            
            # Demander à l'agent d'interpréter
            print(f"\n{'='*70}")
            print("🤖 ANALYSE DE L'AGENT")
            print(f"{'='*70}\n")
            
            analysis_prompt = f"""Basé sur ces données météo:

{result}

Donne une recommandation de voyage: quelle ville est plus agréable à visiter en ce moment et pourquoi? 
Sois concis et pratique."""
            
            analysis = llm.invoke(analysis_prompt)
            print(analysis)
            
        else:
            print("❌ Impossible de détecter deux villes pour la comparaison")
    
    # Sinon, c'est une requête simple de météo
    else:
        print("🔍 Détection: Requête météo simple\n")
        
        # Extraire la ville - chercher les mots-clés
        question_clean = question.replace('?', '').replace(',', '')
        words = question_clean.split()
        
        # Liste de mots à ignorer
        skip_words = ['quel', 'quelle', 'temps', 'fait', 'il', 'la', 'le', 'météo', 'à', 'dans', 'de', 'du']
        
        city = None
        for word in words:
            if len(word) > 2 and word[0].isupper() and word.lower() not in skip_words:
                city = word
                break
        
        if city:
            print(f"🌍 Ville détectée: {city}\n")
            print("🤖 L'agent appelle l'outil get_weather...\n")
            result = get_weather.invoke({"city": city})
            
            print(f"{'='*70}")
            print("✅ RÉSULTAT")
            print(f"{'='*70}\n")
            print(result)
            
            # Demander à l'agent de donner des conseils
            print(f"\n{'='*70}")
            print("🤖 CONSEILS DE L'AGENT")
            print(f"{'='*70}\n")
            
            advice_prompt = f"""Basé sur cette météo:

{result}

Donne 2-3 conseils pratiques pour un voyageur visitant cette ville aujourd'hui.
Sois concis et utile."""
            
            advice = llm.invoke(advice_prompt)
            print(advice)
        else:
            print("❌ Impossible de détecter une ville dans la question")

if __name__ == "__main__":
    print("☁️ WEATHER SPECIALIST AGENT\n")
    print("Cet agent peut:")
    print("  1️⃣  Récupérer la météo actuelle d'une ville")
    print("  2️⃣  Comparer la météo entre deux villes\n")
    
    print("Exemples de questions:")
    print('  - "Quel temps fait-il à Paris ?"')
    print('  - "Compare la météo entre Tokyo et Paris"')
    print('  - "Quelle est la différence de température entre Londres et Madrid ?"\n')
    
    question = input("Votre question (ou Entrée pour tester): ").strip()
    
    if not question:
        # Test par défaut
        print("\n🧪 Test 1: Météo simple\n")
        weather_agent("Quel temps fait-il à Paris ?")
        
        print("\n" + "="*70)
        print("\n🧪 Test 2: Comparaison\n")
        weather_agent("Compare la météo entre Tokyo et Paris")
    else:
        weather_agent(question)
