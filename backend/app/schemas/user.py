from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "clinician"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows reading from SQLAlchemy models


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"