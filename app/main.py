from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes
from app.utils.api_description import getDescription
import logging

# Logger setup
logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

# Restrictive CORS settings (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # replace with actual allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        settings = get_settings()
        Database.initialize(settings.database_url, settings.debug)
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise RuntimeError("Database initialization failed") from e

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )

# Include user management routes
app.include_router(user_routes.router)

