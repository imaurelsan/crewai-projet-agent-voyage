# 📦 Guide de Publication sur GitHub

Guide pas à pas pour publier ce projet sur GitHub.

## Prérequis

1. Compte GitHub créé sur https://github.com
2. Git installé sur votre machine
   - Windows: https://git-scm.com/download/win
   - Vérifier: `git --version`

## Étape 1 : Créer le repository sur GitHub

1. Aller sur https://github.com
2. Cliquer sur le bouton **"New"** (ou "+" → "New repository")
3. Remplir les informations :
   - **Repository name**: `crewai-projet-agent-voyage`
   - **Description**: "Système multi-agents de planification de voyage avec CrewAI, LangChain et Ollama"
   - **Visibilité**: Public ou Private (à votre choix)
   - ❌ **NE PAS** cocher "Initialize with README" (on a déjà le nôtre)
4. Cliquer sur **"Create repository"**

## Étape 2 : Initialiser Git localement

Ouvrez PowerShell dans le dossier du projet :

```powershell
# Se placer dans le dossier du projet
cd C:\Users\imaur\Desktop\crewai-projet-agent-voyage

# Initialiser Git
git init

# Vérifier que .gitignore existe
ls .gitignore
```

## Étape 3 : Faire le premier commit

```powershell
# Ajouter tous les fichiers
git add .

# Vérifier ce qui sera commité
git status

# Créer le premier commit
git commit -m "Initial commit: Projet CrewAI Agent de Voyage"
```

## Étape 4 : Connecter au repository GitHub

```powershell
# Remplacer <votre-username> par votre nom d'utilisateur GitHub
git remote add origin https://github.com/<votre-username>/crewai-projet-agent-voyage.git

# Vérifier que c'est bien configuré
git remote -v
```

## Étape 5 : Pousser le code

```powershell
# Renommer la branche en 'main' (standard GitHub)
git branch -M main

# Pousser le code
git push -u origin main
```

**Si demandé**, entrez vos identifiants GitHub.

## Étape 6 : Vérifier sur GitHub

1. Aller sur `https://github.com/<votre-username>/crewai-projet-agent-voyage`
2. Vous devriez voir tous vos fichiers
3. Le README.md s'affiche automatiquement en page d'accueil

## 🎨 Personnaliser le repository

### Ajouter un badge de statut

Dans le README.md, les badges sont déjà configurés :
```markdown
![Python Version](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)
```

### Ajouter des topics

Sur GitHub :
1. Cliquer sur l'icône ⚙️ à côté de "About"
2. Ajouter des topics : `python`, `ai`, `langchain`, `ollama`, `crewai`, `agents`

### Activer les Issues

1. Aller dans **Settings** → **Features**
2. Cocher **Issues**
3. Les utilisateurs pourront signaler des bugs ou poser des questions

## 🔄 Workflow de développement

### Faire des modifications

```powershell
# 1. Modifier vos fichiers
# (éditez src/crew_voyage.py par exemple)

# 2. Voir ce qui a changé
git status

# 3. Ajouter les changements
git add .

# 4. Commiter avec un message descriptif
git commit -m "Ajout d'un agent transport"

# 5. Pousser vers GitHub
git push
```

### Messages de commit recommandés

- ✅ `"Ajout agent météo avec API wttr.in"`
- ✅ `"Fix: Correction timeout API météo"`
- ✅ `"Docs: Mise à jour du guide développement"`
- ✅ `"Refactor: Simplification du code crew"`
- ❌ `"update"` (trop vague)
- ❌ `"fix bug"` (pas assez précis)

## 🌿 Utiliser des branches

Pour les fonctionnalités importantes :

```powershell
# Créer une nouvelle branche
git checkout -b feature/agent-transport

# Faire vos modifications
# ...

# Commiter
git add .
git commit -m "Ajout agent transport avec calcul d'itinéraire"

# Pousser la branche
git push -u origin feature/agent-transport
```

Puis sur GitHub :
1. Créer une **Pull Request**
2. Vérifier les changements
3. Merger dans `main`

## 📋 Checklist avant publication

- [ ] `.gitignore` présent (ne pas commiter `venv/`, `.env`)
- [ ] `README.md` complet et à jour
- [ ] `GUIDE_DEVELOPPEMENT.md` pour les débutants
- [ ] `requirements.txt` à jour
- [ ] `LICENSE` présent (MIT recommandé)
- [ ] Fichiers de configuration (`.env.example` au lieu de `.env`)
- [ ] Code commenté et propre
- [ ] Tests fonctionnels effectués

## 🔒 Sécurité

### Ne JAMAIS commiter

- ❌ Le fichier `.env` (contient des secrets)
- ❌ Le dossier `venv/` (trop gros, spécifique à votre machine)
- ❌ Les clés API privées
- ❌ Les mots de passe

### Créer un .env.example

```powershell
# Copier .env en .env.example
Copy-Item .env .env.example

# Éditer .env.example et remplacer les valeurs par des exemples
# OLLAMA_MODEL=llama3.2:3b
# OLLAMA_BASE_URL=http://localhost:11434
```

## 📊 Ajouter un README badge personnalisé

```markdown
![Made with](https://img.shields.io/badge/Made%20with-LangChain-blue)
![Powered by](https://img.shields.io/badge/Powered%20by-Ollama-green)
![Stars](https://img.shields.io/github/stars/<username>/crewai-projet-agent-voyage)
![Forks](https://img.shields.io/github/forks/<username>/crewai-projet-agent-voyage)
```

## 🤝 Inviter des collaborateurs

1. Aller dans **Settings** → **Collaborators**
2. Cliquer sur **Add people**
3. Entrer le nom d'utilisateur GitHub
4. Ils pourront push directement

## 📝 Gérer les Issues

Quand quelqu'un ouvre une issue :

1. **Lire attentivement** le problème
2. **Reproduire** le bug si possible
3. **Répondre** rapidement (même "je regarde")
4. **Labelliser** : `bug`, `enhancement`, `question`
5. **Fermer** quand résolu avec un commit de référence

## 🎉 Promouvoir votre projet

1. **Twitter/X** : Partager avec hashtags `#Python #AI #LangChain`
2. **Reddit** : r/Python, r/MachineLearning
3. **LinkedIn** : Partager en expliquant ce que vous avez appris
4. **Dev.to** : Écrire un article de blog

## 📈 Suivre les statistiques

GitHub fournit :
- **Insights** → **Traffic** : Nombre de visiteurs
- **Insights** → **Community** : Contributeurs
- **Insights** → **Pulse** : Activité récente

---

**🎊 Félicitations !** Votre projet est maintenant sur GitHub et prêt à être partagé avec le monde ! 🚀
