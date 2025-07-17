from fastapi import HTTPException
from pydantic import BaseModel

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class ErrorResponseModel(BaseModel):
    status: bool
    detail: str