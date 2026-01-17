#!/usr/bin/env python
"""Point d'entrée principal pour l'agent de voyage"""

from src.crew import TravelCrew
from src.config import APP_NAME, APP_VERSION

def main():
    """Fonction principale"""
    print(f"\n{'='*60}")
    print(f"{APP_NAME} v{APP_VERSION}")
    print(f"{'='*60}\n")
    
    # Exemple d'utilisation
    crew = TravelCrew()
    
    # Paramètres du voyage
    destination = "Paris, France"
    duree = 5
    interets = "culture, gastronomie, art"
    niveau_confort = "moyen"
    
    print(f"Planification d'un voyage à {destination}...")
    print(f"Durée: {duree} jours")
    print(f"Intérêts: {interets}")
    print(f"Niveau de confort: {niveau_confort}")
    print("\n" + "="*60 + "\n")
    
    # Lancer la planification
    result = crew.planifier_voyage(
        destination=destination,
        duree=duree,
        interets=interets,
        niveau_confort=niveau_confort
    )
    
    print("\n" + "="*60)
    print("RÉSULTAT FINAL")
    print("="*60 + "\n")
    print(result)

if __name__ == "__main__":
    main()
