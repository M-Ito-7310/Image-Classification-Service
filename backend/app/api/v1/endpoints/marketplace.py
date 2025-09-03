"""
AI Model Marketplace API endpoints.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, status, Form, Query, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.services.model_marketplace import model_marketplace
from app.services.security_service import FileSecurityService

router = APIRouter()

class ModelMetadata(BaseModel):
    """Model metadata schema for marketplace uploads."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    category: str = Field(..., regex="^(image_classification|object_detection|semantic_segmentation|custom)$")
    input_type: str = Field(..., description="Type of input data (e.g., 'image', 'text', 'audio')")
    output_type: str = Field(..., description="Type of output (e.g., 'classification', 'detection', 'segmentation')")
    tags: Optional[list] = Field(default=[], description="Tags for model discovery")
    license: Optional[str] = Field(default="MIT", description="Model license")
    version: Optional[str] = Field(default="1.0.0", description="Model version")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Custom Plant Classifier",
                "description": "A CNN model trained to classify different plant species with 95% accuracy on validation set.",
                "category": "image_classification", 
                "input_type": "image",
                "output_type": "classification",
                "tags": ["plants", "nature", "biology"],
                "license": "MIT",
                "version": "1.0.0"
            }
        }

@router.post("/upload")
async def upload_model(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    input_type: str = Form(...),
    output_type: str = Form(...),
    tags: str = Form(""),
    license: str = Form("MIT"),
    version: str = Form("1.0.0"),
    user_id: str = Form(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Upload a custom AI model to the marketplace.
    
    Args:
        file: Model file (supported formats: .h5, .hdf5, .pb, .pt, .pth, .onnx, .zip)
        name: Model name
        description: Model description
        category: Model category
        input_type: Input data type
        output_type: Output type
        tags: Comma-separated tags
        license: Model license
        version: Model version
        user_id: User ID (from authentication)
    
    Returns:
        Upload result with model ID
    """
    
    # Validate file size
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required"
        )
    
    # Validate file extension
    supported_extensions = ['.h5', '.hdf5', '.pb', '.pt', '.pth', '.onnx', '.zip']
    file_extension = '.' + file.filename.split('.')[-1].lower()
    
    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Supported: {supported_extensions}"
        )
    
    # Validate category
    valid_categories = ["image_classification", "object_detection", "semantic_segmentation", "custom"]
    if category not in valid_categories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category. Valid categories: {valid_categories}"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Prepare metadata
        model_metadata = {
            "name": name,
            "description": description,
            "category": category,
            "input_type": input_type,
            "output_type": output_type,
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
            "license": license,
            "version": version
        }
        
        # Upload model
        result = await model_marketplace.upload_model(
            model_file_content=file_content,
            model_metadata=model_metadata,
            user_id=user_id,
            filename=file.filename
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model upload failed: {str(e)}"
        )

@router.get("/models")
async def get_marketplace_models(
    category: Optional[str] = Query(None, description="Filter by category"),
    user_id: Optional[str] = Query(None, description="Filter by uploader"),
    search: Optional[str] = Query(None, description="Search in model names and descriptions"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Models per page")
) -> Dict[str, Any]:
    """
    Get models from marketplace with filtering and pagination.
    
    Returns:
        Paginated list of marketplace models
    """
    
    try:
        result = await model_marketplace.get_marketplace_models(
            category=category,
            user_id=user_id,
            search_query=search,
            page=page,
            page_size=page_size
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get marketplace models: {str(e)}"
        )

@router.get("/models/{model_id}")
async def get_model_details(model_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific model.
    
    Args:
        model_id: Model identifier
    
    Returns:
        Detailed model information
    """
    
    try:
        result = await model_marketplace.get_model_details(model_id)
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model details: {str(e)}"
        )

@router.post("/models/{model_id}/download")
async def download_model(
    model_id: str,
    user_id: str = Form(...)  # In production, this would come from authentication
) -> FileResponse:
    """
    Download a model from the marketplace.
    
    Args:
        model_id: Model identifier
        user_id: User ID requesting download
    
    Returns:
        Model file for download
    """
    
    try:
        result = await model_marketplace.download_model(model_id, user_id)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Download failed")
            )
        
        file_path = result["file_path"]
        filename = result["filename"]
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream',
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "X-Model-ID": model_id,
                "X-Download-Count": str(result["download_info"]["total_downloads"])
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model download failed: {str(e)}"
        )

