from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import os
import shutil
import json
import logging
from pathlib import Path
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User, ClassificationRecord
from app.routers.auth import get_current_user_optional
from app.services.image_service import ImageService
from app.services.classification_service import ClassificationService
from app.services.security_service import security_service
from app.schemas.classification import (
    ClassificationResponse,
    ClassificationRequest,
    ImageMetadata
)

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize services
logger.info("Initializing image service...")
image_service = ImageService()
logger.info("Initializing classification service...")
classification_service = ClassificationService()
logger.info("Services initialized successfully")

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
    print(f"\n=== CLASSIFICATION REQUEST STARTED ===")
    print(f"File: {file.filename}")
    print(f"User: {current_user.id if current_user and hasattr(current_user, 'id') else 'Anonymous'}")
    
    try:
        # Read file content for validation
        content = await file.read()
        
        # Reset file pointer for subsequent reads
        await file.seek(0)
        
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
        
        # Save file (using content we already read)
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Collect image metadata
        from PIL import Image as PILImage
        with PILImage.open(file_path) as img:
            image_metadata = {
                "filename": file.filename,
                "size": file_size,
                "format": img.format,
                "dimensions": [img.width, img.height],
                "width": img.width,
                "height": img.height,
                "has_transparency": img.mode in ('RGBA', 'LA') or 'transparency' in img.info
            }
        logger.info(f"Image metadata collected: {image_metadata}")
        
        # Process image
        logger.info("Processing image...")
        processed_image = await image_service.process_image(file_path)
        logger.info(f"Image processed successfully. Shape: {processed_image.shape}")
        
        # Classify image - let service use default model selection
        # This will use the DEFAULT_MODEL setting or auto-select best available
        logger.info("Starting classification...")
        logger.info(f"Available models: {list(classification_service.models.keys())}")
        logger.info(f"Using model: {classification_service.get_default_model()}")
        
        results = await classification_service.classify(
            processed_image, 
            model_name=None,  # Use default model selection
            confidence_threshold=0.01,  # Low threshold to show results
            use_cache=False  # Disable cache to test fix
        )
        logger.info("Classification completed")
        
        # Debug logging
        logger.info(f"Classification service returned: {results}")
        logger.info(f"Raw predictions: {results.get('predictions', [])}")
        logger.info(f"Model used: {results.get('model_used', 'unknown')}")
        
        logger.debug("Starting response preparation...")
        
        # Extract predictions and confidence scores from service response
        from app.schemas.classification import Prediction
        
        predictions_list = []
        confidence_scores_dict = {}
        
        logger.info(f"Processing {len(results.get('predictions', []))} predictions")
        
        # Handle the prediction format from classification service
        for i, pred_obj in enumerate(results.get("predictions", [])):
            logger.debug(f"Processing prediction {i}: {pred_obj}")
            if isinstance(pred_obj, dict):
                class_name = pred_obj.get("class_name", "unknown")
                confidence = pred_obj.get("confidence", 0.0)
                class_id = pred_obj.get("class_id", str(i))
                
                # Create Prediction object for schema compliance
                prediction = Prediction(
                    class_name=class_name,
                    confidence=confidence,
                    class_id=class_id
                )
                predictions_list.append(prediction)
                confidence_scores_dict[class_name] = confidence
                logger.debug(f"Added: {class_name} = {confidence}")
            else:
                # Fallback for unexpected format
                prediction = Prediction(
                    class_name=str(pred_obj),
                    confidence=0.0,
                    class_id=str(i)
                )
                predictions_list.append(prediction)
                logger.debug(f"Fallback for: {pred_obj}")
        
        logger.info(f"Generated {len(predictions_list)} prediction objects")
        logger.debug(f"Confidence scores: {confidence_scores_dict}")
        
        # Save to history if user is authenticated
        if current_user:
            logger.info("Saving to history for authenticated user...")
            try:
                # Get the highest confidence score
                max_confidence = max(confidence_scores_dict.values()) if confidence_scores_dict else 0.0
                
                # Prepare predictions for storage (use original format from service)
                predictions_data = results.get("predictions", [])
                
                logger.debug(f"Creating history record with max_confidence: {max_confidence}")
                
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
                logger.info("History record saved successfully")
            except Exception as e:
                logger.error(f"Error saving history: {e}")
                import traceback
                traceback.print_exc()
        else:
            logger.debug("No user authenticated, skipping history save")
        
        logger.debug("Creating response object...")
        try:
            # Create ImageMetadata object
            metadata_obj = ImageMetadata(**image_metadata)
            
            response = ClassificationResponse(
                id=file_id,
                filename=file.filename,
                predictions=predictions_list,
                confidence_scores=confidence_scores_dict,
                processing_time=results["processing_time"],
                model_used=results["model_used"],
                timestamp=datetime.utcnow(),
                image_url=f"/uploads/{filename}",
                image_metadata=metadata_obj
            )
            logger.info(f"Classification successful: {len(predictions_list)} predictions, processing time: {results['processing_time']:.2f}s")
            return response
        except Exception as e:
            logger.error(f"Error creating response: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    except Exception as e:
        # Clean up uploaded file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
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