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
            "image_url": "https://images.unsplash.com/photo-1667185486143-a2d5609f5229?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        })
    assert response.status_code == 201
    assert response.json()["name"] == "Kaju Katli"
