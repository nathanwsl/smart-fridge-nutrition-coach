"""
Routes de debug pour tester la Séquence 2 — TheMealDB + USDA.
"""
from fastapi import APIRouter
import httpx

from app.services import themealdb, usda, nutrition_pipeline
from app.schemas.recipe import RawMealDBRecipe

router = APIRouter(prefix="/recipes", tags=["Recettes (debug)"])


@router.get("/debug/search")
async def debug_search(ingredient: str):
    async with httpx.AsyncClient() as client:
        meals = await themealdb.search_recipes_by_ingredient(client, ingredient)
    return {"count": len(meals), "meals": meals}


@router.get("/debug/details/{meal_id}")
async def debug_details(meal_id: str):
    async with httpx.AsyncClient() as client:
        meal = await themealdb.get_recipe_details(client, meal_id)
    return meal


@router.get("/debug/flatten/{meal_id}")
async def debug_flatten(meal_id: str):
    """Teste le validateur Pydantic qui aplatit les ingrédients."""
    async with httpx.AsyncClient() as client:
        raw_meal = await themealdb.get_recipe_details(client, meal_id)

    if raw_meal is None:
        return {"error": "Recette introuvable"}

    parsed = RawMealDBRecipe(**raw_meal)
    return parsed


@router.get("/debug/usda/{query}")
async def debug_usda(query: str):
    async with httpx.AsyncClient() as client:
        food = await usda.search_food(client, query)

    if food is None:
        return {"error": "Aucun aliment brut trouvé"}

    nutrients = usda.extract_nutrients(food)
    return {
        "description": food.get("description"),
        "fdcId": food.get("fdcId"),
        "nutrients": nutrients,
    }


@router.get("/debug/pipeline/{meal_id}")
async def debug_pipeline(meal_id: str):
    """Teste le pipeline complet : recette -> ingrédients -> nutrition USDA."""
    async with httpx.AsyncClient() as client:
        result = await nutrition_pipeline.compute_recipe_nutrition(client, meal_id)
    return result