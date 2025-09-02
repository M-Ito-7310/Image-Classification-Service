from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# User Registration Schema
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password (8-100 characters)")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name (optional)")

class UserLogin(BaseModel):
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    
class PasswordChange(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password (8-100 characters)")

# Token Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Token expiration time in seconds")

class TokenRefresh(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    scopes: list[str] = []

# Authentication Response
class AuthResponse(BaseModel):
    user: UserResponse
    token: Token
    message: str = "Authentication successful"

# Session Schema
class UserSessionResponse(BaseModel):
    id: int
    session_token: str
    expires_at: datetime
    created_at: datetime
    is_active: bool
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    
    class Config:
        from_attributes = True