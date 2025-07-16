from fastapi import FastAPI
from src.routes import sweet_routes
# from src.routes import *  # assuming you’ll add this

app = FastAPI()

# app.include_router(sweet_routes.router, prefix="/sweets")


@app.get("/")
def root():
    return {"msg": "Sweet Shop Backend is Live 🍭"}

app.include_router(sweet_routes.sweetRouter, prefix="/sweets", tags=["Sweets"])
