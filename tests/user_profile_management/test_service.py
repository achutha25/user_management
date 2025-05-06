import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, timezone
from app.models.user_model import User, UserRole
from app.features.user_profile.service import UserProfileService

@pytest.mark.asyncio
async def test_update_profile_fields():
    session = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    user = User(id=uuid4(), first_name="Old", bio="Before")
    update_data = {"first_name": "New", "bio": "After"}

    updated_user = await UserProfileService.update_profile(session, user, update_data)

    assert updated_user.first_name == "New"
    assert updated_user.bio == "After"
    session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_upgrade_professional_status_success(monkeypatch):
    session = MagicMock()
    session.commit = AsyncMock()
    session.get = AsyncMock(return_value=User(id=uuid4(), email="x@y.com"))

    mock_email = MagicMock()
    mock_email.send_user_email = AsyncMock()

    admin = User(id=uuid4(), role=UserRole.ADMIN)

    result = await UserProfileService.upgrade_professional_status(
        session, uuid4(), admin, mock_email
    )
    assert result is True
    session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_upgrade_professional_status_denied(monkeypatch):
    session = MagicMock()
    user = User(id=uuid4(), role=UserRole.AUTHENTICATED)

    result = await UserProfileService.upgrade_professional_status(
        session, uuid4(), user, MagicMock()
    )
    assert result is False

