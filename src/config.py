import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de l'application
APP_NAME = "Agent de Voyage CrewAI"
APP_VERSION = "1.0.0"

# Configuration du LLM
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()

# Configuration Ollama (gratuit)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Configuration OpenAI (payant)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4")

# Vérifier la configuration selon le provider
if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError(
        "LLM_PROVIDER est 'openai' mais OPENAI_API_KEY n'est pas défini. "
        "Modifiez LLM_PROVIDER='ollama' dans .env pour utiliser Ollama gratuitement."
    )
