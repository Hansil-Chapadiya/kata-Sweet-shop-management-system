import pytest
from httpx import AsyncClient
from api.main import app  # From your deployed entrypoint
from src.Models.Sweet import SweetBase, SweetCategory

@pytest.mark.asyncio
async def test_add_sweet_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/sweets", json={
            "name": "Kaju Katli",
            "category": "Nut-based",
            "price": 100.0,
            "quantity": 10,
            "discount": 10,
            "description": "Top tier",
            "image_url": "https://example.com/kaju.jpg"
        })
    assert response.status_code == 201
    assert response.json()["name"] == "Kaju Katli"
