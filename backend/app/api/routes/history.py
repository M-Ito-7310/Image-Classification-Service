from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta
import json

from app.core.database import get_db
from app.models.user import User, ClassificationRecord
from app.routers.auth import get_current_user
from app.schemas.history import (
    ClassificationHistoryResponse,
    ClassificationHistoryList,
    ClassificationStats,
    ClassificationHistoryFilter
)

router = APIRouter()

@router.get("/history", response_model=ClassificationHistoryList)
async def get_classification_history(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    model_name: Optional[str] = Query(None, description="Filter by model name"),
    date_from: Optional[datetime] = Query(None, description="Filter from date"),
    date_to: Optional[datetime] = Query(None, description="Filter to date"),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get classification history for the current user."""
    query = db.query(ClassificationRecord)
    
    # Filter by user if authenticated
    if current_user:
        query = query.filter(ClassificationRecord.user_id == current_user.id)
    else:
        # For anonymous users, return empty list or public records only
        return ClassificationHistoryList(items=[], total=0, skip=skip, limit=limit)
    
    # Apply filters
    if model_name:
        query = query.filter(ClassificationRecord.model_name == model_name)
    
    if date_from:
        query = query.filter(ClassificationRecord.created_at >= date_from)
    
    if date_to:
        query = query.filter(ClassificationRecord.created_at <= date_to)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    records = query.order_by(desc(ClassificationRecord.created_at))\
                  .offset(skip)\
                  .limit(limit)\
                  .all()
    
    # Convert records to response format
    items = []
    for record in records:
        try:
            predictions = json.loads(record.predictions) if record.predictions else []
        except:
            predictions = []
            
        items.append(ClassificationHistoryResponse(
            id=record.id,
            image_filename=record.image_filename,
            image_path=record.image_path,
            model_name=record.model_name,
            predictions=predictions,
            processing_time=record.processing_time,
            confidence_score=float(record.confidence_score) if record.confidence_score else 0.0,
            created_at=record.created_at
        ))
    
    return ClassificationHistoryList(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/history/{record_id}", response_model=ClassificationHistoryResponse)
async def get_classification_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific classification record."""
    record = db.query(ClassificationRecord).filter(
        ClassificationRecord.id == record_id,
        ClassificationRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classification record not found"
        )
    
    try:
        predictions = json.loads(record.predictions) if record.predictions else []
    except:
        predictions = []
    
    return ClassificationHistoryResponse(
        id=record.id,
        image_filename=record.image_filename,
        image_path=record.image_path,
        model_name=record.model_name,
        predictions=predictions,
        processing_time=record.processing_time,
        confidence_score=float(record.confidence_score) if record.confidence_score else 0.0,
        created_at=record.created_at
    )

@router.delete("/history/{record_id}")
async def delete_classification_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a classification record."""
    record = db.query(ClassificationRecord).filter(
        ClassificationRecord.id == record_id,
        ClassificationRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Classification record not found"
        )
    
    db.delete(record)
    db.commit()
    
    return {"message": "Classification record deleted successfully"}

@router.get("/stats", response_model=ClassificationStats)
async def get_classification_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get classification statistics for the current user."""
    # Total classifications
    total_classifications = db.query(ClassificationRecord).filter(
        ClassificationRecord.user_id == current_user.id
    ).count()
    
    # This month's classifications
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_classifications = db.query(ClassificationRecord).filter(
        ClassificationRecord.user_id == current_user.id,
        ClassificationRecord.created_at >= start_of_month
    ).count()
    
    # Today's classifications
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    daily_classifications = db.query(ClassificationRecord).filter(
        ClassificationRecord.user_id == current_user.id,
        ClassificationRecord.created_at >= start_of_day
    ).count()
    
    # Calculate average accuracy (confidence score)
    records = db.query(ClassificationRecord).filter(
        ClassificationRecord.user_id == current_user.id
    ).all()
    
    if records:
        total_confidence = sum(float(r.confidence_score) for r in records if r.confidence_score)
        average_accuracy = (total_confidence / len(records)) * 100 if records else 0
        
        # Calculate average processing time
        total_time = sum(r.processing_time for r in records if r.processing_time)
        average_processing_time = total_time / len(records) if records else 0
    else:
        average_accuracy = 0
        average_processing_time = 0
    
    # Get most used models
    model_counts = {}
    for record in records:
        model_name = record.model_name
        if model_name in model_counts:
            model_counts[model_name] += 1
        else:
            model_counts[model_name] = 1
    
    most_used_models = sorted(
        [{"name": k, "count": v} for k, v in model_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:5]
    
    return ClassificationStats(
        total_classifications=total_classifications,
        monthly_classifications=monthly_classifications,
        daily_classifications=daily_classifications,
        average_accuracy=round(average_accuracy, 2),
        average_processing_time=round(average_processing_time, 2),
        most_used_models=most_used_models
    )

@router.post("/history/bulk-delete")
async def bulk_delete_classification_records(
    record_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete multiple classification records."""
    deleted_count = db.query(ClassificationRecord).filter(
        ClassificationRecord.id.in_(record_ids),
        ClassificationRecord.user_id == current_user.id
    ).delete(synchronize_session=False)
    
    db.commit()
    
    return {
        "message": f"{deleted_count} classification records deleted successfully",
        "deleted_count": deleted_count
    }