from fastapi import (
    APIRouter,
    HTTPException,
    Body,
    Depends,
    Request,
    UploadFile,
    File,
    status,
)
from fastapi.background import BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from response_error import ErrorResponseModel
from ..Controllers.check_secrete_key import authenticate_api_key
from ..Controllers.SweetController import SweetController
from src.Models.Sweet import SweetBase
from typing import List
from bson import ObjectId

sweetRouter = APIRouter()


async def get_api_key(api_key: str = Depends(APIKeyHeader(name="API-Key"))):
    if api_key and not authenticate_api_key(api_key):
        error_response = ErrorResponseModel(status=False, detail="Invalid API-Key")
        raise HTTPException(status_code=404, detail=dict(error_response))
    return api_key


@sweetRouter.post("/sweets", status_code=status.HTTP_201_CREATED)
async def add_sweet(
    request: Request,
    background_tasks: BackgroundTasks,
    register_data: SweetBase = Body(...),
    api_key: str = Depends(get_api_key),
):
    try:
        registration_creation = await SweetController.create_sweet(
            register_data, background_tasks
        )
        return registration_creation
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        error_response = ErrorResponseModel(status=False, detail=str(e))
        raise HTTPException(status_code=500, detail=error_response.dict())
