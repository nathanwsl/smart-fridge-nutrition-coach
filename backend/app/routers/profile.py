from fastapi import APIRouter

from app.schemas.profile import ProfileCreate, ProfileResult
from app.services import nutrition_engine

router = APIRouter(prefix="/profile", tags=["Profil"])


@router.post("/calculate", response_model=ProfileResult)
async def calculate_profile(profile: ProfileCreate):
    bmr = nutrition_engine.calculate_bmr(
        poids_kg=profile.poids_kg,
        taille_cm=profile.taille_cm,
        age=profile.age,
        sexe=profile.sexe,
    )

    tdee = nutrition_engine.calculate_tdee(
        bmr=bmr,
        niveau_activite=profile.niveau_activite,
    )

    target_calories = nutrition_engine.calculate_target_calories(
        tdee=tdee,
        objectif=profile.objectif,
    )

    macros = nutrition_engine.calculate_macros(target_calories)

    return ProfileResult(
        bmr=round(bmr, 1),
        tdee=round(tdee, 1),
        target_calories=round(target_calories, 1),
        protein_g=macros["protein_g"],
        carbs_g=macros["carbs_g"],
        fat_g=macros["fat_g"],
    )