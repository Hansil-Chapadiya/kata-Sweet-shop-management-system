from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)  # Asynchronous MongoDB driver for Python
from urllib.parse import (
    quote_plus,
)  # Used for URL-encoding special characters in connection strings
from fastapi import FastAPI  # FastAPI framework for building APIs
from config import params  # Import configuration parameters (e.g., MongoDB credentials)

# Retrieve MongoDB username and password from configuration parameters
username = params["username"]
password = params["password"]

# URL-encode the username and password to ensure special characters are handled correctly
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

# Initialize the asynchronous MongoDB client
# Connects to the MongoDB Atlas cluster using the provided credentials
client = AsyncIOMotorClient(
    f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.grvhoxa.mongodb.net/?authMechanism=DEFAULT"
)
# Select the 'kksm' database from the MongoDB client
database = client["kksm"]


async def connect_to_mongo(app: FastAPI):
    """
    Asynchronous function to establish a connection to MongoDB and attach it to the FastAPI application state.
    This function is typically called during the FastAPI application's startup event.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.state.mongodb = (
        database  # Attach the database connection to the app's state for easy access
    )
    app.state.mongodb_client = client  # Attach the client instance, useful for closing the connection gracefully later


async def get_database() -> AsyncIOMotorDatabase:
    """
    Asynchronous utility function to retrieve the MongoDB database instance.
    This function can be used as a dependency in FastAPI route functions.

    Returns:
        AsyncIOMotorDatabase: The connected MongoDB database instance.
    """
    return database
