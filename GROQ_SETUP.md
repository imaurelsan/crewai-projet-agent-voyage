# 🚀 Configuration de Groq (100% Gratuit & Ultra-rapide)

## ⚡ Pourquoi Groq?

Nous avons remplacé **Ollama** par **Groq** pour ces raisons:

- ✅ **100% Gratuit** - Quota généreux sans carte bancaire
- ✅ **10x plus rapide** qu'Ollama en local
- ✅ **Pas d'installation** - Fonctionne dans le cloud
- ✅ **Modèles puissants** - Llama 3.1 70B, Mixtral 8x7B
- ✅ **Excellent support LangChain** - Intégration native

## 📝 Étapes pour obtenir votre clé gratuite

### 1. Créer un compte Groq

1. Allez sur [console.groq.com](https://console.groq.com)
2. Cliquez sur **"Sign Up"** (en haut à droite)
3. Inscrivez-vous avec:
   - Votre email
   - Votre compte Google
   - Votre compte GitHub

> 💡 **Aucune carte bancaire requise!**

### 2. Créer votre clé API

Une fois connecté:

1. Dans le menu de gauche, cliquez sur **"API Keys"**
2. Cliquez sur **"Create API Key"**
3. Donnez un nom à votre clé (ex: "Travel Agent Project")
4. Cliquez sur **"Create"**
5. **COPIEZ IMMÉDIATEMENT** votre clé (elle commence par `gsk_`)

⚠️ **IMPORTANT**: La clé ne sera montrée qu'une seule fois!

### 3. Configurer votre projet

1. Ouvrez le fichier `.env` dans votre projet
2. Si le fichier n'existe pas, copiez `.env.example` vers `.env`:
   ```bash
   copy .env.example .env
   ```

3. Ajoutez votre clé Groq:
   ```env
   GROQ_API_KEY=gsk_votre_clé_ici
   GROQ_MODEL=llama-3.1-70b-versatile
   LLM_PROVIDER=groq
   ```

### 4. Tester votre configuration

Exécutez ce test rapide:

```bash
python -c "import os; from dotenv import load_dotenv; from langchain_groq import ChatGroq; load_dotenv(); llm = ChatGroq(api_key=os.getenv('GROQ_API_KEY'), model='llama-3.1-70b-versatile'); print(llm.invoke('Dis bonjour!').content)"
```

Si vous voyez un message de salutation, **c'est bon!** ✅

## 🎯 Modèles disponibles (tous gratuits)

| Modèle | Description | Vitesse | Usage recommandé |
|--------|-------------|---------|------------------|
| `llama-3.1-70b-versatile` | **Le plus puissant** | Rapide | **RECOMMANDÉ** - Meilleur équilibre |
| `llama-3.1-8b-instant` | Le plus rapide | Ultra-rapide | Prototypage rapide |
| `mixtral-8x7b-32768` | Contexte étendu | Rapide | Longs documents |
| `gemma2-9b-it` | Bon équilibre | Très rapide | Usage général |

## 🔧 Utilisation dans votre code

```python
from langchain_groq import ChatGroq
import os

# Initialiser Groq
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-70b-versatile",
    temperature=0.7
)

# Utiliser
response = llm.invoke("Quelle est la capitale de la France?")
print(response.content)
```

## 📊 Limites gratuites

Groq offre un quota généreux:

- **Requêtes par minute**: 30
- **Requêtes par jour**: 14,400
- **Tokens par minute**: 1,000,000

C'est **largement suffisant** pour le développement et même la production!

## ❓ FAQ

### Dois-je payer après un certain temps?

Non! Groq est **100% gratuit** avec des limites généreuses.

### Que faire si j'atteins la limite?

Les limites se réinitialisent chaque minute. Si vous avez besoin de plus, vous pouvez:
1. Attendre 1 minute
2. Créer plusieurs clés API
3. Optimiser vos requêtes

### Groq vs Ollama?

| Aspect | Groq | Ollama |
|--------|------|--------|
| Vitesse | ⚡⚡⚡⚡⚡ (ultra-rapide) | ⚡⚡ (lent) |
| Installation | ☁️ Cloud (rien à installer) | 💾 Local (2GB+) |
| Ressources | 0% de votre CPU/RAM | 50-100% CPU |
| Coût | Gratuit | Gratuit |
| Modèles | Très puissants | Limités par votre PC |

### Mes données sont-elles sécurisées?

Oui! Groq respecte la confidentialité:
- ✅ Pas de stockage des requêtes
- ✅ Chiffrement HTTPS
- ✅ Conforme RGPD

## 🆘 Problèmes courants

### Erreur: "Invalid API Key"

```python
# Vérifiez que votre clé est bien définie
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("GROQ_API_KEY"))  # Doit afficher gsk_...
```

### Erreur: "Rate limit exceeded"

Vous avez dépassé le quota. Attendez 1 minute ou réduisez la fréquence des requêtes.

### Erreur: "GROQ_API_KEY non défini"

Le fichier `.env` n'est pas chargé ou la clé n'est pas dedans:

```bash
# Vérifiez que .env existe
dir .env

# Vérifiez le contenu
type .env
```

## 🎉 C'est tout!

Vous êtes maintenant configuré avec **Groq** - le provider LLM **le plus rapide et gratuit** du marché!

Bon développement! 🚀
