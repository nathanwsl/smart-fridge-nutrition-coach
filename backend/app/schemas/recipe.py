"""
Schémas Pydantic pour les recettes — Séquence 2.
"""
from pydantic import BaseModel, Field, model_validator


class IngredientQuantity(BaseModel):
    name: str
    measure: str


class RawMealDBRecipe(BaseModel):
    id_meal: str = Field(alias="idMeal")
    str_meal: str = Field(alias="strMeal")
    ingredients: list[IngredientQuantity] = []

    model_config = {"populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def flatten_ingredients(cls, data: dict) -> dict:
        ingredients = []
        for i in range(1, 21):
            name = data.get(f"strIngredient{i}")
            measure = data.get(f"strMeasure{i}")
            if name and name.strip():
                ingredients.append({"name": name.strip(), "measure": (measure or "").strip()})
        data["ingredients"] = ingredients
        return data