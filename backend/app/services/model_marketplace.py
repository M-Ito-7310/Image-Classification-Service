"""
AI Model Marketplace service for user-uploaded custom models.
Enables users to upload, validate, and share trained AI models.
"""

import os
import json
import hashlib
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import torch
import tensorflow as tf
from PIL import Image
import numpy as np

from app.core.config import settings
from app.services.cache_service import CacheService
from app.services.security_service import FileSecurityService


class ModelMarketplace:
    """Service for managing user-uploaded AI models."""
    
    def __init__(self):
        self.cache_service = CacheService()
        self.security_service = FileSecurityService()
        self.marketplace_path = Path(settings.MODEL_STORAGE_PATH) / "marketplace"
        self.marketplace_path.mkdir(parents=True, exist_ok=True)
        
        # Model registry for tracking uploaded models
        self.registry_file = self.marketplace_path / "model_registry.json"
        self.model_registry = self._load_model_registry()
    
    def _load_model_registry(self) -> Dict[str, Any]:
        """Load model registry from file."""
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading model registry: {e}")
        
        # Default registry structure
        return {
            "models": {},
            "statistics": {
                "total_models": 0,
                "active_models": 0,
                "total_downloads": 0,
                "last_updated": datetime.utcnow().isoformat()
            },
            "categories": [
                "image_classification",
                "object_detection", 
                "semantic_segmentation",
                "custom"
            ]
        }
    
    def _save_model_registry(self):
        """Save model registry to file."""
        try:
            self.model_registry["statistics"]["last_updated"] = datetime.utcnow().isoformat()
            
            with open(self.registry_file, 'w') as f:
                json.dump(self.model_registry, f, indent=2)
        except Exception as e:
            print(f"Error saving model registry: {e}")
    
    async def upload_model(
        self,
        model_file_content: bytes,
        model_metadata: Dict[str, Any],
        user_id: str,
        filename: str
    ) -> Dict[str, Any]:
        """
        Upload and validate a custom AI model.
        
        Args:
            model_file_content: Binary content of model file
            model_metadata: Model metadata and configuration
            user_id: ID of user uploading the model
            filename: Original filename
        
        Returns:
            Upload result with model ID and validation status
        """
        
        try:
            # Security validation
            security_result = await self.security_service.validate_file_upload(
                model_file_content, filename
            )
            
            if not security_result["is_safe"]:
                return {
                    "success": False,
                    "error": f"Security validation failed: {security_result['reason']}"
                }
            
            # Generate model ID
            model_hash = hashlib.sha256(model_file_content).hexdigest()[:16]
            model_id = f"{user_id}_{model_hash}_{int(datetime.utcnow().timestamp())}"
            
            # Create model directory
            model_dir = self.marketplace_path / model_id
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # Save model file
            model_file_path = model_dir / filename
            with open(model_file_path, 'wb') as f:
                f.write(model_file_content)
            
            # Validate model format
            validation_result = await self._validate_model_format(
                str(model_file_path), model_metadata
            )
            
            if not validation_result["is_valid"]:
                # Clean up failed upload
                self._cleanup_model_directory(model_dir)
                return {
                    "success": False,
                    "error": f"Model validation failed: {validation_result['error']}"
                }
            
            # Create model entry
            model_entry = {
                "model_id": model_id,
                "user_id": user_id,
                "filename": filename,
                "file_path": str(model_file_path),
                "file_size": len(model_file_content),
                "file_hash": model_hash,
                "metadata": model_metadata,
                "validation": validation_result,
                "upload_date": datetime.utcnow().isoformat(),
                "status": "active",
                "downloads": 0,
                "rating": 0.0,
                "reviews": []
            }
            
            # Add to registry
            self.model_registry["models"][model_id] = model_entry
            self.model_registry["statistics"]["total_models"] += 1
            self.model_registry["statistics"]["active_models"] += 1
            
            # Save registry
            self._save_model_registry()
            
            # Cache model info for quick access
            await self.cache_service.set(
                f"marketplace_model:{model_id}",
                json.dumps(model_entry),
                ttl=3600
            )
            
            return {
                "success": True,
                "model_id": model_id,
                "model_info": {
                    "model_id": model_id,
                    "filename": filename,
                    "file_size": len(model_file_content),
                    "upload_date": model_entry["upload_date"],
                    "status": "active",
                    "validation": validation_result
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Model upload failed: {str(e)}"
            }
    
    async def _validate_model_format(
        self, 
        model_path: str, 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate uploaded model format and compatibility.
        
        Args:
            model_path: Path to uploaded model file
            metadata: Model metadata for validation
        
        Returns:
            Validation result with details
        """
        
        validation = {
            "is_valid": False,
            "format": None,
            "framework": None,
            "input_shape": None,
            "output_shape": None,
            "classes": None,
            "error": None
        }
        
        try:
            file_extension = Path(model_path).suffix.lower()
            
            # TensorFlow model validation
            if file_extension in ['.pb', '.h5', '.hdf5']:
                validation.update(await self._validate_tensorflow_model(model_path, metadata))
            
            # PyTorch model validation  
            elif file_extension in ['.pt', '.pth']:
                validation.update(await self._validate_pytorch_model(model_path, metadata))
            
            # ONNX model validation
            elif file_extension == '.onnx':
                validation.update(await self._validate_onnx_model(model_path, metadata))
            
            # ZIP archive (could contain model files)
            elif file_extension == '.zip':
                validation.update(await self._validate_zip_model(model_path, metadata))
            
            else:
                validation["error"] = f"Unsupported model format: {file_extension}"
                return validation
            
            # Additional metadata validation
            if validation["is_valid"]:
                validation.update(self._validate_model_metadata(metadata))
            
            return validation
            
        except Exception as e:
            validation["error"] = f"Model validation failed: {str(e)}"
            return validation
    
    async def _validate_tensorflow_model(
        self, 
        model_path: str, 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate TensorFlow model."""
        
        validation = {"framework": "tensorflow"}
        
        try:
            if model_path.endswith('.h5') or model_path.endswith('.hdf5'):
                # Keras model
                model = tf.keras.models.load_model(model_path)
                
                validation.update({
                    "is_valid": True,
                    "format": "keras_h5",
                    "input_shape": model.input_shape,
                    "output_shape": model.output_shape,
                    "layers": len(model.layers),
                    "parameters": model.count_params()
                })
                
            elif model_path.endswith('.pb'):
                # SavedModel format
                model = tf.saved_model.load(model_path)
                
                validation.update({
                    "is_valid": True,
                    "format": "saved_model",
                    "signatures": list(model.signatures.keys()) if hasattr(model, 'signatures') else []
                })
            
            else:
                validation["error"] = "Unsupported TensorFlow format"
                
        except Exception as e:
            validation["error"] = f"TensorFlow validation failed: {str(e)}"
        
        return validation
    
    async def _validate_pytorch_model(
        self, 
        model_path: str, 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate PyTorch model."""
        
        validation = {"framework": "pytorch"}
        
        try:
            # Load PyTorch model
            checkpoint = torch.load(model_path, map_location='cpu')
            
            if isinstance(checkpoint, dict):
                # Standard checkpoint format
                if 'model' in checkpoint:
                    model_state = checkpoint['model']
                elif 'state_dict' in checkpoint:
                    model_state = checkpoint['state_dict']
                else:
                    model_state = checkpoint
                
                validation.update({
                    "is_valid": True,
                    "format": "pytorch_checkpoint",
                    "keys": list(checkpoint.keys()),
                    "parameters": len(model_state) if isinstance(model_state, dict) else 0
                })
                
            else:
                # Direct model object
                validation.update({
                    "is_valid": True,
                    "format": "pytorch_model",
                    "type": type(checkpoint).__name__
                })
            
        except Exception as e:
            validation["error"] = f"PyTorch validation failed: {str(e)}"
        
        return validation
    
    async def _validate_onnx_model(
        self, 
        model_path: str, 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate ONNX model."""
        
        validation = {"framework": "onnx"}
        
        try:
            # Basic file validation
            if os.path.exists(model_path) and os.path.getsize(model_path) > 0:
                validation.update({
                    "is_valid": True,
                    "format": "onnx",
                    "file_size": os.path.getsize(model_path)
                })
            else:
                validation["error"] = "Invalid ONNX file"
                
        except Exception as e:
            validation["error"] = f"ONNX validation failed: {str(e)}"
        
        return validation
    
    async def _validate_zip_model(
        self, 
        model_path: str, 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate ZIP archive containing model files."""
        
        validation = {"framework": "archive"}
        
        try:
            with zipfile.ZipFile(model_path, 'r') as zip_file:
                file_list = zip_file.namelist()
                
                # Check for common model files
                model_files = [
                    f for f in file_list 
                    if any(f.endswith(ext) for ext in ['.h5', '.hdf5', '.pb', '.pt', '.pth', '.onnx'])
                ]
                
                if model_files:
                    validation.update({
                        "is_valid": True,
                        "format": "zip_archive",
                        "contents": file_list,
                        "model_files": model_files
                    })
                else:
                    validation["error"] = "No recognized model files in archive"
                    
        except Exception as e:
            validation["error"] = f"ZIP validation failed: {str(e)}"
        
        return validation
    
    def _validate_model_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate model metadata completeness."""
        
        required_fields = ["name", "description", "category", "input_type", "output_type"]
        validation = {}
        
        missing_fields = [field for field in required_fields if field not in metadata]
        
        if missing_fields:
            validation["metadata_warning"] = f"Missing recommended fields: {missing_fields}"
        
        # Validate category
        if "category" in metadata:
            if metadata["category"] not in self.model_registry["categories"]:
                validation["category_warning"] = f"Unknown category: {metadata['category']}"
        
        return validation
    
    async def get_marketplace_models(
        self,
        category: Optional[str] = None,
        user_id: Optional[str] = None,
        search_query: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        Get models from marketplace with filtering and pagination.
        
        Args:
            category: Filter by model category
            user_id: Filter by uploader user ID
            search_query: Search in model names and descriptions
            page: Page number (1-based)
            page_size: Models per page
        
        Returns:
            Paginated model listing with metadata
        """
        
        try:
            models = list(self.model_registry["models"].values())
            
            # Apply filters
            if category:
                models = [m for m in models if m.get("metadata", {}).get("category") == category]
            
            if user_id:
                models = [m for m in models if m.get("user_id") == user_id]
            
            if search_query:
                query_lower = search_query.lower()
                models = [
                    m for m in models 
                    if (query_lower in m.get("metadata", {}).get("name", "").lower() or
                        query_lower in m.get("metadata", {}).get("description", "").lower())
                ]
            
            # Filter only active models
            models = [m for m in models if m.get("status") == "active"]
            
            # Sort by upload date (newest first)
            models.sort(key=lambda x: x.get("upload_date", ""), reverse=True)
            
            # Pagination
            total_models = len(models)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            page_models = models[start_idx:end_idx]
            
            # Prepare response models (remove sensitive info)
            response_models = []
            for model in page_models:
                response_model = {
                    "model_id": model["model_id"],
                    "name": model.get("metadata", {}).get("name", "Unnamed Model"),
                    "description": model.get("metadata", {}).get("description", ""),
                    "category": model.get("metadata", {}).get("category", "custom"),
                    "upload_date": model["upload_date"],
                    "downloads": model.get("downloads", 0),
                    "rating": model.get("rating", 0.0),
                    "file_size": model.get("file_size", 0),
                    "framework": model.get("validation", {}).get("framework", "unknown"),
                    "input_type": model.get("metadata", {}).get("input_type", "unknown"),
                    "output_type": model.get("metadata", {}).get("output_type", "unknown")
                }
                response_models.append(response_model)
            
            return {
                "models": response_models,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_models": total_models,
                    "total_pages": (total_models + page_size - 1) // page_size
                },
                "filters_applied": {
                    "category": category,
                    "user_id": user_id,
                    "search_query": search_query
                },
                "statistics": self.model_registry["statistics"]
            }
            
        except Exception as e:
            return {
                "error": f"Failed to get marketplace models: {str(e)}",
                "models": [],
                "pagination": {"page": 1, "page_size": 20, "total_models": 0, "total_pages": 0}
            }
    
    async def get_model_details(self, model_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific model.
        
        Args:
            model_id: Model identifier
        
        Returns:
            Detailed model information
        """
        
        try:
            # Check cache first
            cached_model = await self.cache_service.get(f"marketplace_model:{model_id}")
            if cached_model:
                model_data = json.loads(cached_model)
            else:
                # Get from registry
                model_data = self.model_registry["models"].get(model_id)
                
                if not model_data:
                    return {"error": f"Model {model_id} not found"}
                
                # Cache for future requests
                await self.cache_service.set(
                    f"marketplace_model:{model_id}",
                    json.dumps(model_data),
                    ttl=3600
                )
            
            # Remove sensitive information
            public_model_data = {
                "model_id": model_data["model_id"],
                "metadata": model_data.get("metadata", {}),
                "validation": model_data.get("validation", {}),
                "upload_date": model_data["upload_date"],
                "status": model_data["status"],
                "downloads": model_data.get("downloads", 0),
                "rating": model_data.get("rating", 0.0),
                "reviews": model_data.get("reviews", []),
                "file_size": model_data.get("file_size", 0),
                "file_hash": model_data.get("file_hash", "")
            }
            
            return {"model": public_model_data}
            
        except Exception as e:
            return {"error": f"Failed to get model details: {str(e)}"}
    
    async def download_model(self, model_id: str, requesting_user_id: str) -> Dict[str, Any]:
        """
        Download a model from the marketplace.
        
        Args:
            model_id: Model identifier
            requesting_user_id: ID of user requesting download
        
        Returns:
            Download information or error
        """
        
        try:
            model_data = self.model_registry["models"].get(model_id)
            
            if not model_data:
                return {"error": f"Model {model_id} not found"}
            
            if model_data["status"] != "active":
                return {"error": f"Model {model_id} is not available for download"}
            
            model_file_path = model_data["file_path"]
            
            if not os.path.exists(model_file_path):
                return {"error": f"Model file not found on server"}
            
            # Increment download counter
            self.model_registry["models"][model_id]["downloads"] += 1
            self.model_registry["statistics"]["total_downloads"] += 1
            
            # Save updated statistics
            self._save_model_registry()
            
            # Update cache
            await self.cache_service.set(
                f"marketplace_model:{model_id}",
                json.dumps(model_data),
                ttl=3600
            )
            
            return {
                "success": True,
                "model_id": model_id,
                "file_path": model_file_path,
                "filename": model_data["filename"],
                "file_size": model_data["file_size"],
                "download_info": {
                    "total_downloads": model_data["downloads"],
                    "download_date": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            return {"error": f"Model download failed: {str(e)}"}
    
    def _cleanup_model_directory(self, model_dir: Path):
        """Clean up model directory after failed upload."""
        try:
            import shutil
            if model_dir.exists():
                shutil.rmtree(model_dir)
        except Exception:
            pass  # Silent cleanup failure
    
    async def get_marketplace_statistics(self) -> Dict[str, Any]:
        """Get marketplace statistics and analytics."""
        
        try:
            stats = self.model_registry["statistics"].copy()
            
            # Calculate additional statistics
            models = list(self.model_registry["models"].values())
            active_models = [m for m in models if m.get("status") == "active"]
            
            # Category breakdown
            category_counts = {}
            for model in active_models:
                category = model.get("metadata", {}).get("category", "unknown")
                category_counts[category] = category_counts.get(category, 0) + 1
            
            # Framework breakdown
            framework_counts = {}
            for model in active_models:
                framework = model.get("validation", {}).get("framework", "unknown")
                framework_counts[framework] = framework_counts.get(framework, 0) + 1
            
            # Popular models (top 10 by downloads)
            popular_models = sorted(
                active_models,
                key=lambda x: x.get("downloads", 0),
                reverse=True
            )[:10]
            
            stats.update({
                "category_breakdown": category_counts,
                "framework_breakdown": framework_counts,
                "popular_models": [
                    {
                        "model_id": m["model_id"],
                        "name": m.get("metadata", {}).get("name", "Unnamed"),
                        "downloads": m.get("downloads", 0),
                        "rating": m.get("rating", 0.0)
                    }
                    for m in popular_models
                ],
                "recent_uploads": len([
                    m for m in active_models 
                    if (datetime.utcnow() - datetime.fromisoformat(m["upload_date"])).days <= 7
                ])
            })
            
            return stats
            
        except Exception as e:
            return {"error": f"Failed to get marketplace statistics: {str(e)}"}


# Global instance
model_marketplace = ModelMarketplace()