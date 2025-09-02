#!/usr/bin/env python3
"""
Demo data initialization script for AI Image Classification Service.
Creates demo users and sample classification history data.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json
import random

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_database
from app.models.user import User, UserSession, ClassificationRecord
from app.utils.auth import get_password_hash, create_access_token, create_refresh_token
from app.core.config import settings

def create_demo_users(db: Session) -> dict:
    """Create demo users for testing and demonstration."""
    
    demo_users = []
    
    # Demo User 1: Regular user
    demo_user = User(
        username="demo",
        email="demo@example.com",
        hashed_password=get_password_hash("demo1234"),
        full_name="Demo User",
        is_active=True,
        is_admin=False,
        created_at=datetime.now(timezone.utc) - timedelta(days=30),
        last_login=datetime.now(timezone.utc) - timedelta(hours=2)
    )
    
    # Demo User 2: Admin user
    admin_user = User(
        username="admin",
        email="admin@example.com", 
        hashed_password=get_password_hash("admin1234"),
        full_name="Admin User",
        is_active=True,
        is_admin=True,
        created_at=datetime.now(timezone.utc) - timedelta(days=60),
        last_login=datetime.now(timezone.utc) - timedelta(minutes=30)
    )
    
    # Demo User 3: Sample user with Japanese name
    sample_user = User(
        username="yamada",
        email="yamada@example.jp",
        hashed_password=get_password_hash("yamada1234"),
        full_name="山田太郎",
        is_active=True,
        is_admin=False,
        created_at=datetime.now(timezone.utc) - timedelta(days=15),
        last_login=datetime.now(timezone.utc) - timedelta(days=1)
    )
    
    # Check if users already exist before creating
    for user in [demo_user, admin_user, sample_user]:
        existing_user = db.query(User).filter(User.username == user.username).first()
        if not existing_user:
            db.add(user)
            demo_users.append(user)
            print(f"Created user: {user.username}")
        else:
            demo_users.append(existing_user)
            print(f"User already exists: {user.username}")
    
    db.commit()
    
    # Refresh users to get IDs
    for user in demo_users:
        db.refresh(user)
    
    return {
        'demo': demo_users[0],
        'admin': demo_users[1], 
        'yamada': demo_users[2]
    }

def create_sample_classification_data(db: Session, users: dict) -> None:
    """Create sample classification history data."""
    
    # Sample classification results
    sample_classifications = [
        {
            "image_filename": "cat_001.jpg",
            "predictions": [
                {"class_name": "Egyptian cat", "confidence": 0.94, "class_id": 285},
                {"class_name": "tabby cat", "confidence": 0.89, "class_id": 281},
                {"class_name": "tiger cat", "confidence": 0.12, "class_id": 282}
            ],
            "model_used": "resnet50_imagenet",
            "processing_time": 0.421
        },
        {
            "image_filename": "dog_golden.jpg", 
            "predictions": [
                {"class_name": "golden retriever", "confidence": 0.96, "class_id": 207},
                {"class_name": "Nova Scotia duck tolling retriever", "confidence": 0.78, "class_id": 208},
                {"class_name": "kuvasz", "confidence": 0.15, "class_id": 222}
            ],
            "model_used": "resnet50_imagenet",
            "processing_time": 0.389
        },
        {
            "image_filename": "flower_rose.jpg",
            "predictions": [
                {"class_name": "rose", "confidence": 0.91, "class_id": 997},
                {"class_name": "flower", "confidence": 0.87, "class_id": 985},
                {"class_name": "daisy", "confidence": 0.23, "class_id": 986}
            ],
            "model_used": "efficientnet_b0",
            "processing_time": 0.267
        },
        {
            "image_filename": "car_tesla.jpg",
            "predictions": [
                {"class_name": "sports car", "confidence": 0.88, "class_id": 817},
                {"class_name": "convertible", "confidence": 0.76, "class_id": 511},
                {"class_name": "limousine", "confidence": 0.34, "class_id": 627}
            ],
            "model_used": "resnet50_imagenet",
            "processing_time": 0.445
        },
        {
            "image_filename": "food_sushi.jpg",
            "predictions": [
                {"class_name": "sushi", "confidence": 0.93, "class_id": 963},
                {"class_name": "Japanese food", "confidence": 0.89, "class_id": 961},
                {"class_name": "salmon", "confidence": 0.45, "class_id": 332}
            ],
            "model_used": "efficientnet_b0",
            "processing_time": 0.312
        }
    ]
    
    # Create classification records for demo users
    for i, classification in enumerate(sample_classifications):
        # Assign to different users
        user_key = ['demo', 'yamada', 'demo', 'yamada', 'demo'][i % 3]
        user = users[user_key]
        
        # Create classification record
        record = ClassificationRecord(
            user_id=user.id,
            image_filename=classification["image_filename"],
            image_path=f"/uploads/demo/{classification['image_filename']}",
            model_name=classification["model_used"],
            predictions=json.dumps(classification["predictions"]),
            processing_time=int(classification["processing_time"] * 1000),  # Convert to milliseconds
            confidence_score=str(max(pred["confidence"] for pred in classification["predictions"])),
            created_at=datetime.now(timezone.utc) - timedelta(
                days=random.randint(1, 28),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
        )
        
        # Check if record already exists
        existing_record = db.query(ClassificationRecord).filter(
            ClassificationRecord.user_id == user.id,
            ClassificationRecord.image_filename == classification["image_filename"]
        ).first()
        
        if not existing_record:
            db.add(record)
            print(f"Created classification record: {classification['image_filename']} for user {user.username}")
        else:
            print(f"Classification record already exists: {classification['image_filename']}")
    
    db.commit()

def init_demo_data():
    """Initialize demo data for the application."""
    print("Initializing demo data...")
    
    # Create database tables if they don't exist
    create_database()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create demo users
        print("\n=== Creating Demo Users ===")
        users = create_demo_users(db)
        
        # Create sample classification data
        print("\n=== Creating Sample Classification Data ===")
        create_sample_classification_data(db, users)
        
        print("\n=== Demo Data Initialization Complete ===")
        print("\nDemo Accounts Created:")
        print("Regular User  - Username: demo    Password: demo1234")
        print("Admin User    - Username: admin   Password: admin1234") 
        print("Sample User   - Username: yamada  Password: yamada1234")
        print("\nYou can now use these accounts to test the authentication features.")
        
    except Exception as e:
        print(f"Error initializing demo data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_demo_data()