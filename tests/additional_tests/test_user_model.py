import uuid
from datetime import datetime
from app.models.user_model import User, UserRole

def create_test_user():
    return User(
        id=uuid.uuid4(),
        nickname="testuser",
        email="test@example.com",
        role=UserRole.AUTHENTICATED,
        hashed_password="hashedpassword123"
    )

def test_user_repr():
    user = create_test_user()
    assert str(user) == f"<User testuser, Role: {user.role.name}>"

def test_lock_unlock_account():
    user = create_test_user()
    assert not user.is_locked
    user.lock_account()
    assert user.is_locked
    user.unlock_account()
    assert not user.is_locked

def test_email_verification():
    user = create_test_user()
    assert not user.email_verified
    user.verify_email()
    assert user.email_verified

def test_has_role_true():
    user = create_test_user()
    assert user.has_role(UserRole.AUTHENTICATED)

def test_has_role_false():
    user = create_test_user()
    assert not user.has_role(UserRole.ADMIN)

def test_update_professional_status():
    user = create_test_user()
    assert not user.is_professional
    user.update_professional_status(True)
    assert user.is_professional
    # We can't assert exact timestamp since func.now() is a SQLAlchemy function,
    # but we can assert the attribute is set
    assert user.professional_status_updated_at is not None

