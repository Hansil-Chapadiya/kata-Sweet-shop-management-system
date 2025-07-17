from fastapi import (
    HTTPException,
)  # Import HTTPException from FastAPI for custom exceptions
from pydantic import (
    BaseModel,
)  # Import BaseModel from Pydantic for data validation and serialization


class CustomHTTPException(HTTPException):
    """
    A custom HTTP exception class that extends FastAPI's HTTPException.
    This can be used to raise custom HTTP errors with specific status codes and details.
    """

    def __init__(self, status_code: int, detail: str):
        """
        Initializes the CustomHTTPException.

        Args:
            status_code (int): The HTTP status code to return (e.g., 400, 404, 500).
            detail (str): A message providing more details about the error.
        """
        super().__init__(status_code=status_code, detail=detail)


class ErrorResponseModel(BaseModel):
    """
    Pydantic model for a standardized error response body.
    Ensures consistent structure for error messages returned by the API.
    """

    status: bool  # Indicates the success or failure status of the operation (False for error)
    detail: str  # A string message providing details about the error
