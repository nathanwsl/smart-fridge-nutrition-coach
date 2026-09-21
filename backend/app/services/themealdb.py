
import httpx

from app.config import get_settings

settings = get_settings()


async def search_recipes_by_ingredient(client: httpx.AsyncClient, ingredient: str) -> list[dict]:
    """Cherche les recettes contenant l'ingrédient donné via filter.php."""
    url = f"{settings.themealdb_base_url}/filter.php"

    response = await client.get(url, params={"i": ingredient})
    response.raise_for_status()

    data = response.json()
    meals = data.get("meals")

    if meals is None:
        return []

    return meals


async def get_recipe_details(client: httpx.AsyncClient, meal_id: str) -> dict | None:
    """Récupère le détail complet d'une recette via lookup.php."""
    url = f"{settings.themealdb_base_url}/lookup.php"

    response = await client.get(url, params={"i": meal_id})
    response.raise_for_status()

    data = response.json()
    meals = data.get("meals")

    if meals is None:
        return None

    return meals[0]