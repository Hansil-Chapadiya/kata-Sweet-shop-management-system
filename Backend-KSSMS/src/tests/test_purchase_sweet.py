import pytest  # The testing framework for Python
from httpx import AsyncClient  # An asynchronous HTTP client for making requests
from api.main import app  # Import the FastAPI application instance
from src.Models.Sweet import (
    SweetCategory,
)  # Import the SweetCategory Enum for valid sweet categories
from config import params  # Import configuration parameters, including the API key
from src.utils.generate_unique_sweet import (
    generate_unique_name,
)  # Import a utility function to generate unique sweet names


@pytest.mark.asyncio
async def test_purchase_sweet_success():
    """Test successful sweet purchase"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create sweet with quantity 20
        create_resp = await ac.post(
            "/addsweet",
            json={
                "name": generate_unique_name(),
                "category": SweetCategory.CHOCOLATE.value,
                "price": 200.0,
                "quantity": 20,
            },
            headers={"API-Key": params["API_KEY"]},
        )
        sweet_id = create_resp.json()["sweet_id"]

        # Purchase 5 items
        purchase_resp = await ac.post(
            f"/purchase",
            json={"items": [{"quantity": 5, "sweet_id": sweet_id}]},
            headers={"API-Key": params["API_KEY"]},
        )
        assert purchase_resp.status_code == 200
        assert purchase_resp.json()["results"][0]["remaining_quantity"] == 15


@pytest.mark.asyncio
async def test_purchase_invalid_sweet_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Try purchasing with a fake sweet_id
        fake_id = "60b8d6f8c25e4a2e95d90f00"
        purchase_resp = await ac.post(
            f"/purchase",
            json={"items": [{"quantity": 2, "sweet_id": fake_id}]},
            headers={"API-Key": params["API_KEY"]},
        )
        assert purchase_resp.status_code == 500
        assert purchase_resp.json()["detail"]["status"] == False
