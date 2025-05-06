import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app

# NOTE: These assume a working test client fixture, test DB, and mock user/role setup
# If not available, let me know and I’ll help mock those dependencies in conftest.py

@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient):
    payload = {
        "email": "testuser@example.com",
        "password": "StrongPass123!",
        "role": "AUTHENTICATED"
    }
    response = await async_client.post("/register/", json=payload)
    assert response.status_code == 200
    assert "email" in response.json()

@pytest.mark.asyncio
async def test_register_duplicate_email(async_client: AsyncClient):
    payload = {
        "email": "testuser@example.com",  # same as above
        "password": "AnotherPass!23",
        "role": "AUTHENTICATED"
    }
    response = await async_client.post("/register/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

@pytest.mark.asyncio
async def test_login_valid_credentials(async_client: AsyncClient):
    form_data = {
        "username": "testuser@example.com",
        "password": "StrongPass123!"
    }
    response = await async_client.post("/login/", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_credentials(async_client: AsyncClient):
    form_data = {
        "username": "testuser@example.com",
        "password": "WrongPass"
    }
    response = await async_client.post("/login/", data=form_data)
    assert response.status_code == 401
    assert "Authentication failed" in response.json()["detail"]

@pytest.mark.asyncio
async def test_verify_email_invalid_token(async_client: AsyncClient):
    response = await async_client.get("/verify-email/?token=invalid-token")
    assert response.status_code == 400
    assert "Email verification failed" in response.json()["detail"]

# Assume this gets overridden in a fixture with an admin user's auth header
@pytest.mark.asyncio
async def test_list_users_admin_access(async_client: AsyncClient, admin_auth_headers):
    response = await async_client.get("/users/?skip=0&limit=5", headers=admin_auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_list_users_unauthenticated(async_client: AsyncClient):
    response = await async_client.get("/users/?skip=0&limit=5")
    assert response.status_code == 401 or response.status_code == 403

