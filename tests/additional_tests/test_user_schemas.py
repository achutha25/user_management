import pytest
import uuid
from pydantic import ValidationError
from app.schemas.user_schemas import (
    UserCreate, UserUpdate, UserResponse,
    LoginRequest, UserListResponse, validate_url
)
from app.models.user_model import UserRole


def test_user_create_valid():
    user = UserCreate(
        email="test@example.com",
        password="Secure*1234",
        role=UserRole.AUTHENTICATED
    )
    assert user.email == "test@example.com"
    assert user.role == UserRole.AUTHENTICATED


def test_user_create_missing_password():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@example.com",
            role=UserRole.AUTHENTICATED
        )


def test_user_update_requires_one_field():
    with pytest.raises(ValidationError):
        UserUpdate()


def test_user_update_valid_partial():
    user = UserUpdate(first_name="John")
    assert user.first_name == "John"


def test_user_response_valid():
    user = UserResponse(
        id=uuid.uuid4(),
        email="john@example.com",
        nickname="johndoe",
        role=UserRole.AUTHENTICATED
    )
    assert isinstance(user.id, uuid.UUID)


def test_login_request_valid():
    login = LoginRequest(email="user@example.com", password="pass123")
    assert login.email == "user@example.com"


def test_user_list_response_structure():
    user1 = UserResponse(
        id=uuid.uuid4(),
        email="a@example.com",
        nickname="usera",
        role=UserRole.AUTHENTICATED
    )
    response = UserListResponse(items=[user1], total=1, page=1, size=1)
    assert len(response.items) == 1
    assert response.total == 1


@pytest.mark.parametrize("url", [
    "https://example.com",
    "http://test.org/page",
])
def test_validate_url_valid(url):
    assert validate_url(url) == url


@pytest.mark.parametrize("url", [
    "not-a-url",
    "ftp://invalid.com",
    "example.com",
])
def test_validate_url_invalid(url):
    with pytest.raises(ValueError):
        validate_url(url)

