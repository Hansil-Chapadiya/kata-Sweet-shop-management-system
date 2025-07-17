from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from urllib.parse import quote_plus
from fastapi import FastAPI
from config import params  # Your config module

# Retrieve MongoDB username and password from configuration parameters
username = params["username"]
password = params["password"]

# URL-encode the username and password to ensure special characters are handled correctly
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

# Initialize the asynchronous MongoDB client
client = AsyncIOMotorClient(
    f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.grvhoxa.mongodb.net/?authMechanism=DEFAULT"
)

# Select the 'kksm' database
database = client["kksm"]


async def connect_to_mongo(app: FastAPI):
    app.state.mongodb = database
    app.state.mongodb_client = client


async def close_mongo_connection(app: FastAPI):
    app.state.mongodb_client.close()


async def get_database() -> AsyncIOMotorDatabase:
    return database
