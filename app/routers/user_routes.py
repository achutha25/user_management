from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import UserCreate, UserResponse, TokenResponse
from app.services.user_service import UserService
from app.dependencies import get_db, get_current_user
from app.enums.user_roles import UserRole
from app.services.email_service import EmailService
from app.dependencies import get_email_service

router = APIRouter()

@router.post("/register/", response_model=UserResponse, tags=["Login and Registration"])
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
    email_service: EmailService = Depends(get_email_service)
):
    try:
        user = await UserService.register_user(session, user_data.model_dump(), email_service)
        if user:
            return user
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/login/", response_model=TokenResponse, tags=["Login and Registration"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    try:
        token = await UserService.authenticate_user(session, form_data)
        return token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

@router.get("/verify-email/", tags=["Login and Registration"])
async def verify_email(
    token: str,
    session: AsyncSession = Depends(get_db)
):
    try:
        result = await UserService.verify_email_token(session, token)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Email verification failed: {str(e)}")

@router.get("/users/", response_model=list[UserResponse], tags=["User Operations"])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can view users.")
    try:
        users = await UserService.get_all_users(session, skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

