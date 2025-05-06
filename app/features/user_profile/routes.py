from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.dependencies import get_db, get_current_user, get_email_service
from app.features.user_profile.schemas import UserProfileUpdate
from app.features.user_profile.service import UserProfileService
from app.services.email_service import EmailService
from app.schemas.user_schemas import UserResponse

router = APIRouter()

@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    update_data: UserProfileUpdate,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated = await UserProfileService.update_profile(session, current_user, update_data.dict(exclude_unset=True))
    return updated

@router.post("/{user_id}/upgrade", response_model=dict)
async def upgrade_user_professional_status(
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
    email_service: EmailService = Depends(get_email_service)
):
    success = await UserProfileService.upgrade_professional_status(session, user_id, current_user, email_service)
    if not success:
        raise HTTPException(status_code=403, detail="You are not authorized to upgrade this user.")
    return {"message": "User upgraded to professional status."}

