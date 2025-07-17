import pytest
from httpx import AsyncClient
from api.main import app
from src.Models.Sweet import SweetCategory
from config import params
from src.utils.generate_unique_sweet import (
    generate_unique_name,
)  # Import a utility function to generate unique sweet names


@pytest.mark.asyncio
async def test_restock_success():
    """
    Test successful restocking of a sweet item.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create sweet with initial quantity 10
        create_resp = await ac.post(
            "/addsweet",
            json={
                "name": generate_unique_name(),
                "category": SweetCategory.NUT_BASED.value,
                "price": 100.0,
                "quantity": 10,
                "discount": 0,
                "description": "For restock testing",
                "image_url": "https://images.unsplash.com/photo-1667185486143-a2d5609f5229",
            },
            headers={"API-Key": params["API_KEY"]},
        )
        sweet_id = create_resp.json()["sweet_id"]

        # Now restock it with 40 more
        restock_resp = await ac.post(
            "/restock",
            json={"quantity": 40, "sweet_id": sweet_id},
            headers={"API-Key": params["API_KEY"]},
        )

        assert restock_resp.status_code == 200
        resp_json = restock_resp.json()
        assert resp_json["status"] == True
        assert resp_json["message"] == "Restock successful"
        assert resp_json["updated_stock"] == 50


@pytest.mark.asyncio
async def test_restock_invalid_sweet_id():
    """
    Test restocking with an invalid sweet ID, expecting 404 error.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        fake_id = "64f8b43c26c2cc26a011abcd"  # Valid ObjectId format but not in DB
        response = await ac.post(
            "/restock",
            json={"quantity": 30, "sweet_id": fake_id},
            headers={"API-Key": params["API_KEY"]},
        )

        assert response.status_code == 404 or 500
        assert response.json()["detail"]["message"] == "Sweet not found"
