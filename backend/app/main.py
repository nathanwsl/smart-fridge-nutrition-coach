from fastapi import FastAPI
from app.routers import profile


app = FastAPI(title="Smart Fridge & Nutrition Coach")

app.include_router(profile.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}