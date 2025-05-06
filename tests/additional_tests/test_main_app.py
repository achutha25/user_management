import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_app_register_route_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "email": "newuser@example.com",
            "password": "Secure123!",
            "role": "AUTHENTICATED"
        }
        response = await ac.post("/register/", json=payload)
        # Success or handled error confirms route is wired
        assert response.status_code in [200, 400, 500]

@pytest.mark.asyncio
async def test_global_exception_handler(monkeypatch):
    @app.get("/raise-error/")
    async def raise_error():
        raise RuntimeError("Simulated failure")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/raise-error/")
        assert response.status_code == 500
        assert response.json()["message"] == "An unexpected error occurred. Please try again later."

@pytest.mark.asyncio
async def test_cors_headers_allowed_origin():
    headers = {
        "Origin": "https://your-frontend.com"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.options("/register/", headers=headers)
        assert response.status_code in [200, 204]
        assert "access-control-allow-origin" in response.headers

