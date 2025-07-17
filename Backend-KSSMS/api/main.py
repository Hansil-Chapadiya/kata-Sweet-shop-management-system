from fastapi import FastAPI
from src.routes import sweet_routes
from fastapi.middleware.cors import CORSMiddleware
# from src.routes import *  # assuming you’ll add this

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["API-Key"],  # Explicitly allow your header
    expose_headers=["API-Key"]
)

# app.include_router(sweet_routes.router, prefix="/sweets")


@app.get("/")
def root():
    return {"msg": "Sweet Shop Backend is Live 🍭"}

@app.get("/ping")
def ping():
    return {"msg": "pong"}


app.include_router(sweet_routes.sweetRouter)
