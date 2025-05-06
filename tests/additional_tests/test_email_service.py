import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.email_service import EmailService
from app.models.user_model import User
import uuid

class DummySettings:
    smtp_server = "smtp.test.com"
    smtp_port = 587
    smtp_username = "user"
    smtp_password = "pass"
    server_base_url = "https://test.api/"


@pytest.mark.asyncio
async def test_send_user_email_valid(monkeypatch):
    # Mock TemplateManager
    mock_template_manager = MagicMock()
    mock_template_manager.render_template.return_value = "<html>Email</html>"

    # Patch SMTPClient.send_email to do nothing
    mock_smtp = MagicMock()
    mock_smtp.send_email = MagicMock()

    monkeypatch.setattr("app.services.email_service.SMTPClient", lambda **kwargs: mock_smtp)
    monkeypatch.setattr("app.services.email_service.settings", DummySettings)

    service = EmailService(mock_template_manager)

    user_data = {
        "name": "John",
        "verification_url": "https://example.com",
        "email": "john@example.com"
    }

    await service.send_user_email(user_data, "email_verification")

    mock_template_manager.render_template.assert_called_once_with("email_verification", **user_data)
    mock_smtp.send_email.assert_called_once_with(
        "Verify Your Account",
        "<html>Email</html>",
        "john@example.com"
    )


@pytest.mark.asyncio
async def test_send_user_email_invalid_type(monkeypatch):
    mock_template_manager = MagicMock()
    monkeypatch.setattr("app.services.email_service.SMTPClient", lambda **kwargs: MagicMock())
    monkeypatch.setattr("app.services.email_service.settings", DummySettings)

    service = EmailService(mock_template_manager)

    with pytest.raises(ValueError):
        await service.send_user_email({"email": "a@test.com"}, "invalid_type")


@pytest.mark.asyncio
async def test_send_verification_email(monkeypatch):
    # Setup
    mock_template_manager = MagicMock()
    mock_template_manager.render_template.return_value = "<html>Email</html>"
    mock_smtp = MagicMock()
    mock_smtp.send_email = MagicMock()

    monkeypatch.setattr("app.services.email_service.SMTPClient", lambda **kwargs: mock_smtp)
    monkeypatch.setattr("app.services.email_service.settings", DummySettings)

    service = EmailService(mock_template_manager)

    user = User(
        id=uuid.uuid4(),
        email="verify@test.com",
        first_name="Veronica",
        nickname="v",
        role="AUTHENTICATED",
        hashed_password="abc"
    )
    user.verification_token = "token123"

    await service.send_verification_email(user)

    mock_template_manager.render_template.assert_called_once()
    mock_smtp.send_email.assert_called_once()

