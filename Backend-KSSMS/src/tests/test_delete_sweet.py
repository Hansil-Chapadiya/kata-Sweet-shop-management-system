import pytest
from httpx import AsyncClient
from api.main import app
from src.Models.Sweet import SweetCategory
from config import params

@pytest.mark.asyncio
async def test_delete_sweet():
    """
    Creates a sweet, fetches its ID, and deletes it.
    """
    sweet_name = "DeleteMeLadoo"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Add sweet
        add_response = await ac.post(
            "/addsweet",
            json={
                "name": sweet_name,
                "category": SweetCategory.NUT_BASED.value,
                "price": 50.0,
                "quantity": 5,
                "discount": 5,
                "description": "Will be deleted",
                "image_url": "https://images.unsplash.com/photo-1667185486143-a2d5609f5229",
            },
            headers={"API-Key": params["API_KEY"]},
        )
        assert add_response.status_code == 200
        sweet_id = add_response.json()["sweet_id"]

        # Delete sweet
        delete_response = await ac.delete(
            f"/deletesweet/{sweet_id}",
            headers={"API-Key": params["API_KEY"]},
        )
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Sweet deleted successfully"
