from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.user_model import User, UserRole
from app.schemas.user_schemas import UserUpdate
from app.features.user_profile.schemas import UserProfileUpdate
from app.services.email_service import EmailService

class UserProfileService:

    @staticmethod
    async def update_profile(session: AsyncSession, user: User, update_data: dict) -> User:
        for field, value in update_data.items():
            setattr(user, field, value)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def upgrade_professional_status(
        session: AsyncSession, user_id: UUID, upgraded_by: User, email_service: EmailService
    ) -> bool:
        if upgraded_by.role not in [UserRole.MANAGER, UserRole.ADMIN]:
            return False

        user = await session.get(User, user_id)
        if user is None:
            return False

        user.is_professional = True
        user.professional_status_updated_at = datetime.now(timezone.utc)

        session.add(user)
        await session.commit()
        await email_service.send_user_email({
            "name": user.first_name or "User",
            "email": user.email,
        }, "professional_upgrade")

        return True

