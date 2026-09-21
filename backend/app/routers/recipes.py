import asyncio

from fastapi import APIRouter, Depends, HTTPException
import httpx

from app.services import themealdb, usda, nutrition_pipeline
from app.schemas.recipe import RawMealDBRecipe
from app.security.auth import get_current_user
from app.services.supabase_client import supabase

router = APIRouter(prefix="/recipes", tags=["Recettes"])


@router.get("/suggestions")
async def get_suggestions(current_user: str = Depends(get_current_user), limit: int = 3):
    """
    Suggestions de recettes basées sur le frigo de l'utilisateur connecté.
    Croise TheMealDB (recherche) et USDA (nutrition) via le pipeline async.
    """
    fridge_response = (
        supabase.table("fridge_items").select("*").eq("username", current_user).execute()
    )
    fridge_ingredients = [item["ingredient_name"] for item in fridge_response.data]

    if not fridge_ingredients:
        raise HTTPException(status_code=400, detail="Ton frigo est vide, ajoute des ingrédients d'abord")

    timeout = httpx.Timeout(10.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        recipes = await nutrition_pipeline.find_recipes_for_fridge(client, fridge_ingredients)
        top_recipes = recipes[:limit]

        results = await asyncio.gather(*[
            nutrition_pipeline.compute_recipe_nutrition(client, r["idMeal"])
            for r in top_recipes
        ])

    valid_results = [r for r in results if "error" not in r]

    return {"fridge_ingredients": fridge_ingredients, "suggestions": valid_results}

    return {"fridge_ingredients": fridge_ingredients, "suggestions": results}


@router.get("/debug/search", tags=["Recettes (debug)"])
async def debug_search(ingredient: str):
    async with httpx.AsyncClient() as client:
        meals = await themealdb.search_recipes_by_ingredient(client, ingredient)
    return {"count": len(meals), "meals": meals}


@router.get("/debug/details/{meal_id}", tags=["Recettes (debug)"])
async def debug_details(meal_id: str):
    async with httpx.AsyncClient() as client:
        meal = await themealdb.get_recipe_details(client, meal_id)
    return meal


@router.get("/debug/flatten/{meal_id}", tags=["Recettes (debug)"])
async def debug_flatten(meal_id: str):
    async with httpx.AsyncClient() as client:
        raw_meal = await themealdb.get_recipe_details(client, meal_id)

    if raw_meal is None:
        return {"error": "Recette introuvable"}

    return RawMealDBRecipe(**raw_meal)


@router.get("/debug/usda/{query}", tags=["Recettes (debug)"])
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


@router.get("/debug/pipeline/{meal_id}", tags=["Recettes (debug)"])
async def debug_pipeline(meal_id: str):
    async with httpx.AsyncClient() as client:
        result = await nutrition_pipeline.compute_recipe_nutrition(client, meal_id)
    return result