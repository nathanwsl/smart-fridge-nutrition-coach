
import asyncio

import httpx

from app.services import themealdb, usda
from app.services.ingredient_mapping import normalize_ingredient_name
from app.schemas.recipe import RawMealDBRecipe


async def find_recipes_for_fridge(client: httpx.AsyncClient, fridge_ingredients: list[str]) -> list[dict]:
    """
    Cherche des recettes pour CHAQUE ingrédient du frigo, en parallèle.
    Renvoie une liste dédupliquée de recettes (par idMeal).
    """
    tasks = [
        themealdb.search_recipes_by_ingredient(client, ingredient)
        for ingredient in fridge_ingredients
    ]
    results = await asyncio.gather(*tasks)

    seen_ids = set()
    unique_recipes = []
    for meals in results:
        for meal in meals:
            if meal["idMeal"] not in seen_ids:
                seen_ids.add(meal["idMeal"])
                unique_recipes.append(meal)

    return unique_recipes

async def compute_recipe_nutrition(client: httpx.AsyncClient, meal_id: str) -> dict:
    """
    Récupère une recette, aplatit ses ingrédients, puis interroge l'USDA
    pour CHAQUE ingrédient en parallèle, et additionne calories/macros.
    """
    raw_meal = await themealdb.get_recipe_details(client, meal_id)
    if raw_meal is None:
        return {"error": "Recette introuvable"}

    recipe = RawMealDBRecipe(**raw_meal)

    tasks = [
        usda.search_food(client, normalize_ingredient_name(ing.name))
        for ing in recipe.ingredients
    ]
    usda_results = await asyncio.gather(*tasks)

    total = {"energy_kcal": 0.0, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 0.0}
    matched_ingredients = []
    unmatched_ingredients = []

    for ingredient, food in zip(recipe.ingredients, usda_results):
        if food is None:
            unmatched_ingredients.append(ingredient.name)
            continue

        nutrients = usda.extract_nutrients(food)
        for key in total:
            total[key] += nutrients[key]

        matched_ingredients.append({
            "name": ingredient.name,
            "measure": ingredient.measure,
            "usda_match": food.get("description"),
        })

    return {
        "id_meal": recipe.id_meal,
        "str_meal": recipe.str_meal,
        "total_nutrients_per_100g_sum": total,
        "matched_ingredients": matched_ingredients,
        "unmatched_ingredients": unmatched_ingredients,
    }

