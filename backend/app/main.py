from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.reasoning import analyze_environment

app = FastAPI(
    title="DarEco API",
    description="AI Biodiversity Intelligence System"
)


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dar-eco.vercel.app",
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Environment(BaseModel):
    soil_organic_carbon: float | None = None
    soil_ph: float | None = None
    rainfall: str | None = None
    land_use: str | None = None
    biodiversity: str | None = None
    region: str | None = None
    question: str | None = None
    conversation_history: list[dict] = []


@app.get("/")
def root():
    return {
        "message": "DarEco AI Biodiversity Intelligence API is running 🌿"
    }


@app.post("/analyze")
def analyze(environment: Environment):

    result = analyze_environment(
        environment.model_dump()
    )

    return result