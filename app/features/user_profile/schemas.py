from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(None, example="Jane")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Engineer at Example Inc.")
    profile_picture_url: Optional[HttpUrl] = None
    linkedin_profile_url: Optional[HttpUrl] = None
    github_profile_url: Optional[HttpUrl] = None

