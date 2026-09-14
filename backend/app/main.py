from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers import profile

app = FastAPI(title="Smart Fridge & Nutrition Coach")

app.include_router(profile.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def serve_index():
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health_check():
    return {"status": "ok"}