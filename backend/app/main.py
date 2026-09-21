from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers import profile, recipes, auth, fridge
from app.security.auth import get_current_user

app = FastAPI(title="Smart Fridge & Nutrition Coach")

app.include_router(profile.router)
app.include_router(recipes.router)
app.include_router(auth.router)
app.include_router(fridge.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def serve_index():
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health_check():
    return {"status": "ok"}