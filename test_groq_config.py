#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEST RAPIDE - Vérifier que Groq est bien configuré
"""

import os
import sys
from dotenv import load_dotenv

print("=" * 70)
print("🧪 TEST DE CONFIGURATION GROQ")
print("=" * 70)

# 1. Vérifier que .env existe
print("\n1️⃣ Vérification du fichier .env...")
load_dotenv()

if not os.path.exists(".env"):
    print("❌ ERREUR: Fichier .env introuvable!")
    print("   Créez le fichier .env en copiant .env.example:")
    print("   > copy .env.example .env")
    sys.exit(1)
else:
    print("✅ Fichier .env trouvé")

# 2. Vérifier que GROQ_API_KEY est définie
print("\n2️⃣ Vérification de GROQ_API_KEY...")
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    print("❌ ERREUR: GROQ_API_KEY non définie dans .env!")
    print("   Obtenez une clé gratuite sur: https://console.groq.com")
    print("   Puis ajoutez dans .env: GROQ_API_KEY=gsk_...")
    sys.exit(1)
elif not groq_key.startswith("gsk_"):
    print(f"⚠️  ATTENTION: La clé ne commence pas par 'gsk_': {groq_key[:10]}...")
    print("   Vérifiez que c'est bien une clé Groq valide")
else:
    print(f"✅ GROQ_API_KEY trouvée: {groq_key[:15]}...")

# 3. Vérifier que langchain-groq est installé
print("\n3️⃣ Vérification de langchain-groq...")
try:
    from langchain_groq import ChatGroq
    print("✅ langchain-groq installé")
except ImportError:
    print("❌ ERREUR: langchain-groq non installé!")
    print("   Installez-le avec: pip install langchain-groq")
    sys.exit(1)

# 4. Test de connexion à Groq
print("\n4️⃣ Test de connexion à Groq...")
try:
    llm = ChatGroq(
        api_key=groq_key,
        model=os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
        temperature=0.7
    )
    print("✅ ChatGroq initialisé")
    
    # Test simple
    print("\n5️⃣ Test d'invocation (question simple)...")
    response = llm.invoke("Réponds juste 'Bonjour!' en français")
    print(f"✅ Réponse reçue: {response.content}")
    
except Exception as e:
    print(f"❌ ERREUR lors du test: {e}")
    print("\nVérifiez:")
    print("   - Que votre clé API est valide")
    print("   - Que vous avez une connexion internet")
    print("   - Que vous n'avez pas dépassé le quota gratuit")
    sys.exit(1)

# Résumé
print("\n" + "=" * 70)
print("✅ TOUS LES TESTS SONT RÉUSSIS!")
print("=" * 70)
print("\nVotre configuration Groq est parfaite! 🎉")
print("Vous pouvez maintenant exécuter:")
print("  - python exemple_simple.py")
print("  - python multi_agents.py")
print("  - python src/crew_voyage_complet.py")
print("\n" + "=" * 70)
