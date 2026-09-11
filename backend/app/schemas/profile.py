from enum import Enum
from pydantic import BaseModel, Field

class Sexe(str, Enum):
    homme = "homme"
    femme = "femme"

class NiveauActivite(str, Enum):
    sedentaire = "sédentaire"
    leger = "léger"
    modere = "modéré"
    actif = "actif"
    extreme = "extrême"

class Objectif(str, Enum):
    perte = "perte"
    maintien = "maintien"
    prise = "prise"


class ProfileCreate(BaseModel):
    sexe: Sexe
    poids_kg: float = Field(..., gt=0, le=300, description="Poids en kilogrammes")
    taille_cm: float = Field(..., gt=0, le=250, description="Taille en centimètres")
    age: int = Field(..., ge=1, le=120)
    niveau_activite: NiveauActivite
    objectif: Objectif


class ProfileResult(BaseModel):
    bmr: float
    tdee: float
    target_calories: float
    protein_g: float
    carbs_g: float
    fat_g: float