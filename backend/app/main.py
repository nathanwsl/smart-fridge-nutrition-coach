from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers import profile, recipes, auth
from app.security.auth import get_current_user

app = FastAPI(title="Smart Fridge & Nutrition Coach")

app.include_router(profile.router)
app.include_router(recipes.router)
app.include_router(auth.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def serve_index():
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/fridge/secure-status")
async def secure_fridge_status(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, tu es connecté"}