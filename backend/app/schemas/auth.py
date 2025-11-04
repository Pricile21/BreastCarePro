"""
Authentication schemas
"""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    Token response schema
    """
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """
    Token payload schema
    """
    sub: Optional[str] = None


class UserBase(BaseModel):
    """
    Base user schema
    """
    email: str
    full_name: str
    phone: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    """
    User creation schema
    """
    password: str


class MobileUserCreate(BaseModel):
    """
    Mobile user creation schema
    """
    name: str
    email: str
    phone: str
    password: str


class UserResponse(UserBase):
    """
    User response schema
    """
    id: str
    professional_id: Optional[str] = None
    user_type: Optional[str] = None
    
    class Config:
        from_attributes = True
