import httpx

from app.config import get_settings

settings = get_settings()

NUTRIENT_IDS = {
    "energy_kcal": 1008,
    "protein_g": 1003,
    "carbs_g": 1005,
    "fat_g": 1004,
}


async def search_food(client: httpx.AsyncClient, query: str) -> dict | None:
    """Cherche un aliment brut dans l'USDA (filtré SR Legacy / Foundation)."""
    url = f"{settings.usda_base_url}/foods/search"
    body = {
        "query": query,
        "dataType": ["SR Legacy", "Foundation"],
        "pageSize": 5,
    }

    response = await client.post(
        url,
        json=body,
        params={"api_key": settings.usda_api_key},
    )
    response.raise_for_status()

    data = response.json()

    if data.get("totalHits", 0) == 0:
        return None

    return _pick_best_match(query, data["foods"])


def _pick_best_match(query: str, foods: list[dict]) -> dict | None:
    query_words = set(query.lower().split())

    def score(food: dict) -> int:
        description_words = set(food.get("description", "").lower().replace(",", " ").split())
        return len(query_words & description_words)

    best = max(foods, key=score)
    if score(best) == 0:
        return None

    return best


def extract_nutrients(food: dict) -> dict:
    """Extrait calories/protéines/glucides/lipides depuis la réponse USDA brute."""
    result = {key: 0.0 for key in NUTRIENT_IDS}

    for nutrient in food.get("foodNutrients", []):
        nutrient_id = nutrient.get("nutrientId")
        value = nutrient.get("value", 0.0)

        for key, target_id in NUTRIENT_IDS.items():
            if nutrient_id == target_id:
                result[key] = value

    return result