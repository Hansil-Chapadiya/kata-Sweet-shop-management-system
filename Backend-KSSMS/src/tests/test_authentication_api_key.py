import pytest  # The testing framework for Python
from httpx import AsyncClient  # An asynchronous HTTP client for making requests
from api.main import app  # Import the FastAPI application instance
from src.Models.Sweet import (
    SweetCategory,
)  # Import the SweetCategory Enum for valid sweet categories

# --- Authentication Tests ---
@pytest.mark.asyncio
async def test_missing_api_key():
    """Test requests without API key"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/sweets",
            json={
                "name": "TestSweet",
                "category": SweetCategory.CANDY.value,
                "price": 10.0,
                "quantity": 100
            }
            # No API key header
        )
        assert response.status_code == 404