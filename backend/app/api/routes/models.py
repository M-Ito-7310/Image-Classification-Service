from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import os
import json
from pathlib import Path
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User, CustomModel
from app.routers.auth import get_current_user
from app.schemas.classification import (
    CustomModelRequest,
    CustomModelResponse,
    ModelInfo
)

router = APIRouter()

@router.get("/")
async def get_available_models() -> Dict[str, Any]:
    """
    Get list of available models for classification.
    Public endpoint - no authentication required.
    
    Returns:
        List of available models with their information
    """
    available_models = [
        {
            "name": "mobilenet_v2",
            "description": "Fast and efficient model for general image classification",
            "version": "1.0",
            "classes": 1000,
            "status": "active",
            "accuracy": 0.72,
            "inference_time": 50,
            "provider": "tensorflow"
        },
        {
            "name": "resnet18", 
            "description": "Lightweight ResNet model for image classification",
            "version": "1.0",
            "classes": 1000,
            "status": "active", 
            "accuracy": 0.70,
            "inference_time": 45,
            "provider": "pytorch"
        },
        {
            "name": "efficientnet_b0",
            "description": "Balanced model with good accuracy and efficiency", 
            "version": "1.0",
            "classes": 1000,
            "status": "active",
            "accuracy": 0.77,
            "inference_time": 80,
            "provider": "tensorflow"
        }
    ]
    
    return {
        "available_models": available_models,
        "default_model": "mobilenet_v2"
    }

@router.post("/upload", response_model=CustomModelResponse)
async def upload_custom_model(
    file: UploadFile = File(..., description="Custom model file"),
    name: str = Form(..., description="Model name"),
    description: Optional[str] = Form(None, description="Model description"),
    model_type: str = Form(..., description="Model type (tensorflow/pytorch)"),
    classes: str = Form(..., description="JSON string of class names"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> CustomModelResponse:
    """
    Upload a custom trained model.
    
    Args:
        file: Model file (.h5 for TensorFlow, .pth for PyTorch)
        name: Model name
        description: Optional model description
        model_type: tensorflow or pytorch
        classes: JSON string of class names
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Upload confirmation with model ID
    """
    try:
        # Validate model type
        if model_type not in ['tensorflow', 'pytorch']:
            raise HTTPException(
                status_code=400,
                detail="Model type must be 'tensorflow' or 'pytorch'"
            )
        
        # Validate file extension based on model type
        file_extension = Path(file.filename).suffix.lower()
        expected_extensions = {
            'tensorflow': ['.h5', '.hdf5', '.pb'],
            'pytorch': ['.pth', '.pt']
        }
        
        if file_extension not in expected_extensions[model_type]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file extension {file_extension} for {model_type} model. "
                       f"Expected: {expected_extensions[model_type]}"
            )
        
        # Validate classes JSON
        try:
            class_list = json.loads(classes)
            if not isinstance(class_list, list) or len(class_list) == 0:
                raise ValueError("Classes must be a non-empty list")
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid classes format: {str(e)}"
            )
        
        # Check file size
        content = await file.read()
        file_size = len(content)
        
        # Custom models can be larger than regular uploads
        max_model_size = 500 * 1024 * 1024  # 500MB
        if file_size > max_model_size:
            raise HTTPException(
                status_code=400,
                detail=f"Model file size {file_size} exceeds maximum allowed size {max_model_size}"
            )
        
        # Generate unique model ID and file path
        model_id = str(uuid.uuid4())
        filename = f"{model_id}_{name.replace(' ', '_')}{file_extension}"
        
        # Ensure models directory exists
        models_dir = Path(settings.UPLOAD_DIR) / "custom_models"
        models_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = models_dir / filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Create database record
        custom_model = CustomModel(
            user_id=current_user.id,
            model_id=model_id,
            name=name,
            description=description,
            model_type=model_type,
            file_path=str(file_path),
            file_size=file_size,
            classes=classes,
            status='uploaded'
        )
        
        db.add(custom_model)
        db.commit()
        db.refresh(custom_model)
        
        # TODO: Add model validation in background task
        
        return CustomModelResponse(
            model_id=model_id,
            name=name,
            status='uploaded',
            file_size=file_size,
            upload_timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        # Clean up uploaded file if it exists
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Model upload failed: {str(e)}"
        )

