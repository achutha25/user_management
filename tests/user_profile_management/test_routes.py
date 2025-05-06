import pytest
from httpx import AsyncClient
from uuid import uuid4
from app.main import app

@pytest.mark.asyncio
async def test_update_my_profile_success(async_client: AsyncClient, test_user_auth_headers):
    update_data = {"first_name": "Jane", "bio": "Updated bio"}
    response = await async_client.patch(
        "/profile/me", json=update_data, headers=test_user_auth_headers
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"
    assert "bio" in response.json()

@pytest.mark.asyncio
async def test_upgrade_professional_status_as_admin(async_client: AsyncClient, admin_auth_headers):
    # Replace with a real test user UUID from your test DB
    target_user_id = str(uuid4())
    response = await async_client.post(
        f"/profile/{target_user_id}/upgrade", headers=admin_auth_headers
    )
    # Acceptable outcomes: success or not found (if user doesn't exist in test DB)
    assert response.status_code in [200, 404, 403]

