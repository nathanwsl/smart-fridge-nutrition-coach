from fastapi import APIRouter, Depends, HTTPException

from app.security.auth import get_current_user
from app.services.supabase_client import supabase
from app.schemas.fridge import IngredientCreate

router = APIRouter(prefix="/fridge", tags=["Frigo"])


@router.post("/ingredients")
def add_ingredient(payload: IngredientCreate, current_user: str = Depends(get_current_user)):
    supabase.table("fridge_items").insert({
        "username": current_user,
        "ingredient_name": payload.ingredient_name,
    }).execute()
    return {"message": f"{payload.ingredient_name} ajouté au frigo de {current_user}"}


@router.get("/ingredients")
def list_ingredients(current_user: str = Depends(get_current_user)):
    response = supabase.table("fridge_items").select("*").eq("username", current_user).execute()
    return response.data


@router.delete("/ingredients/{item_id}")
def delete_ingredient(item_id: int, current_user: str = Depends(get_current_user)):
    existing = (
        supabase.table("fridge_items")
        .select("*")
        .eq("id", item_id)
        .eq("username", current_user)
        .execute()
    )
    if not existing.data:
        raise HTTPException(status_code=404, detail="Ingrédient introuvable dans ton frigo")

    supabase.table("fridge_items").delete().eq("id", item_id).execute()
    return {"message": "Ingrédient supprimé"}