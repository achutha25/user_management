import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, timezone

from app.services.user_service import UserService
from app.models.user_model import User, UserRole
from app.utils.security import hash_password

@pytest.fixture
def mock_session():
    session = MagicMock(spec=["execute", "add", "commit", "refresh", "rollback", "delete"])
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = MagicMock()
    session.delete = AsyncMock()
    return session

@pytest.fixture
def mock_email_service():
    svc = MagicMock()
    svc.send_verification_email = AsyncMock()
    return svc

@pytest.mark.asyncio
async def test_register_user_creates_new_user(mock_session, mock_email_service, monkeypatch):
    # Simulate no user exists
    monkeypatch.setattr(UserService, "get_by_email", AsyncMock(return_value=None))
    monkeypatch.setattr(UserService, "get_by_nickname", AsyncMock(return_value=None))
    monkeypatch.setattr(UserService, "count", AsyncMock(return_value=1))  # simulate non-admin

    user_data = {
        "email": "test@example.com",
        "password": "TestPass123!",
        "role": "AUTHENTICATED"
    }

    user = await UserService.register_user(mock_session, user_data, mock_email_service)
    assert user.email == "test@example.com"
    assert user.nickname is not None
    mock_email_service.send_verification_email.assert_awaited_once()

@pytest.mark.asyncio
async def test_login_user_valid(mock_session, monkeypatch):
    fake_user = User(
        id=uuid4(),
        email="user@test.com",
        nickname="tester",
        hashed_password=hash_password("Test123!"),
        role=UserRole.AUTHENTICATED,
        email_verified=True
    )
    monkeypatch.setattr(UserService, "get_by_email", AsyncMock(return_value=fake_user))
    result = await UserService.login_user(mock_session, "user@test.com", "Test123!")
    assert result == fake_user

@pytest.mark.asyncio
async def test_login_user_invalid_password(mock_session, monkeypatch):
    fake_user = User(
        id=uuid4(),
        email="user@test.com",
        nickname="tester",
        hashed_password=hash_password("RightPass123"),
        role=UserRole.AUTHENTICATED,
        email_verified=True
    )
    monkeypatch.setattr(UserService, "get_by_email", AsyncMock(return_value=fake_user))
    result = await UserService.login_user(mock_session, "user@test.com", "WrongPass")
    assert result is None

@pytest.mark.asyncio
async def test_verify_email_with_valid_token(mock_session, monkeypatch):
    fake_user = User(id=uuid4(), email="a@test.com", verification_token="abc123")
    monkeypatch.setattr(UserService, "get_by_id", AsyncMock(return_value=fake_user))
    result = await UserService.verify_email_with_token(mock_session, fake_user.id, "abc123")
    assert result is True
    assert fake_user.verification_token is None
    assert fake_user.email_verified is True

@pytest.mark.asyncio
async def test_verify_email_with_invalid_token(mock_session, monkeypatch):
    fake_user = User(id=uuid4(), email="a@test.com", verification_token="abc123")
    monkeypatch.setattr(UserService, "get_by_id", AsyncMock(return_value=fake_user))
    result = await UserService.verify_email_with_token(mock_session, fake_user.id, "wrong")
    assert result is False

@pytest.mark.asyncio
async def test_reset_password(mock_session, monkeypatch):
    user = User(id=uuid4(), email="a@test.com")
    monkeypatch.setattr(UserService, "get_by_id", AsyncMock(return_value=user))
    result = await UserService.reset_password(mock_session, user.id, "newPassword!123")
    assert result is True
    assert user.failed_login_attempts == 0
    assert user.is_locked is False

@pytest.mark.asyncio
async def test_unlock_user_account(mock_session, monkeypatch):
    user = User(id=uuid4(), email="a@test.com", is_locked=True, failed_login_attempts=3)
    monkeypatch.setattr(UserService, "get_by_id", AsyncMock(return_value=user))
    result = await UserService.unlock_user_account(mock_session, user.id)
    assert result is True
    assert user.is_locked is False
    assert user.failed_login_attempts == 0

@pytest.mark.asyncio
async def test_count_users(mock_session):
    mock_session.execute.return_value.scalar.return_value = 7
    result = await UserService.count(mock_session)
    assert result == 7

