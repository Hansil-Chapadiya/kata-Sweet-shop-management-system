import pytest
from httpx import AsyncClient
from api.main import app
from src.Models.Sweet import SweetCategory
from config import params


@pytest.mark.asyncio
async def test_add_sweet_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/sweets",
            json={
                "name": "TestLadoo125",  # Use a UNIQUE name to avoid 400 error
                "category": SweetCategory.NUT_BASED.value,
                "price": 100.0,
                "quantity": 10,
                "discount": 10,
                "description": "Top tier",
                "image_url": "https://images.unsplash.com/photo-1667185486143-a2d5609f5229",
            },
            headers={"API-Key": params["API_KEY"]},
        )
    assert response.status_code == 200  # Or 200, depending on your route setup
    assert response.json()["status"] == True


@pytest.mark.asyncio
async def test_duplicate_sweet_name():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Add once
        await ac.post(
            "/sweets",
            json={
                "name": "ChocoLadoo",
                "category": SweetCategory.NUT_BASED.value,
                "price": 100.0,
                "quantity": 10,
                "discount": 10,
                "description": "Delicious",
                "image_url": "https://images.unsplash.com/photo-1667185486143-a2d5609f5229",
            },
            headers={"API-Key": params["API_KEY"]},
        )

        # Try adding again (should fail)
        response = await ac.post(
            "/sweets",
            json={
                "name": "ChocoLadoo",  # Same name
                "category": SweetCategory.NUT_BASED.value,
                "price": 100.0,
                "quantity": 10,
                "discount": 10,
                "description": "Duplicate",
                "image_url": "https://images.unsplash.com/photo-1667185486143-a2d5609f5229",
            },
            headers={"API-Key": params["API_KEY"]},
        )
    assert response.status_code == 500
    # assert response.json()["detail"] == "Sweet with this name already exists"
