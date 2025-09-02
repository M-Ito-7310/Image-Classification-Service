from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class ClassificationRequest(BaseModel):
    """Request model for image classification."""
    model_config = {"protected_namespaces": ()}
    
    model_name: Optional[str] = Field(default=None, description="Model to use for classification")
    confidence_threshold: Optional[float] = Field(default=0.5, description="Minimum confidence threshold")
    max_results: Optional[int] = Field(default=5, description="Maximum number of results to return")

class Prediction(BaseModel):
    """Individual prediction result."""
    class_name: str = Field(description="Predicted class name")
    confidence: float = Field(description="Confidence score (0.0 to 1.0)")
    class_id: Optional[str] = Field(default=None, description="Class identifier")

class ClassificationResponse(BaseModel):
    """Response model for image classification."""
    model_config = {"protected_namespaces": ()}
    
    id: str = Field(description="Unique identifier for this classification")
    filename: str = Field(description="Original filename")
    predictions: List[Prediction] = Field(description="Classification predictions")
    confidence_scores: Dict[str, float] = Field(description="Raw confidence scores")
    processing_time: float = Field(description="Processing time in seconds")
    model_used: str = Field(description="Model used for classification")
    timestamp: datetime = Field(description="Classification timestamp")
    image_url: Optional[str] = Field(default=None, description="URL to access the uploaded image")

class BatchClassificationResponse(BaseModel):
    """Response model for batch image classification."""
    batch_id: str = Field(description="Unique identifier for this batch")
    total_files: int = Field(description="Total number of files in batch")
    successful_classifications: int = Field(description="Number of successful classifications")
    failed_classifications: int = Field(description="Number of failed classifications")
    results: List[ClassificationResponse] = Field(description="Successful classification results")
    errors: List[Dict[str, Any]] = Field(description="Error details for failed classifications")
    timestamp: datetime = Field(description="Batch processing timestamp")

class ModelInfo(BaseModel):
    """Information about a classification model."""
    name: str = Field(description="Model name")
    description: str = Field(description="Model description")
    version: str = Field(description="Model version")
    classes: List[str] = Field(description="List of classes the model can predict")
    accuracy: Optional[float] = Field(default=None, description="Model accuracy on test set")
    size: Optional[str] = Field(default=None, description="Model size")

class HistoryResponse(BaseModel):
    """Response model for classification history."""
    total_count: int = Field(description="Total number of classifications")
    results: List[ClassificationResponse] = Field(description="Classification history")
    has_next: bool = Field(description="Whether there are more results available")
    page: int = Field(description="Current page number")

class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str = Field(description="Error message")
    status_code: int = Field(description="HTTP status code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Configuration schemas
class UploadConfig(BaseModel):
    """Upload configuration."""
    max_file_size: int = Field(description="Maximum file size in bytes")
    allowed_extensions: List[str] = Field(description="Allowed file extensions")
    max_batch_size: int = Field(description="Maximum number of files in a batch")

class CustomModelRequest(BaseModel):
    """Request model for custom model upload."""
    name: str = Field(description="Custom model name")
    description: Optional[str] = Field(default=None, description="Model description")
    model_type: str = Field(description="Model type (tensorflow/pytorch)")
    classes: List[str] = Field(description="List of classes the model can predict")

class CustomModelResponse(BaseModel):
    """Response model for custom model upload."""
    model_id: str = Field(description="Unique model identifier")
    name: str = Field(description="Model name")
    status: str = Field(description="Upload and validation status")
    file_size: int = Field(description="Model file size in bytes")
    upload_timestamp: datetime = Field(description="Upload timestamp")

class APIInfo(BaseModel):
    """API information model."""
    name: str = Field(description="API name")
    version: str = Field(description="API version")
    description: str = Field(description="API description")
    upload_config: UploadConfig = Field(description="Upload configuration")
    available_models: List[str] = Field(description="Available models")