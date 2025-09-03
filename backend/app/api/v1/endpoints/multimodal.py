"""
Multi-modal classification API endpoints for video and audio files.
"""

import os
import tempfile
from typing import Dict, Any, Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, status, Form, BackgroundTasks
from fastapi.responses import JSONResponse

from app.services.multimodal_service import multimodal_service
from app.services.security_service import FileSecurityService
from app.core.config import settings

router = APIRouter()

# Supported file types
SUPPORTED_VIDEO_TYPES = {
    "video/mp4": [".mp4"],
    "video/avi": [".avi"],
    "video/mov": [".mov"],
    "video/mkv": [".mkv"],
    "video/webm": [".webm"]
}

SUPPORTED_AUDIO_TYPES = {
    "audio/wav": [".wav"],
    "audio/mp3": [".mp3"],
    "audio/m4a": [".m4a"],
    "audio/flac": [".flac"],
    "audio/ogg": [".ogg"]
}

@router.post("/classify/video")
async def classify_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    extract_frames: int = Form(5),
    extract_audio: bool = Form(True),
    model_name: str = Form("imagenet_mobilenet_v2")
) -> Dict[str, Any]:
    """
    Classify video file by extracting and analyzing frames and audio.
    
    Args:
        file: Video file to classify
        extract_frames: Number of frames to extract (default: 5)
        extract_audio: Whether to extract and classify audio (default: True)
        model_name: AI model to use for frame classification
    
    Returns:
        Video classification results with frame and audio analysis
    """
    
    # Validate file type
    if file.content_type not in SUPPORTED_VIDEO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported video format. Supported formats: {list(SUPPORTED_VIDEO_TYPES.keys())}"
        )
    
    # Validate parameters
    if extract_frames < 1 or extract_frames > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="extract_frames must be between 1 and 20"
        )
    
    temp_file_path = None
    
    try:
        # Save uploaded file temporarily
        file_content = await file.read()
        
        # Security validation
        security_service = FileSecurityService()
        security_result = await security_service.validate_file_upload(
            file_content, file.filename or "video"
        )
        
        if not security_result["is_safe"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File security validation failed: {security_result['reason']}"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        # Initialize multi-modal service
        await multimodal_service.initialize()
        
        # Classify video
        classification_result = await multimodal_service.classify_video(
            video_file_path=temp_file_path,
            extract_frames=extract_frames,
            extract_audio=extract_audio
        )
        
        # Add request metadata
        classification_result["request_info"] = {
            "filename": file.filename,
            "file_size": len(file_content),
            "content_type": file.content_type,
            "model_used": model_name,
            "extract_frames": extract_frames,
            "extract_audio": extract_audio
        }
        
        # Schedule cleanup
        if temp_file_path:
            background_tasks.add_task(cleanup_temp_file, temp_file_path)
        
        return classification_result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        if temp_file_path:
            cleanup_temp_file(temp_file_path)
        raise
        
    except Exception as e:
        if temp_file_path:
            cleanup_temp_file(temp_file_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Video classification failed: {str(e)}"
        )

@router.post("/classify/audio")
async def classify_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    model_name: str = Form("wav2vec2")
) -> Dict[str, Any]:
    """
    Classify audio file content and extract features.
    
    Args:
        file: Audio file to classify
        model_name: Audio model to use for classification
    
    Returns:
        Audio classification results with features
    """
    
    # Validate file type
    if file.content_type not in SUPPORTED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported audio format. Supported formats: {list(SUPPORTED_AUDIO_TYPES.keys())}"
        )
    
    temp_file_path = None
    
    try:
        # Save uploaded file temporarily
        file_content = await file.read()
        
        # Security validation
        security_service = FileSecurityService()
        security_result = await security_service.validate_file_upload(
            file_content, file.filename or "audio"
        )
        
        if not security_result["is_safe"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File security validation failed: {security_result['reason']}"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        # Initialize multi-modal service
        await multimodal_service.initialize()
        
        # Classify audio
        classification_result = await multimodal_service.classify_audio(temp_file_path)
        
        # Add request metadata
        classification_result["request_info"] = {
            "filename": file.filename,
            "file_size": len(file_content),
            "content_type": file.content_type,
            "model_used": model_name
        }
        
        # Schedule cleanup
        if temp_file_path:
            background_tasks.add_task(cleanup_temp_file, temp_file_path)
        
        return classification_result
        
    except HTTPException:
        # Re-raise HTTP exceptions
        if temp_file_path:
            cleanup_temp_file(temp_file_path)
        raise
        
    except Exception as e:
        if temp_file_path:
            cleanup_temp_file(temp_file_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audio classification failed: {str(e)}"
        )

@router.get("/models/video")
async def get_video_models() -> Dict[str, Any]:
    """
    Get available models for video classification.
    
    Returns:
        Available video classification models
    """
    
    return {
        "available_models": [
            {
                "name": "imagenet_mobilenet_v2",
                "description": "MobileNet v2 trained on ImageNet for frame classification",
                "type": "image_classification",
                "input_size": [224, 224],
                "classes": 1000
            },
            {
                "name": "imagenet_resnet50",
                "description": "ResNet50 trained on ImageNet for frame classification",
                "type": "image_classification", 
                "input_size": [224, 224],
                "classes": 1000
            }
        ],
        "supported_formats": list(SUPPORTED_VIDEO_TYPES.keys()),
        "max_file_size_mb": settings.MAX_FILE_SIZE / 1024 / 1024,
        "max_extract_frames": 20,
        "features": [
            "Frame extraction and classification",
            "Audio extraction and analysis",
            "Temporal analysis",
            "Scene change detection",
            "Object frequency analysis"
        ]
    }

@router.get("/models/audio")
async def get_audio_models() -> Dict[str, Any]:
    """
    Get available models for audio classification.
    
    Returns:
        Available audio classification models
    """
    
    return {
        "available_models": [
            {
                "name": "wav2vec2",
                "description": "Wav2Vec2 model for audio classification",
                "type": "audio_classification",
                "sample_rate": 16000,
                "max_duration": 300
            }
        ],
        "supported_formats": list(SUPPORTED_AUDIO_TYPES.keys()),
        "max_file_size_mb": settings.MAX_FILE_SIZE / 1024 / 1024,
        "features": [
            "Audio content classification",
            "Spectral feature extraction",
            "Tempo detection",
            "Energy analysis",
            "Harmonic analysis"
        ]
    }

@router.post("/validate/video")
async def validate_video_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Validate video file without processing.
    
    Args:
        file: Video file to validate
    
    Returns:
        Validation results and metadata
    """
    
    temp_file_path = None
    
    try:
        # Save uploaded file temporarily
        file_content = await file.read()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        # Import video processor
        from app.services.multimodal_service import VideoProcessor
        
        # Validate video
        validation_result = VideoProcessor.validate_video_file(temp_file_path)
        
        # Add file info
        validation_result["file_info"] = {
            "filename": file.filename,
            "file_size": len(file_content),
            "content_type": file.content_type
        }
        
        return validation_result
        
    except Exception as e:
        return {
            "is_valid": False,
            "error": f"Validation failed: {str(e)}",
            "file_info": {
                "filename": file.filename,
                "content_type": file.content_type
            }
        }
        
    finally:
        if temp_file_path:
            cleanup_temp_file(temp_file_path)

@router.post("/validate/audio")
async def validate_audio_file(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Validate audio file without processing.
    
    Args:
        file: Audio file to validate
    
    Returns:
        Validation results and metadata
    """
    
    temp_file_path = None
    
    try:
        # Save uploaded file temporarily
        file_content = await file.read()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        # Import audio processor
        from app.services.multimodal_service import AudioProcessor
        
        # Validate audio
        validation_result = AudioProcessor.validate_audio_file(temp_file_path)
        
        # Add file info
        validation_result["file_info"] = {
            "filename": file.filename,
            "file_size": len(file_content),
            "content_type": file.content_type
        }
        
        return validation_result
        
    except Exception as e:
        return {
            "is_valid": False,
            "error": f"Validation failed: {str(e)}",
            "file_info": {
                "filename": file.filename,
                "content_type": file.content_type
            }
        }
        
    finally:
        if temp_file_path:
            cleanup_temp_file(temp_file_path)

@router.get("/capabilities")
async def get_multimodal_capabilities() -> Dict[str, Any]:
    """
    Get multi-modal service capabilities and status.
    
    Returns:
        Service capabilities and initialization status
    """
    
    try:
        # Check initialization status
        await multimodal_service.initialize()
        
        return {
            "status": "available",
            "initialized": multimodal_service.initialized,
            "supported_media_types": {
                "video": {
                    "formats": list(SUPPORTED_VIDEO_TYPES.keys()),
                    "max_extract_frames": 20,
                    "features": [
                        "Frame extraction",
                        "Object detection per frame", 
                        "Scene change detection",
                        "Temporal analysis",
                        "Audio extraction"
                    ]
                },
                "audio": {
                    "formats": list(SUPPORTED_AUDIO_TYPES.keys()),
                    "max_duration": 300,
                    "features": [
                        "Content classification",
                        "Spectral analysis",
                        "Tempo detection",
                        "Energy analysis",
                        "Feature extraction"
                    ]
                }
            },
            "models": {
                "video_frame_classification": ["imagenet_mobilenet_v2", "imagenet_resnet50"],
                "audio_classification": ["wav2vec2"]
            },
            "limitations": {
                "max_file_size_mb": settings.MAX_FILE_SIZE / 1024 / 1024,
                "max_video_duration": 600,  # 10 minutes
                "max_audio_duration": 300,   # 5 minutes
                "concurrent_processing": 3
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "initialized": False,
            "error": str(e),
            "message": "Multi-modal service initialization failed"
        }

def cleanup_temp_file(file_path: str):
    """Clean up temporary file."""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception:
        pass  # Silent cleanup failure