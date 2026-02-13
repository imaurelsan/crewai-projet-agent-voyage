# CrewAI Travel Planner (Telegram + CLI)

This project is a beginner-friendly, multi-agent travel planner. It includes:
- A CrewAI-like simulator compatible with Python 3.13
- Custom tools and shared memory
- A Telegram bot handler
- LLM support for Groq or OpenRouter

The goal is simple: send a natural language travel request and get a structured travel plan.

## What was built

- Multi-agent workflow (research, weather, hotels, transport, activities, synthesis)
- Custom tools via a minimal BaseTool pattern
- Shared in-memory context between tasks
- Telegram bot that accepts user messages and replies with a plan
- Input extraction (destination, origin, duration, budget, dates)

## Quick start

### 1) Create and activate venv

```powershell
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
pip install python-telegram-bot langchain-openai
```

### 3) Configure environment

Edit [.env](.env) and set:
- `LLM_PROVIDER` (groq or openrouter)
- LLM API key and model
- `TELEGRAM_BOT_TOKEN`

Setup guides:
- [GROQ_SETUP.md](GROQ_SETUP.md)
- [OPENROUTER_SETUP.md](OPENROUTER_SETUP.md)
- [QUICKSTART.md](QUICKSTART.md)

## Run

### Telegram bot

```powershell
.\venv\Scripts\python.exe src/crewai_simulator.py
```

Example message:
```
Je vais au Senegal le 28 fevrier, je reviens le 31 mars, budget 4000€, je pars de Paris.
```

### CLI (crew only)

```powershell
.\venv\Scripts\python.exe src/crew_voyage_complet.py
```

## Tests

```powershell
.\venv\Scripts\python.exe test_outils.py
.\venv\Scripts\python.exe test_groq_config.py
```

## Project structure (main files)

- [src/crewai_simulator.py](src/crewai_simulator.py): simulator, memory, telegram handler
- [src/crew_voyage_complet.py](src/crew_voyage_complet.py): full multi-agent crew
- [src/tools/travel_tools.py](src/tools/travel_tools.py): travel tools
- [config/agents.yaml](config/agents.yaml) and [config/tasks.yaml](config/tasks.yaml)

## Troubleshooting

- If you hit Groq rate limits, switch to OpenRouter in [.env](.env)
- If Telegram returns no reply, ensure only one bot instance is running
- If import errors appear, run from the repo root with the venv active

## Summary

This repo delivers a complete, working travel planning assistant with:
- Multi-agent workflow
- Tooling and shared memory
- Telegram interface
- LLM provider flexibility

It is ready for anyone to clone, configure, and run.
