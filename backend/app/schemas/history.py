from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ClassificationPrediction(BaseModel):
    """Single prediction result."""
    class_name: str
    confidence: float
    class_id: Optional[int] = None

class ClassificationHistoryResponse(BaseModel):
    """Classification history record response."""
    id: int
    image_filename: str
    image_path: str
    model_name: str
    predictions: List[ClassificationPrediction]
    processing_time: Optional[int] = Field(None, description="Processing time in milliseconds")
    confidence_score: float = Field(..., description="Highest confidence score")
    created_at: datetime
    
    class Config:
        from_attributes = True

class ClassificationHistoryList(BaseModel):
    """Paginated list of classification history records."""
    items: List[ClassificationHistoryResponse]
    total: int
    skip: int
    limit: int

class ClassificationHistoryFilter(BaseModel):
    """Filter options for classification history."""
    model_name: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_confidence: Optional[float] = Field(None, ge=0, le=1)
    max_confidence: Optional[float] = Field(None, ge=0, le=1)

class ModelUsageStats(BaseModel):
    """Model usage statistics."""
    name: str
    count: int

class ClassificationStats(BaseModel):
    """User classification statistics."""
    total_classifications: int
    monthly_classifications: int
    daily_classifications: int
    average_accuracy: float = Field(..., description="Average accuracy percentage")
    average_processing_time: float = Field(..., description="Average processing time in milliseconds")
    most_used_models: List[ModelUsageStats]

class ClassificationRecordCreate(BaseModel):
    """Create a new classification record."""
    image_filename: str
    image_path: str
    model_name: str
    predictions: List[ClassificationPrediction]
    processing_time: int
    confidence_score: float