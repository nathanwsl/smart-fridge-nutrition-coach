
from app.schemas.profile import Sexe, NiveauActivite, Objectif

FACTEURS_ACTIVITE = {
    NiveauActivite.sedentaire: 1.2,
    NiveauActivite.leger: 1.375,
    NiveauActivite.modere: 1.55,
    NiveauActivite.actif: 1.725,
    NiveauActivite.extreme: 1.9,
}

AJUSTEMENT_OBJECTIF = {
    Objectif.perte: -500,
    Objectif.maintien: 0,
    Objectif.prise: 300,
}


def calculate_bmr(poids_kg: float, taille_cm: float, age: int, sexe: Sexe) -> float:
    """Calcule le métabolisme de base (Mifflin-St Jeor)."""
    base = 10 * poids_kg + 6.25 * taille_cm - 5 * age
    if sexe == Sexe.homme:
        return base + 5
    return base - 161


def calculate_tdee(bmr: float, niveau_activite: NiveauActivite) -> float:
    """Calcule la dépense énergétique totale journalière."""
    return bmr * FACTEURS_ACTIVITE[niveau_activite]


def calculate_target_calories(tdee: float, objectif: Objectif) -> float:
    """Ajuste le TDEE selon l'objectif (perte/maintien/prise)."""
    return tdee + AJUSTEMENT_OBJECTIF[objectif]


def calculate_macros(target_calories: float) -> dict:
    """
    Répartit les calories cibles en grammes de macronutriments.
    Répartition standard : 30% protéines, 40% glucides, 30% lipides.
    Rappel : 1g protéines = 4 kcal, 1g glucides = 4 kcal, 1g lipides = 9 kcal.
    """
    protein_kcal = target_calories * 0.30
    carbs_kcal = target_calories * 0.40
    fat_kcal = target_calories * 0.30

    return {
        "protein_g": round(protein_kcal / 4, 1),
        "carbs_g": round(carbs_kcal / 4, 1),
        "fat_g": round(fat_kcal / 9, 1),
    }