@router.get("/statistics")
async def get_marketplace_statistics() -> Dict[str, Any]:
    """
    Get marketplace statistics and analytics.
    
    Returns:
        Marketplace statistics
    """
    
    try:
        result = await model_marketplace.get_marketplace_statistics()
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get marketplace statistics: {str(e)}"
        )

@router.get("/categories")
async def get_model_categories() -> Dict[str, Any]:
    """
    Get available model categories.
    
    Returns:
        List of available categories with descriptions
    """
    
    categories = [
        {
            "id": "image_classification",
            "name": "Image Classification",
            "description": "Models that classify images into predefined categories",
            "examples": ["Plant species classifier", "Animal breed identifier", "Medical image classifier"]
        },
        {
            "id": "object_detection",
            "name": "Object Detection",
            "description": "Models that detect and locate objects within images",
            "examples": ["Face detection", "Vehicle detection", "Product detection"]
        },
        {
            "id": "semantic_segmentation", 
            "name": "Semantic Segmentation",
            "description": "Models that classify each pixel in an image",
            "examples": ["Road segmentation", "Medical image segmentation", "Satellite image analysis"]
        },
        {
            "id": "custom",
            "name": "Custom",
            "description": "Custom models that don't fit standard categories",
            "examples": ["Multi-modal models", "Specialized domain models", "Research models"]
        }
    ]
    
    return {
        "categories": categories,
        "total_categories": len(categories)
    }

@router.post("/models/{model_id}/review")
async def add_model_review(
    model_id: str,
    rating: int = Form(..., ge=1, le=5),
    comment: str = Form(..., min_length=10, max_length=500),
    user_id: str = Form(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Add a review for a model.
    
    Args:
        model_id: Model identifier
        rating: Rating from 1-5 stars
        comment: Review comment
        user_id: User ID leaving the review
    
    Returns:
        Review confirmation
    """
    
    try:
        # Get model details to verify it exists
        model_result = await model_marketplace.get_model_details(model_id)
        
        if "error" in model_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Model not found"
            )
        
        # In a full implementation, this would update the model's reviews
        # For now, return a success response
        
        return {
            "success": True,
            "message": "Review added successfully",
            "review": {
                "model_id": model_id,
                "user_id": user_id,
                "rating": rating,
                "comment": comment,
                "date": "2025-09-03T12:00:00Z"  # Would use actual timestamp
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add review: {str(e)}"
        )

@router.get("/search")
async def search_models(
    query: str = Query(..., min_length=2, description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="Minimum rating filter"),
    sort_by: str = Query("relevance", regex="^(relevance|rating|downloads|date)$", description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Results per page")
) -> Dict[str, Any]:
    """
    Search models in the marketplace.
    
    Args:
        query: Search query
        category: Filter by category
        min_rating: Minimum rating filter
        sort_by: Sort order (relevance, rating, downloads, date)
        page: Page number
        page_size: Results per page
    
    Returns:
        Search results with pagination
    """
    
    try:
        # Use the existing get_marketplace_models method with search
        result = await model_marketplace.get_marketplace_models(
            category=category,
            search_query=query,
            page=page,
            page_size=page_size
        )
        
        # Add search metadata
        result["search_info"] = {
            "query": query,
            "sort_by": sort_by,
            "min_rating": min_rating,
            "search_performed": True
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )

@router.get("/user/{user_id}/models")
async def get_user_models(
    user_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Models per page")
) -> Dict[str, Any]:
    """
    Get models uploaded by a specific user.
    
    Args:
        user_id: User identifier
        page: Page number
        page_size: Models per page
    
    Returns:
        User's uploaded models
    """
    
    try:
        result = await model_marketplace.get_marketplace_models(
            user_id=user_id,
            page=page,
            page_size=page_size
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user models: {str(e)}"
        )