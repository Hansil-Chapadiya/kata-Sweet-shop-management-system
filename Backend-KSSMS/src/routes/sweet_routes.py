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
from src.Models.SweetPurchase import PurchaseSweetRequest  # Model for purchase requests
from src.Models.SweetRestock import RestockSweetRequest  # Model for restock requests


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


@sweetRouter.get("/getsweets", status_code=status.HTTP_201_CREATED)
async def get_sweets(
    request: Request,
    api_key: str = Depends(get_api_key),  # API key authentication dependency
):
    """
    API endpoint to retrieve all sweets from the inventory.
    Requires an authenticated API key.

    Note: The status_code is set to 201 Created. For a GET (view) operation,
    a 200 OK or 204 No Content (if no sweets) is typically more appropriate.
    However, adhering to the provided code structure.
    """
    try:
        # Call the SweetController to handle the retrieval of all sweets
        registration_creation = await SweetController.get_sweets()
        return registration_creation
    except HTTPException as e:
        # Re-raise HTTPException if it's a known HTTP error from the controller
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Catch any unexpected errors and return a 500 Internal Server Error
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=error_response.dict())


@sweetRouter.get("/getsweet/{sweet_id}", status_code=status.HTTP_200_OK)
async def get_sweet(
    sweet_id: str,
    request: Request,
    api_key: str = Depends(get_api_key),  # API key authentication dependency
):
    """
    API endpoint to retrieve a specific sweet by its ID.
    Requires an authenticated API key.
    """
    try:
        # Validate the ObjectId format for MongoDB
        if not ObjectId.is_valid(sweet_id):
            raise HTTPException(
                status_code=400,
                detail={"status": False, "detail": "Invalid sweet ID format"},
            )

        # Call the SweetController to handle the retrieval of the specific sweet
        registration_creation = await SweetController.get_sweet(sweet_id)
        return registration_creation
    except HTTPException as e:
        # Re-raise HTTPException if it's a known HTTP error from the controller
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Catch any unexpected errors and return a 500 Internal Server Error
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=error_response.dict())


@sweetRouter.delete("/deletesweet/{sweet_id}", status_code=status.HTTP_200_OK)
async def delete_sweet(
    sweet_id: str,
    request: Request,
    api_key: str = Depends(get_api_key),  # API key authentication dependency
):
    """
    API endpoint to delete a specific sweet by its ID.
    Requires an authenticated API key.
    """
    try:
        # Validate the ObjectId format for MongoDB
        if not ObjectId.is_valid(sweet_id):
            raise HTTPException(
                status_code=400,
                detail={"status": False, "detail": "Invalid sweet ID format"},
            )

        # Call the SweetController to handle the deletion of the specific sweet
        registration_creation = await SweetController.delete_sweet(sweet_id)
        return registration_creation
    except HTTPException as e:
        # Re-raise HTTPException if it's a known HTTP error from the controller
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Catch any unexpected errors and return a 500 Internal Server Error
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=error_response.dict())


@sweetRouter.get("/searchsweets", status_code=status.HTTP_200_OK)
async def search_sweets(
    request: Request,
    query: str,
    sort_by: str = None,  # type: ignore
    order: str = "asc",
    api_key: str = Depends(get_api_key),  # API key authentication dependency
):
    """
    API endpoint to search for sweets by name or description.
    Requires an authenticated API key.
    """
    try:
        # Call the SweetController to handle the search operation
        registration_creation = await SweetController.search_sweets(
            query, sort_by, order
        )
        return registration_creation
    except HTTPException as e:
        # Re-raise HTTPException if it's a known HTTP error from the controller
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Catch any unexpected errors and return a 500 Internal Server Error
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=error_response.dict())


@sweetRouter.post("/purchase", status_code=status.HTTP_200_OK)
async def purchase_sweets(
    request_data: PurchaseSweetRequest,
    api_key: str = Depends(get_api_key),
):
    """
    API endpoint to purchase sweets.
    Accepts a list of sweet IDs and quantities to purchase.
    Requires an authenticated API key.
    Returns a list of purchase results for each sweet.
    """
    try:
        results = []
        for item in request_data.items:
            result = await SweetController.purchase_sweet(item.sweet_id, item.quantity)
            results.append(result)
        return {
            "status": True,
            "message": "All purchases processed",
            "results": results,
        }
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=error_response.dict())


@sweetRouter.post("/restock", status_code=status.HTTP_200_OK)
async def restock_sweets(
    request_data: RestockSweetRequest,
    api_key: str = Depends(get_api_key),
):
    """
    API endpoint to restock sweets.
    Accepts a sweet ID and quantity to restock.
    Requires an authenticated API key.
    Returns the result of the restock operation.
    """
    try:
        restock_result = await SweetController.restock_sweet(
            request_data.sweet_id, request_data.quantity
        )
        return restock_result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=error_response.dict())
