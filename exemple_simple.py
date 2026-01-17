#!/usr/bin/env python
"""Exemple simple pour tester Ollama avec LangChain"""

import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Charger les variables d'environnement
load_dotenv()

# Configuration
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Initialiser le LLM
llm = OllamaLLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.7
)

print(f"✅ Utilisation de Ollama - Modèle: {OLLAMA_MODEL}")
print(f"✅ Connexion: {OLLAMA_BASE_URL}\n")

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
