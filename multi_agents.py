#!/usr/bin/env python
"""Exemple avec PLUSIEURS agents travaillant en équipe (avec Groq ultra-rapide!)"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY non défini! Obtenez une clé gratuite sur https://console.groq.com"
    )

# Initialiser le LLM
llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0.7)

print(f"✅ Système multi-agents - Modèle: {GROQ_MODEL}")
print("⚡ Vitesse Groq: 10x plus rapide qu'Ollama!\n")

# ============= AGENT 1: Expert en Destinations =============
agent_destinations = ChatPromptTemplate.from_template("""
Vous êtes un EXPERT EN DESTINATIONS avec 20 ans d'expérience.
Vous connaissez les meilleures attractions et activités.

Destination: {destination}
Intérêts: {interets}

Listez 3 attractions/activités principales qui correspondent à ces intérêts.
Soyez précis et donnez des noms exacts.
""")

# ============= AGENT 2: Expert Gastronomie =============
agent_gastronomie = ChatPromptTemplate.from_template("""
Vous êtes un EXPERT EN GASTRONOMIE locale.
Vous connaissez tous les plats traditionnels du monde.

Destination: {destination}

Recommandez 2 plats/spécialités locales INCONTOURNABLES.
Expliquez pourquoi ils sont spéciaux et où les trouver.
""")

# ============= AGENT 3: Expert Budget =============
agent_budget = ChatPromptTemplate.from_template("""
Vous êtes un EXPERT EN BUDGET DE VOYAGE.
Vous savez estimer les coûts dans toutes les destinations.

Destination: {destination}
Durée: {duree} jours

Estimez le budget total moyen par personne incluant:
- Hébergement
- Repas
- Activités
- Transport local

Donnez une fourchette (budget économique et confortable).
""")

# ============= AGENT 4: Coordinateur =============
agent_coordinateur = ChatPromptTemplate.from_template("""
Vous êtes le COORDINATEUR DE VOYAGE.
Vous synthétisez les informations de l'équipe.

Destination: {destination}
Durée: {duree} jours

Informations des experts:

ATTRACTIONS ET ACTIVITÉS:
{info_destinations}

GASTRONOMIE:
{info_gastronomie}

BUDGET:
{info_budget}

Créez un RÉSUMÉ FINAL structuré et enthousiaste incluant:
1. Vue d'ensemble de la destination
2. Les incontournables
3. Expériences culinaires
4. Budget estimé
5. Un conseil final pour profiter au maximum

Soyez concis mais inspirant!
""")

# Créer les chaînes
chain_destinations = agent_destinations | llm
chain_gastronomie = agent_gastronomie | llm
chain_budget = agent_budget | llm
chain_coordinateur = agent_coordinateur | llm

def planifier_voyage_multi_agents(destination: str, duree: int = 5, interets: str = "culture, gastronomie"):
    """
    Utilise 4 AGENTS travaillant en équipe pour planifier un voyage
    
    Agent 1: Expert Destinations
    Agent 2: Expert Gastronomie  
    Agent 3: Expert Budget
    Agent 4: Coordinateur (synthèse)
    """
    print(f"{'='*70}")
    print(f"🌍 PLANIFICATION MULTI-AGENTS - {destination}")
    print(f"{'='*70}\n")
    
    # AGENT 1: Destinations
    print("🤖 Agent 1 (Expert Destinations) travaille...\n")
    info_destinations = chain_destinations.invoke({
        "destination": destination,
        "interets": interets
    })
    print(f"✅ Agent 1 terminé\n")
    
    # AGENT 2: Gastronomie
    print("🤖 Agent 2 (Expert Gastronomie) travaille...\n")
    info_gastronomie = chain_gastronomie.invoke({
        "destination": destination
    })
    print(f"✅ Agent 2 terminé\n")
    
    # AGENT 3: Budget
    print("🤖 Agent 3 (Expert Budget) travaille...\n")
    info_budget = chain_budget.invoke({
        "destination": destination,
        "duree": duree
    })
    print(f"✅ Agent 3 terminé\n")
    
    # AGENT 4: Coordinateur (synthèse)
    print("🤖 Agent 4 (Coordinateur) synthétise les informations...\n")
    resultat_final = chain_coordinateur.invoke({
        "destination": destination,
        "duree": duree,
        "info_destinations": info_destinations,
        "info_gastronomie": info_gastronomie,
        "info_budget": info_budget
    })
    
    print(f"\n{'='*70}")
    print("✅ PLAN DE VOYAGE COMPLET")
    print(f"{'='*70}\n")
    print(resultat_final)
    print()
    
    return resultat_final

if __name__ == "__main__":
    print("🤖 SYSTÈME MULTI-AGENTS DE VOYAGE\n")
    print("4 agents travaillent en équipe pour votre voyage:\n")
    print("  1️⃣  Expert Destinations")
    print("  2️⃣  Expert Gastronomie")
    print("  3️⃣  Expert Budget")
    print("  4️⃣  Coordinateur\n")
    
    # Paramètres
    destination = input("Destination? (ou Entrée pour Marrakech): ").strip() or "Marrakech"
    duree_str = input("Durée en jours? (ou Entrée pour 5): ").strip()
    duree = int(duree_str) if duree_str.isdigit() else 5
    interets = input("Vos intérêts? (ou Entrée pour 'culture, gastronomie'): ").strip() or "culture, gastronomie"
    
    print()
    planifier_voyage_multi_agents(destination, duree, interets)
