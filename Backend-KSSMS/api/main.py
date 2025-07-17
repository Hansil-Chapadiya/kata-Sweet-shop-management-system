from fastapi import FastAPI
from src.routes import sweet_routes  # Import the APIRouter for sweet-related endpoints
from fastapi.middleware.cors import (
    CORSMiddleware,
)  # Import CORS middleware for handling cross-origin requests
from src.db.db_init import connect_to_mongo, close_mongo_connection # Import MongoDB connection functions

# from src.routes import * # This line is commented out; typically you'd import specific routers

# Initialize the FastAPI application
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo(app)

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection(app)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows your frontend (e.g., Next.js app) running on a different origin
# to make requests to this FastAPI backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows all origins. For production, specify your frontend's exact origin(s).
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["API-Key"],  # Explicitly allows the 'API-Key' header in requests
    expose_headers=[
        "API-Key"
    ],  # Allows the client to access the 'API-Key' header from responses
)

# app.include_router(sweet_routes.router, prefix="/sweets") # This line is commented out


# Define a root endpoint for the API
@app.get("/")
def root():
    """
    Root endpoint for the API.
    Returns a welcome message to confirm the backend is running.
    """
    return {"msg": "Sweet Shop Backend is Live 🍭"}


# Define a simple ping endpoint for health checks
@app.get("/ping")
def ping():
    """
    Health check endpoint.
    Returns 'pong' to indicate the service is responsive.
    """
    return {"msg": "pong"}


# Include the router for sweet-related functionalities
# This mounts all routes defined in sweet_routes.py under the main FastAPI application.
# Assuming 'sweetRouter' is the name of your APIRouter instance in sweet_routes.py.
app.include_router(sweet_routes.sweetRouter)
