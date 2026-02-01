import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'application
APP_NAME = "Agent de Voyage CrewAI"
APP_VERSION = "1.0.0"

# Configuration du LLM - Groq (100% gratuit et ultra-rapide)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

# Configuration Groq (GRATUIT - RECOMMANDÉ)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

# Configuration OpenAI (payant - optionnel)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4")

# Vérifier la configuration selon le provider
if LLM_PROVIDER == "groq" and not GROQ_API_KEY:
    raise ValueError(
        "LLM_PROVIDER est 'groq' mais GROQ_API_KEY n'est pas défini.\n"
        "Obtenez une clé gratuite sur https://console.groq.com\n"
        "Puis ajoutez-la dans votre fichier .env: GROQ_API_KEY=gsk_..."
    )
elif LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError(
        "LLM_PROVIDER est 'openai' mais OPENAI_API_KEY n'est pas défini."
    )
