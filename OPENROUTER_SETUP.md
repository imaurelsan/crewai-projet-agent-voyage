# 🔑 Configuration OpenRouter (GRATUIT)

## Pourquoi OpenRouter ?
- ✅ **Crédits gratuits** pour tester (5$ offerts)
- ✅ Accès à **des dizaines de modèles** (Llama, Mistral, GPT, etc.)
- ✅ Pas de limite quotidienne stricte comme Groq
- ✅ **Mode gratuit** : modèles avec `:free` à la fin

## 📝 Étapes pour obtenir ta clé API

### 1. Créer un compte OpenRouter
👉 Va sur : **https://openrouter.ai/**
- Clique sur "Sign Up" (en haut à droite)
- Connecte-toi avec Google, GitHub ou email

### 2. Obtenir ta clé API
👉 Va sur : **https://openrouter.ai/keys**
- Clique sur "Create Key"
- Donne un nom (ex: "TelegramBot")
- Copie la clé (commence par `sk-or-v1-...`)

### 3. Configurer le bot

Ouvre le fichier `.env` et modifie ces lignes :

```env
# Change le provider
LLM_PROVIDER=openrouter

# Ajoute ta clé OpenRouter
OPENROUTER_API_KEY=sk-or-v1-...  # Colle ta clé ici

# Choisis un modèle GRATUIT
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

### 4. Redémarrer le bot

Le bot utilisera automatiquement OpenRouter au lieu de Groq !

## 🎯 Modèles gratuits recommandés

| Modèle | Description |
|--------|-------------|
| `meta-llama/llama-3.1-8b-instruct:free` | ⭐ Recommandé - Rapide et efficace |
| `mistralai/mistral-7b-instruct:free` | Alternative légère |
| `google/gemma-2-9b-it:free` | Bon pour les conversations |

## 💰 Crédits gratuits
OpenRouter offre **5$ gratuits** à l'inscription, ce qui permet environ :
- 10-20 guides de voyage complets
- Largement suffisant pour tester !

## ❓ Problèmes courants

**Erreur "Invalid API key"** :
- Vérifie que ta clé commence par `sk-or-v1-`
- Vérifie qu'il n'y a pas d'espaces avant/après dans `.env`

**Erreur "Model not found"** :
- Vérifie que le nom du modèle se termine par `:free`
- Voir la liste complète : https://openrouter.ai/models

## 🔄 Retour à Groq

Pour revenir à Groq, change juste dans `.env` :
```env
LLM_PROVIDER=groq
```
