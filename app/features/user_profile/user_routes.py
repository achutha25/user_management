from app.features.user_profile.routes import router as profile_router
router.include_router(profile_router, prefix="/profile", tags=["User Profile"])

