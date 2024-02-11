import pytest
from httpx import AsyncClient

from api import app


@pytest.mark.anyio
async def test_get_athletes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/athletes")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_athlete_by_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/athletes/1")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_boxes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/boxes")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_attendances():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/attendance/1")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_workouts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/workouts")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_news():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/news")
    assert response.status_code == 200

@pytest.mark.anyio
async def test_get_events():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/events")
    assert response.status_code == 200
