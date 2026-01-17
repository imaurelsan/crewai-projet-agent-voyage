from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from src.crew import TravelCrew
from src.config import APP_NAME, APP_VERSION

# Initialiser FastAPI
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="API pour la planification de voyages avec CrewAI"
)

# Modèles Pydantic
class VoyageRequest(BaseModel):
    destination: str = Field(..., description="Destination souhaitée")
    duree: int = Field(..., ge=1, le=30, description="Nombre de jours (1-30)")
    interets: str = Field(..., description="Centres d'intérêt (ex: culture, sport, nature)")
    niveau_confort: Optional[str] = Field(
        "moyen",
        description="Niveau de confort: budget, moyen, confort, ou luxe"
    )

class VoyageResponse(BaseModel):
    success: bool
    destination: str
    duree: int
    guide_voyage: str

# Routes
@app.get("/")
async def root():
    """Route racine"""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "planifier": "/api/v1/planifier-voyage"
        }
    }

@app.get("/health")
async def health():
    """Vérification de l'état de l'API"""
    return {"status": "healthy"}

@app.post("/api/v1/planifier-voyage", response_model=VoyageResponse)
async def planifier_voyage(request: VoyageRequest):
    """
    Planifie un voyage complet avec les agents CrewAI
    
    - **destination**: Ville ou pays de destination
    - **duree**: Nombre de jours du voyage
    - **interets**: Ce qui vous intéresse (culture, nature, sport, etc.)
    - **niveau_confort**: budget, moyen, confort ou luxe
    """
    try:
        # Valider le niveau de confort
        niveaux_valides = ["budget", "moyen", "confort", "luxe"]
        if request.niveau_confort not in niveaux_valides:
            raise HTTPException(
                status_code=400,
                detail=f"Niveau de confort invalide. Choisissez parmi: {', '.join(niveaux_valides)}"
            )
        
        # Créer le crew et planifier le voyage
        crew = TravelCrew()
        result = crew.planifier_voyage(
            destination=request.destination,
            duree=request.duree,
            interets=request.interets,
            niveau_confort=request.niveau_confort
        )
        
        return VoyageResponse(
            success=True,
            destination=request.destination,
            duree=request.duree,
            guide_voyage=str(result)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la planification: {str(e)}"
        )

@app.get("/api/v1/destinations-populaires")
async def destinations_populaires():
    """Liste des destinations populaires"""
    return {
        "destinations": [
            {"nom": "Paris, France", "region": "Europe", "type": "Culture & Gastronomie"},
            {"nom": "Tokyo, Japon", "region": "Asie", "type": "Culture & Technologie"},
            {"nom": "New York, USA", "region": "Amérique du Nord", "type": "Urbain & Culture"},
            {"nom": "Bali, Indonésie", "region": "Asie", "type": "Nature & Détente"},
            {"nom": "Rome, Italie", "region": "Europe", "type": "Histoire & Gastronomie"},
            {"nom": "Barcelone, Espagne", "region": "Europe", "type": "Culture & Plage"},
            {"nom": "Marrakech, Maroc", "region": "Afrique", "type": "Culture & Aventure"},
            {"nom": "Reykjavik, Islande", "region": "Europe", "type": "Nature & Aventure"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
