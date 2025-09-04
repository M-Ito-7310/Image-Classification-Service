from PIL import Image, ImageOps
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Union
import cv2
from fastapi import HTTPException
import io

class ImageService:
    """Service for image processing operations."""
    
    def __init__(self):
        # Standard image size for most models
        self.standard_size = (224, 224)
        self.max_dimension = 4096  # Maximum dimension for safety (supports up to 4K images)
    
    async def process_image(
        self,
        image_path: Union[str, Path],
        target_size: Optional[Tuple[int, int]] = None,
        normalize: bool = True
    ) -> np.ndarray:
        """
        Process image for classification.
        
        Args:
            image_path: Path to the image file
            target_size: Target size for resizing (width, height)
            normalize: Whether to normalize pixel values to [0, 1]
            
        Returns:
            Processed image as numpy array
        """
        try:
            image_path = Path(image_path)
            
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Load image using PIL
            with Image.open(image_path) as image:
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Auto-resize large images instead of rejecting them
                if image.size[0] > self.max_dimension or image.size[1] > self.max_dimension:
                    print(f"Image dimensions {image.size} exceed maximum {self.max_dimension}, auto-resizing...")
                    # Calculate new size maintaining aspect ratio
                    width, height = image.size
                    if width > height:
                        new_width = self.max_dimension
                        new_height = int((height * self.max_dimension) / width)
                    else:
                        new_height = self.max_dimension
                        new_width = int((width * self.max_dimension) / height)
                    
                    # Resize with high quality
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"Image resized to: {image.size}")
                
                # Resize if target size is specified
                if target_size is None:
                    target_size = self.standard_size
                
                # Use high-quality resampling
                image = image.resize(target_size, Image.Resampling.LANCZOS)
                
                # Convert to numpy array
                image_array = np.array(image)
                
                # Normalize if requested
                if normalize:
                    image_array = image_array.astype(np.float32) / 255.0
                
                return image_array
                
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Image processing failed: {str(e)}"
            )
    
    async def preprocess_for_model(
        self,
        image: np.ndarray,
        model_name: str = "mobilenet_v2"
    ) -> np.ndarray:
        """
        Preprocess image for specific model requirements.
        
        Args:
            image: Input image as numpy array
            model_name: Name of the model for preprocessing
            
        Returns:
            Preprocessed image array
        """
        try:
            # Model-specific preprocessing
            if model_name.startswith("mobilenet"):
                # MobileNet preprocessing: scale to [-1, 1]
                image = (image - 0.5) * 2.0
                
            elif model_name.startswith("resnet"):
                # ResNet preprocessing: ImageNet normalization
                mean = np.array([0.485, 0.456, 0.406])
                std = np.array([0.229, 0.224, 0.225])
                image = (image - mean) / std
                
            elif model_name.startswith("inception"):
                # Inception preprocessing: scale to [-1, 1]
                image = (image - 0.5) * 2.0
                
            else:
                # Default: assume image is already normalized to [0, 1]
                pass
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Model preprocessing failed: {str(e)}"
            )
    
    async def enhance_image(self, image_path: Union[str, Path]) -> Path:
        """
        Enhance image quality for better classification.
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Path to enhanced image
        """
        try:
            image_path = Path(image_path)
            
            # Load image with OpenCV for enhancement
            image = cv2.imread(str(image_path))
            
            if image is None:
                raise ValueError("Could not load image with OpenCV")
            
            # Apply enhancements
            # 1. Contrast enhancement
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l_channel, a, b = cv2.split(lab)
            
            # Apply CLAHE to L channel
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l_channel = clahe.apply(l_channel)
            
            # Merge channels and convert back to BGR
            lab = cv2.merge([l_channel, a, b])
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            # 2. Noise reduction
            enhanced = cv2.bilateralFilter(enhanced, 9, 75, 75)
            
            # 3. Sharpening
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            enhanced = cv2.filter2D(enhanced, -1, kernel)
            
            # Save enhanced image
            enhanced_path = image_path.parent / f"enhanced_{image_path.name}"
            cv2.imwrite(str(enhanced_path), enhanced)
            
            return enhanced_path
            
        except Exception as e:
            # Return original path if enhancement fails
            print(f"Image enhancement failed: {e}")
            return image_path
    
    def get_image_metadata(self, image_path: Union[str, Path]) -> dict:
        """
        Extract metadata from image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing image metadata
        """
        try:
            image_path = Path(image_path)
            
            with Image.open(image_path) as image:
                metadata = {
                    "filename": image_path.name,
                    "format": image.format,
                    "mode": image.mode,
                    "size": image.size,
                    "width": image.size[0],
                    "height": image.size[1],
                    "has_transparency": image.mode in ("RGBA", "LA") or "transparency" in image.info
                }
                
                # Add EXIF data if available
                if hasattr(image, '_getexif') and image._getexif():
                    metadata["exif"] = dict(image._getexif())
                
                return metadata
                
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def validate_image_file(file_path: Union[str, Path]) -> bool:
        """
        Validate if file is a valid image.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if valid image, False otherwise
        """
        try:
            with Image.open(file_path) as image:
                image.verify()
            return True
        except Exception:
            return False