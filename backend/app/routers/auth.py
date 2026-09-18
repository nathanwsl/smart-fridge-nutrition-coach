"""
Routes d'authentification — inscription et connexion (Supabase + JWT maison).
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.services.supabase_client import supabase
from app.security.auth import hash_password, verify_password, create_access_token

router = APIRouter(tags=["Authentification"])


@router.post("/signup")
def register_user(form_data: OAuth2PasswordRequestForm = Depends()):
    existing = supabase.table("users").select("*").eq("username", form_data.username).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur existe déjà")

    hashed = hash_password(form_data.password)
    supabase.table("users").insert({
        "username": form_data.username,
        "hashed_password": hashed,
    }).execute()

    return {"message": f"Utilisateur {form_data.username} créé avec succès"}


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    response = supabase.table("users").select("*").eq("username", form_data.username).execute()
    users = response.data

    if not users or not verify_password(form_data.password, users[0]["hashed_password"]):
        raise HTTPException(status_code=400, detail="Identifiants incorrects")

    token = create_access_token(form_data.username)
    return {"access_token": token, "token_type": "bearer"}