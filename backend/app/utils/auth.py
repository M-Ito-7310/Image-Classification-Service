from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict
import secrets
import uuid

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User, UserSession
from app.schemas.auth import TokenData

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token() -> str:
    """Create secure refresh token."""
    return secrets.token_urlsafe(32)

def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        scopes: list = payload.get("scopes", [])
        
        if username is None or user_id is None:
            return None
            
        return TokenData(username=username, user_id=user_id, scopes=scopes)
        
    except JWTError:
        return None

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user with username/email and password."""
    # Try to find user by username or email
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
        
    return user

def create_user_session(
    db: Session, 
    user: User, 
    user_agent: Optional[str] = None,
    ip_address: Optional[str] = None
) -> tuple[str, str]:
    """Create new user session and return access and refresh tokens."""
    
    # Create access token
    access_token_data = {
        "sub": user.username,
        "user_id": user.id,
        "scopes": ["admin"] if user.is_admin else ["user"]
    }
    access_token = create_access_token(access_token_data)
    
    # Create refresh token
    refresh_token = create_refresh_token()
    
    # Calculate expiration time
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Create session record
    session = UserSession(
        user_id=user.id,
        session_token=str(uuid.uuid4()),
        refresh_token=refresh_token,
        expires_at=expires_at,
        user_agent=user_agent,
        ip_address=ip_address,
        is_active=True
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return access_token, refresh_token

def revoke_user_session(db: Session, refresh_token: str) -> bool:
    """Revoke user session by refresh token."""
    session = db.query(UserSession).filter(
        UserSession.refresh_token == refresh_token,
        UserSession.is_active == True
    ).first()
    
    if not session:
        return False
    
    session.is_active = False
    db.commit()
    
    return True

def get_user_from_token(db: Session, token: str) -> Optional[User]:
    """Get user from JWT token."""
    token_data = verify_token(token)
    if not token_data:
        return None
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    return user


def refresh_access_token(db: Session, refresh_token: str) -> Optional[tuple[str, str]]:
    """Refresh access token using refresh token."""
    session = db.query(UserSession).filter(
        UserSession.refresh_token == refresh_token,
        UserSession.is_active == True,
        UserSession.expires_at > datetime.now(timezone.utc)
    ).first()
    
    if not session:
        return None
    
    user = session.user
    if not user or not user.is_active:
        return None
    
    # Create new tokens
    access_token_data = {
        "sub": user.username,
        "user_id": user.id,
        "scopes": ["admin"] if user.is_admin else ["user"]
    }
    new_access_token = create_access_token(access_token_data)
    new_refresh_token = create_refresh_token()
    
    # Update session with new refresh token
    session.refresh_token = new_refresh_token
    session.expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db.commit()
    
    return new_access_token, new_refresh_token

def get_api_key_info(api_key: str) -> Dict[str, Any]:
    """
    Get API key information for billing/monetization.
    TODO: Implement proper API key validation and rate limiting.
    """
    # Temporary implementation for development
    return {
        "user_id": "demo_user",
        "tier": "free",
        "requests_remaining": 1000,
        "valid": True
    }