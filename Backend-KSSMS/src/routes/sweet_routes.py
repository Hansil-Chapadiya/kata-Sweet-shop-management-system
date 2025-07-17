from fastapi import (
    APIRouter,  # APIRouter for organizing routes
    HTTPException,  # Used for raising HTTP exceptions
    Body,  # Used to declare a request body parameter
    Depends,  # Used for dependency injection
    Request,  # To access request details
    UploadFile,  # For handling file uploads (though not used in this snippet)
    File,  # For handling file uploads (though not used in this snippet)
    status,  # HTTP status codes
)

from fastapi.background import BackgroundTasks  # For running tasks in the background
from fastapi.responses import JSONResponse  # For returning JSON responses
from fastapi.security import APIKeyHeader  # Security utility for API key in headers
from response_error import ErrorResponseModel  # Custom error response model

from ..Controllers.check_secrete_key import (
    authenticate_api_key,
)  # Function to authenticate API key
from ..Controllers.SweetController import (
    SweetController,
)  # Controller for sweet-related business logic
from src.Models.Sweet import SweetBase  # Pydantic model for sweet data


from typing import List  # For type hints
from bson import ObjectId  # For handling MongoDB's ObjectId

# Initialize FastAPI APIRouter for sweet-related endpoints
sweetRouter = APIRouter()


async def get_api_key(api_key: str = Depends(APIKeyHeader(name="API-Key"))):
    """
    Dependency function to extract and authenticate the API-Key from request headers.
    If the API key is missing or invalid, it raises an HTTPException.
    """
    if api_key and not authenticate_api_key(api_key):
        error_response = ErrorResponseModel(status=False, detail="Invalid API-Key")
        raise HTTPException(status_code=404, detail=dict(error_response))
    return api_key


@sweetRouter.post("/addsweet", status_code=status.HTTP_201_CREATED)
async def add_sweet(
    request: Request,
    background_tasks: BackgroundTasks,  # Dependency for running background tasks
    register_data: SweetBase = Body(
        ...
    ),  # Request body validated against SweetBase model
    api_key: str = Depends(get_api_key),  # API key authentication dependency
):
    """
    API endpoint to add a new sweet to the inventory.
    Requires an authenticated API key.
    On success, returns 201 Created status.
    """
    try:
        # Call the SweetController to handle the creation of the sweet
        registration_creation = await SweetController.create_sweet(
            register_data, background_tasks
        )
        return registration_creation
    except HTTPException as e:
        # Re-raise HTTPException if it's a known HTTP error from the controller
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Catch any unexpected errors and return a 500 Internal Server Error
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=error_response.dict())
