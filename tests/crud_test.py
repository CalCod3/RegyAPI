import pytest
from httpx import AsyncClient

from ..api import app


@pytest.mark.anyio
async def test_get_athletes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/athletes")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_athlete_by_id(athlete_id: int):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/athletes")
    assert response.status_code == 200