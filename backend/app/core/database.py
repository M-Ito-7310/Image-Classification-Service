from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

from app.core.config import settings

# Create SQLAlchemy engine
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite configuration
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={
            "check_same_thread": False,
            "timeout": 20
        },
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    # PostgreSQL configuration
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        echo=settings.DEBUG
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database():
    """Create database tables."""
    # Import all models to ensure they are registered
    from app.models.user import User, UserSession, ClassificationRecord
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

def drop_database():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully")

# Initialize database on module import for development
if settings.ENVIRONMENT == "development":
    try:
        create_database()
    except Exception as e:
        print(f"Database initialization warning: {e}")