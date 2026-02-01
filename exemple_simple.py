#!/usr/bin/env python
"""Exemple simple pour tester Groq avec LangChain (ultra-rapide et gratuit!)"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Charger les variables d'environnement
load_dotenv()

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY non défini!\n"
        "Obtenez une clé gratuite sur: https://console.groq.com\n"
        "Puis ajoutez dans .env: GROQ_API_KEY=gsk_..."
    )

# Initialiser le LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0.7
)

print(f"✅ Utilisation de Groq - Modèle: {GROQ_MODEL}")
print("✨ Groq est ultra-rapide et 100% gratuit!\n")

# Template pour l'agent de voyage
prompt_template = ChatPromptTemplate.from_template("""
Vous êtes un conseiller de voyage expert avec 15 ans d'expérience.
Vous êtes passionné par les voyages et adorez partager vos connaissances.

Destination: {destination}

Donnez 3 recommandations essentielles pour visiter {destination}:

1. **Attraction incontournable**: Une visite absolument essentielle
2. **Plat local à goûter**: Une spécialité culinaire à ne pas manquer
3. **Conseil pratique**: Un conseil utile pour les voyageurs

Soyez concis, enthousiaste et précis!
""")

# Créer la chaîne LangChain
chain = prompt_template | llm

def tester_agent(destination: str = "Paris"):
    """Tester l'agent de voyage avec une destination"""
    print(f"{'='*60}")
    print(f"🌍 AGENT DE VOYAGE - Destination: {destination}")
    print(f"{'='*60}\n")
    
    print("🚀 L'agent réfléchit...\n")
    
    # Invoquer la chaîne
    resultat = chain.invoke({"destination": destination})
    
    print(f"{'='*60}")
    print("✅ RECOMMANDATIONS")
    print(f"{'='*60}\n")
    print(resultat)
    print()
    
    return resultat

if __name__ == "__main__":
    print("\n🤖 Agent de Voyage Intelligent (Ollama + LangChain)\n")
    
    # Demander la destination
    destination = input("Quelle destination voulez-vous explorer? (ou Entrée pour Paris): ").strip()
    if not destination:
        destination = "Paris"
    
    tester_agent(destination)
