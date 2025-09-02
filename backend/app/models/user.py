from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone

from app.core.database import Base

class User(Base):
    """User model for authentication and user management."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationship to classification records
    classification_records = relationship("ClassificationRecord", back_populates="user")
    user_sessions = relationship("UserSession", back_populates="user")
    custom_models = relationship("CustomModel", back_populates="user")


class UserSession(Base):
    """User session model for tracking active sessions."""
    
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String, unique=True, index=True, nullable=False)
    refresh_token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    user_agent = Column(String)
    ip_address = Column(String)
    
    # Relationship to user
    user = relationship("User", back_populates="user_sessions")


class ClassificationRecord(Base):
    """Classification record model for storing user's classification history."""
    
    __tablename__ = "classification_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # nullable for anonymous users
    image_filename = Column(String, nullable=False)
    image_path = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    predictions = Column(String, nullable=False)  # JSON string of predictions
    processing_time = Column(Integer)  # milliseconds
    confidence_score = Column(String)  # highest confidence score
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to user
    user = relationship("User", back_populates="classification_records")


class CustomModel(Base):
    """Custom model model for user-uploaded ML models."""
    
    __tablename__ = "custom_models"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_id = Column(String, unique=True, index=True, nullable=False)  # UUID
    name = Column(String, nullable=False)
    description = Column(String)
    model_type = Column(String, nullable=False)  # 'tensorflow' or 'pytorch'
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # bytes
    classes = Column(String, nullable=False)  # JSON string of class names
    status = Column(String, nullable=False, default='uploaded')  # uploaded, validated, active, error
    validation_error = Column(String)  # error message if validation fails
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to user
    user = relationship("User", back_populates="custom_models")