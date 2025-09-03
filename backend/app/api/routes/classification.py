from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import os
import shutil
import json
from pathlib import Path
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User, ClassificationRecord
from app.utils.auth import get_current_user_optional
from app.services.image_service import ImageService
from app.services.classification_service import ClassificationService
from app.services.security_service import security_service
from app.schemas.classification import (
    ClassificationResponse,
    ClassificationRequest,
    BatchClassificationResponse
)

router = APIRouter()

# Initialize services
image_service = ImageService()
classification_service = ClassificationService()

@router.post("/classify", response_model=ClassificationResponse)
async def classify_image(
    file: UploadFile = File(..., description="Image file to classify"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
) -> ClassificationResponse:
    """
    Classify a single uploaded image.
    
    Args:
        file: Uploaded image file
        
    Returns:
        Classification results with confidence scores
    """
    try:
        # Read file content for validation
        content = await file.read()
        
        # Comprehensive security validation
        validation_result = await security_service.validate_file_upload(
            content, 
            file.filename or "unknown.jpg"
        )
        
        if not validation_result["valid"]:
            # Log security incident
            logger.warning(f"File upload blocked: {file.filename} - Errors: {validation_result['errors']}")
            
            # Quarantine suspicious files
            if validation_result["security_score"] < 30:
                await security_service.quarantine_suspicious_file(
                    content, 
                    file.filename or "unknown.jpg",
                    validation_result
                )
            
            raise HTTPException(
                status_code=400,
                detail=f"File validation failed: {'; '.join(validation_result['errors'])}"
            )
        
        # Log warnings for monitoring
        if validation_result["warnings"]:
            logger.warning(f"File upload warnings for {file.filename}: {validation_result['warnings']}")
        
        file_size = len(content)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in settings.ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File extension {file_extension} not allowed"
            )
        
        filename = f"{file_id}{file_extension}"
        file_path = Path(settings.UPLOAD_DIR) / filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process image
        processed_image = await image_service.process_image(file_path)
        
        # Classify image (check if it's a custom model first)
        model_name = "default"  # You can extend this to accept model parameter
        
        # If user has custom models, they might want to use them
        # This is a simple implementation - you can make it more sophisticated
        results = await classification_service.classify(
            processed_image, 
            model_name=model_name
        )
        
        # Save to history if user is authenticated
        if current_user:
            # Get the highest confidence score
            max_confidence = max(results["confidence_scores"]) if results["confidence_scores"] else 0.0
            
            # Prepare predictions for storage
            predictions_data = []
            for pred, conf in zip(results["predictions"], results["confidence_scores"]):
                predictions_data.append({
                    "class_name": pred,
                    "confidence": conf
                })
            
            # Create history record
            history_record = ClassificationRecord(
                user_id=current_user.id,
                image_filename=file.filename,
                image_path=str(file_path),
                model_name=results["model_used"],
                predictions=json.dumps(predictions_data),
                processing_time=results["processing_time"],
                confidence_score=str(max_confidence)
            )
            
            db.add(history_record)
            db.commit()
            db.refresh(history_record)
        
        return ClassificationResponse(
            id=file_id,
            filename=file.filename,
            predictions=results["predictions"],
            confidence_scores=results["confidence_scores"],
            processing_time=results["processing_time"],
            model_used=results["model_used"],
            timestamp=datetime.utcnow(),
            image_url=f"/uploads/{filename}"
        )
        
    except Exception as e:
        # Clean up uploaded file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )

@router.post("/classify/batch", response_model=BatchClassificationResponse)
async def classify_images_batch(
    files: List[UploadFile] = File(..., description="Multiple image files to classify")
) -> BatchClassificationResponse:
    """
    Classify multiple uploaded images in batch.
    
    Args:
        files: List of uploaded image files
        
    Returns:
        Batch classification results
    """
    if len(files) > 10:  # Limit batch size
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 files allowed per batch"
        )
    
    batch_id = str(uuid.uuid4())
    results = []
    errors = []
    
    for file in files:
        try:
            # Classify each file individually
            result = await classify_image(file)
            results.append(result)
        except HTTPException as e:
            errors.append({
                "filename": file.filename,
                "error": e.detail,
                "status_code": e.status_code
            })
    
    return BatchClassificationResponse(
        batch_id=batch_id,
        total_files=len(files),
        successful_classifications=len(results),
        failed_classifications=len(errors),
        results=results,
        errors=errors,
        timestamp=datetime.utcnow()
    )

@router.get("/models")
async def list_available_models() -> Dict[str, Any]:
    """
    List all available classification models.
    """
    models_list = await classification_service.list_models()
    
    # Transform to expected format with status field
    available_models = []
    for model in models_list:
        available_models.append({
            "name": model["name"],
            "description": model["description"], 
            "version": model.get("version", "1.0"),
            "classes": len(model.get("classes", [])) if isinstance(model.get("classes"), list) else 1000,
            "status": "active",
            "accuracy": model.get("accuracy"),
            "inference_time": model.get("inference_time", 50),
            "provider": model.get("provider", "tensorflow")
        })
    
    return {
        "available_models": available_models,
        "default_model": settings.DEFAULT_MODEL
    }

@router.get("/history")
async def get_classification_history(
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """
    Get classification history.
    
    Args:
        limit: Number of records to return
        offset: Number of records to skip
        
    Returns:
        Classification history
    """
    # TODO: Implement database storage and retrieval
    return {
        "message": "Classification history feature coming soon",
        "limit": limit,
        "offset": offset
    }

@router.delete("/uploads/{file_id}")
async def delete_uploaded_file(file_id: str) -> Dict[str, str]:
    """
    Delete an uploaded file.
    
    Args:
        file_id: File ID to delete
        
    Returns:
        Deletion confirmation
    """
    # Find file with this ID
    upload_dir = Path(settings.UPLOAD_DIR)
    for file_path in upload_dir.glob(f"{file_id}.*"):
        try:
            os.remove(file_path)
            return {"message": f"File {file_id} deleted successfully"}
        except OSError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete file: {str(e)}"
            )
    
    raise HTTPException(
        status_code=404,
        detail=f"File with ID {file_id} not found"
    )