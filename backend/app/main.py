from fastapi import FastAPI

app = FastAPI(title="Smart Fridge & Nutrition Coach")


@app.get("/health")
async def health_check():
    return {"status": "ok"}