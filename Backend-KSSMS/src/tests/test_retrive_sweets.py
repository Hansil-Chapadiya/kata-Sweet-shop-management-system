import pytest
from httpx import AsyncClient
from api.main import app
from src.Models.Sweet import SweetCategory
from config import params


@pytest.mark.asyncio
async def test_view_sweets():
    """
    Tests that all sweets can be fetched successfully.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/getsweets",
            headers={"API-Key": params["API_KEY"]},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == True
    assert isinstance(data["sweets"], list)  # should return a list of sweets