@router.get("/custom", response_model=List[Dict[str, Any]])
async def list_custom_models(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    List user's custom models.
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of user's custom models
    """
    custom_models = db.query(CustomModel).filter(
        CustomModel.user_id == current_user.id
    ).all()
    
    models_list = []
    for model in custom_models:
        classes_list = json.loads(model.classes)
        models_list.append({
            'model_id': model.model_id,
            'name': model.name,
            'description': model.description,
            'model_type': model.model_type,
            'classes': classes_list,
            'status': model.status,
            'file_size': model.file_size,
            'created_at': model.created_at.isoformat(),
            'validation_error': model.validation_error
        })
    
    return models_list

@router.delete("/{model_id}")
async def delete_custom_model(
    model_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Delete a custom model.
    
    Args:
        model_id: Custom model ID
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Deletion confirmation
    """
    # Find the model
    custom_model = db.query(CustomModel).filter(
        CustomModel.model_id == model_id,
        CustomModel.user_id == current_user.id
    ).first()
    
    if not custom_model:
        raise HTTPException(
            status_code=404,
            detail="Custom model not found"
        )
    
    # Delete file
    try:
        if os.path.exists(custom_model.file_path):
            os.remove(custom_model.file_path)
    except OSError as e:
        # Log error but don't fail the deletion
        print(f"Warning: Could not delete model file: {e}")
    
    # Delete from database
    db.delete(custom_model)
    db.commit()
    
    return {"message": f"Custom model {model_id} deleted successfully"}

@router.post("/{model_id}/validate")
async def validate_custom_model(
    model_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Validate and activate a custom model.
    
    Args:
        model_id: Custom model ID
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Validation results
    """
    # Find the model
    custom_model = db.query(CustomModel).filter(
        CustomModel.model_id == model_id,
        CustomModel.user_id == current_user.id
    ).first()
    
    if not custom_model:
        raise HTTPException(
            status_code=404,
            detail="Custom model not found"
        )
    
    try:
        # Validate model based on type
        if custom_model.model_type == 'tensorflow':
            validation_result = await _validate_tensorflow_model(custom_model.file_path)
        elif custom_model.model_type == 'pytorch':
            validation_result = await _validate_pytorch_model(custom_model.file_path)
        else:
            raise ValueError(f"Unsupported model type: {custom_model.model_type}")
        
        if validation_result['valid']:
            custom_model.status = 'active'
            custom_model.validation_error = None
        else:
            custom_model.status = 'error'
            custom_model.validation_error = validation_result['error']
        
        custom_model.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            'model_id': model_id,
            'status': custom_model.status,
            'validation_result': validation_result
        }
        
    except Exception as e:
        custom_model.status = 'error'
        custom_model.validation_error = str(e)
        db.commit()
        
        raise HTTPException(
            status_code=500,
            detail=f"Model validation failed: {str(e)}"
        )

async def _validate_tensorflow_model(file_path: str) -> Dict[str, Any]:
    """Validate a TensorFlow model file."""
    try:
        import tensorflow as tf
        
        # Try to load the model
        model = tf.keras.models.load_model(file_path)
        
        # Get model info
        input_shape = model.input_shape
        output_shape = model.output_shape
        
        return {
            'valid': True,
            'input_shape': input_shape,
            'output_shape': output_shape,
            'model_summary': str(model.summary())
        }
        
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

async def _validate_pytorch_model(file_path: str) -> Dict[str, Any]:
    """Validate a PyTorch model file."""
    try:
        import torch
        
        # Try to load the model
        model = torch.load(file_path, map_location='cpu')
        
        # Basic validation
        if hasattr(model, 'eval'):
            model.eval()
            model_info = {
                'valid': True,
                'type': type(model).__name__,
                'parameters': sum(p.numel() for p in model.parameters()) if hasattr(model, 'parameters') else 'unknown'
            }
        else:
            model_info = {
                'valid': True,
                'type': 'state_dict',
                'note': 'Model appears to be a state dictionary'
            }
        
        return model_info
        
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }