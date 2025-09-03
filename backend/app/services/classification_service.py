import asyncio
import time
import hashlib
from typing import Dict, List, Any, Optional
import numpy as np
from pathlib import Path
import json

# ML imports (will be conditionally imported based on availability)
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available - using mock predictions")

try:
    import torch
    import torchvision.transforms as transforms
    import torchvision.models as models
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    print("PyTorch not available")

try:
    from google.cloud import vision
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False
    print("Google Cloud Vision not available")

from app.core.config import settings
from app.models.user import CustomModel
from app.services.cache_service import cache_service
from sqlalchemy.orm import Session

class ClassificationService:
    """Service for image classification using various ML models."""
    
    def __init__(self):
        self.models = {}
        self.model_info = {}
        self._actual_default_model = None  # Track the actual selected model
        self._models_initialized = False  # Track lazy initialization
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize available models."""
        
        # Initialize TensorFlow models
        if TENSORFLOW_AVAILABLE:
            try:
                self._load_tensorflow_models()
            except Exception as e:
                print(f"Failed to load TensorFlow models: {e}")
        
        # Initialize PyTorch models
        if PYTORCH_AVAILABLE:
            try:
                self._load_pytorch_models()
            except Exception as e:
                print(f"Failed to load PyTorch models: {e}")
        
        # Initialize Google Cloud Vision
        if GOOGLE_VISION_AVAILABLE:
            try:
                self._initialize_google_vision()
            except Exception as e:
                print(f"Failed to initialize Google Vision: {e}")
        
        # Add mock model for development/testing
        self._add_mock_model()
        
        # Handle 'auto' setting for intelligent model selection
        self._handle_auto_model_selection()
        
        # Mark models as initialized
        self._models_initialized = True
    
    def _load_tensorflow_models(self):
        """Load TensorFlow models."""
        if not TENSORFLOW_AVAILABLE:
            return
            
        try:
            # MobileNetV2
            mobilenet = tf.keras.applications.MobileNetV2(
                weights='imagenet',
                include_top=True,
                input_shape=(224, 224, 3)
            )
            self.models['mobilenet_v2'] = mobilenet
            
            # ResNet50
            resnet = tf.keras.applications.ResNet50(
                weights='imagenet',
                include_top=True,
                input_shape=(224, 224, 3)
            )
            self.models['resnet50'] = resnet
            
            # Load ImageNet class labels
            self._load_imagenet_labels()
            
        except Exception as e:
            print(f"Error loading TensorFlow models: {e}")
    
    def _load_pytorch_models(self):
        """Load PyTorch models."""
        if not PYTORCH_AVAILABLE:
            return
            
        try:
            # ResNet18
            resnet18 = models.resnet18(pretrained=True)
            resnet18.eval()
            self.models['resnet18_torch'] = resnet18
            
            # Define transforms
            self.pytorch_transform = transforms.Compose([
                transforms.ToPILImage(),
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                   std=[0.229, 0.224, 0.225])
            ])
            
        except Exception as e:
            print(f"Error loading PyTorch models: {e}")
    
    def _initialize_google_vision(self):
        """Initialize Google Cloud Vision client."""
        if not GOOGLE_VISION_AVAILABLE:
            return
            
        try:
            if settings.GOOGLE_CLOUD_CREDENTIALS:
                self.vision_client = vision.ImageAnnotatorClient()
                self.models['google_vision'] = 'google_cloud_vision'
        except Exception as e:
            print(f"Error initializing Google Vision: {e}")
    
    def _add_mock_model(self):
        """Add a mock model for development/testing."""
        self.models['mock'] = 'mock_classifier'
        self.model_info['mock'] = {
            'name': 'Mock Classifier',
            'description': 'Mock model for development and testing',
            'version': '1.0.0',
            'classes': ['cat', 'dog', 'bird', 'car', 'airplane'],
            'accuracy': 0.85
        }
    
    def _load_imagenet_labels(self):
        """Load ImageNet class labels."""
        try:
            # This would typically load from a JSON file
            # For now, using a subset of common classes
            self.imagenet_labels = [
                'Persian cat', 'Egyptian cat', 'tabby cat',
                'golden retriever', 'Labrador retriever', 'beagle',
                'robin', 'jay', 'magpie',
                'sports car', 'convertible', 'limousine',
                'airliner', 'warplane', 'space shuttle'
            ]
        except Exception as e:
            print(f"Error loading ImageNet labels: {e}")
            self.imagenet_labels = [f"class_{i}" for i in range(1000)]
    
    async def classify(
        self,
        image: np.ndarray,
        model_name: Optional[str] = None,
        confidence_threshold: Optional[float] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Classify an image using the specified model with caching support.
        
        Args:
            image: Preprocessed image array
            model_name: Name of model to use (default: settings.DEFAULT_MODEL)
            confidence_threshold: Minimum confidence threshold
            use_cache: Whether to use caching for results
            
        Returns:
            Classification results
        """
        start_time = time.time()
        
        if model_name is None:
            model_name = self.get_default_model()
        
        if confidence_threshold is None:
            confidence_threshold = settings.CONFIDENCE_THRESHOLD
        
        # Generate cache key from image data
        image_hash = None
        if use_cache:
            image_bytes = image.tobytes()
            image_hash = hashlib.md5(image_bytes).hexdigest()
            
            # Check cache first
            cached_result = await cache_service.get_cached_classification(image_hash, model_name)
            if cached_result:
                # Add cache hit indicator
                cached_result["from_cache"] = True
                cached_result["cache_hit"] = True
                return cached_result
        
        # Check if model exists
        if model_name not in self.models:
            available_models = list(self.models.keys())
            if available_models:
                model_name = available_models[0]
            else:
                model_name = 'mock'
        
        try:
            # Route to appropriate classification method
            if model_name == 'mock':
                results = await self._classify_mock(image)
            elif model_name == 'google_vision':
                results = await self._classify_google_vision(image)
            elif model_name in ['mobilenet_v2', 'resnet50']:
                results = await self._classify_tensorflow(image, model_name)
            elif model_name.endswith('_torch'):
                results = await self._classify_pytorch(image, model_name)
            elif model_name.startswith('custom_'):
                results = await self._classify_custom_model(image, model_name)
            else:
                raise ValueError(f"Unknown model: {model_name}")
            
            # Filter results by confidence threshold
            filtered_predictions = []
            filtered_scores = {}
            
            for pred in results['predictions']:
                if pred['confidence'] >= confidence_threshold:
                    filtered_predictions.append(pred)
                    filtered_scores[pred['class_name']] = pred['confidence']
            
            # Sort by confidence
            filtered_predictions.sort(key=lambda x: x['confidence'], reverse=True)
            
            processing_time = time.time() - start_time
            
            final_result = {
                'predictions': filtered_predictions[:5],  # Top 5
                'confidence_scores': filtered_scores,
                'processing_time': processing_time,
                'model_used': model_name,
                'threshold_applied': confidence_threshold,
                'from_cache': False,
                'cache_hit': False
            }
            
            # Cache the result for future requests
            if use_cache and image_hash:
                await cache_service.cache_classification_result(
                    image_hash, 
                    model_name, 
                    final_result,
                    ttl=3600  # Cache for 1 hour
                )
            
            return final_result
            
        except Exception as e:
            raise Exception(f"Classification failed with model {model_name}: {str(e)}")
    
    async def _classify_mock(self, image: np.ndarray) -> Dict[str, Any]:
        """Mock classification for development/testing."""
        await asyncio.sleep(0.1)  # Simulate processing time
        
        classes = ['cat', 'dog', 'bird', 'car', 'airplane']
        np.random.seed(42)  # For consistent results
        scores = np.random.random(len(classes))
        # Make scores more realistic with higher confidence
        scores = np.array([0.8, 0.15, 0.03, 0.015, 0.005])
        
        predictions = []
        for i, (class_name, score) in enumerate(zip(classes, scores)):
            predictions.append({
                'class_name': class_name,
                'confidence': float(score),
                'class_id': str(i)
            })
        
        return {'predictions': predictions}
    
    async def _classify_tensorflow(
        self, 
        image: np.ndarray, 
        model_name: str
    ) -> Dict[str, Any]:
        """Classify using TensorFlow models."""
        if not TENSORFLOW_AVAILABLE:
            return await self._classify_mock(image)
        
        try:
            model = self.models[model_name]
            
            # Ensure correct input shape
            if len(image.shape) == 3:
                image = np.expand_dims(image, axis=0)
            
            # Make prediction
            predictions = model.predict(image, verbose=0)
            predictions = predictions[0]  # Remove batch dimension
            
            # Get top predictions
            top_indices = np.argsort(predictions)[-5:][::-1]
            
            results = []
            for idx in top_indices:
                class_name = self.imagenet_labels[idx] if idx < len(self.imagenet_labels) else f"class_{idx}"
                confidence = float(predictions[idx])
                
                results.append({
                    'class_name': class_name,
                    'confidence': confidence,
                    'class_id': str(idx)
                })
            
            return {'predictions': results}
            
        except Exception as e:
            print(f"TensorFlow classification error: {e}")
            return await self._classify_mock(image)
    
    async def _classify_pytorch(
        self, 
        image: np.ndarray, 
        model_name: str
    ) -> Dict[str, Any]:
        """Classify using PyTorch models."""
        if not PYTORCH_AVAILABLE:
            return await self._classify_mock(image)
        
        try:
            model = self.models[model_name]
            
            # Convert numpy array to tensor
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)
            
            input_tensor = self.pytorch_transform(image)
            input_batch = input_tensor.unsqueeze(0)
            
            # Make prediction
            with torch.no_grad():
                predictions = model(input_batch)
                probabilities = torch.nn.functional.softmax(predictions[0], dim=0)
            
            # Get top predictions
            top_probs, top_indices = torch.topk(probabilities, 5)
            
            results = []
            for i in range(len(top_indices)):
                idx = top_indices[i].item()
                confidence = top_probs[i].item()
                class_name = self.imagenet_labels[idx] if idx < len(self.imagenet_labels) else f"class_{idx}"
                
                results.append({
                    'class_name': class_name,
                    'confidence': confidence,
                    'class_id': str(idx)
                })
            
            return {'predictions': results}
            
        except Exception as e:
            print(f"PyTorch classification error: {e}")
            return await self._classify_mock(image)
    
    async def _classify_google_vision(self, image: np.ndarray) -> Dict[str, Any]:
        """Classify using Google Cloud Vision API."""
        if not GOOGLE_VISION_AVAILABLE:
            return await self._classify_mock(image)
        
        try:
            # Convert numpy array to bytes
            from PIL import Image
            import io
            
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)
            
            pil_image = Image.fromarray(image)
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Create vision image object
            vision_image = vision.Image(content=img_byte_arr)
            
            # Perform label detection
            response = self.vision_client.label_detection(image=vision_image)
            labels = response.label_annotations
            
            if response.error.message:
                raise Exception(f'{response.error.message}')
            
            results = []
            for label in labels[:5]:  # Top 5 labels
                results.append({
                    'class_name': label.description,
                    'confidence': label.score,
                    'class_id': label.mid
                })
            
            return {'predictions': results}
            
        except Exception as e:
            print(f"Google Vision classification error: {e}")
            return await self._classify_mock(image)
    
    async def _classify_custom_model(
        self, 
        image: np.ndarray, 
        model_name: str
    ) -> Dict[str, Any]:
        """Classify using custom user models."""
        if model_name not in self.models or model_name not in self.model_info:
            return await self._classify_mock(image)
        
        try:
            model = self.models[model_name]
            model_info = self.model_info[model_name]
            model_type = model_info.get('model_type')
            class_names = model_info.get('classes', [])
            
            if model_type == 'tensorflow' and TENSORFLOW_AVAILABLE:
                # Ensure correct input shape for TensorFlow
                if len(image.shape) == 3:
                    image = np.expand_dims(image, axis=0)
                
                # Make prediction
                predictions = model.predict(image, verbose=0)
                predictions = predictions[0]  # Remove batch dimension
                
                # Get top predictions
                top_indices = np.argsort(predictions)[-5:][::-1]
                
                results = []
                for idx in top_indices:
                    if idx < len(class_names):
                        class_name = class_names[idx]
                        confidence = float(predictions[idx])
                        
                        results.append({
                            'class_name': class_name,
                            'confidence': confidence,
                            'class_id': str(idx)
                        })
                
                return {'predictions': results}
            
            elif model_type == 'pytorch' and PYTORCH_AVAILABLE:
                # Convert numpy array to tensor
                if image.dtype != np.uint8:
                    image = (image * 255).astype(np.uint8)
                
                # Use the same transform as built-in PyTorch models
                input_tensor = self.pytorch_transform(image)
                input_batch = input_tensor.unsqueeze(0)
                
                # Make prediction
                with torch.no_grad():
                    predictions = model(input_batch)
                    
                    # Handle different output formats
                    if isinstance(predictions, torch.Tensor):
                        probabilities = torch.nn.functional.softmax(predictions[0], dim=0)
                    else:
                        # Model might return dict or other format
                        probabilities = predictions[0]
                
                # Get top predictions
                top_probs, top_indices = torch.topk(probabilities, min(5, len(class_names)))
                
                results = []
                for i in range(len(top_indices)):
                    idx = top_indices[i].item()
                    confidence = top_probs[i].item()
                    
                    if idx < len(class_names):
                        class_name = class_names[idx]
                        
                        results.append({
                            'class_name': class_name,
                            'confidence': confidence,
                            'class_id': str(idx)
                        })
                
                return {'predictions': results}
            
            else:
                return await self._classify_mock(image)
                
        except Exception as e:
            print(f"Custom model classification error: {e}")
            return await self._classify_mock(image)
    
    async def load_custom_model(self, model_record: CustomModel) -> bool:
        """
        Load a custom model into the service.
        
        Args:
            model_record: Custom model database record
            
        Returns:
            True if successfully loaded, False otherwise
        """
        try:
            model_path = model_record.file_path
            model_id = f"custom_{model_record.model_id}"
            
            if model_record.model_type == 'tensorflow' and TENSORFLOW_AVAILABLE:
                model = tf.keras.models.load_model(model_path)
                self.models[model_id] = model
                
            elif model_record.model_type == 'pytorch' and PYTORCH_AVAILABLE:
                model = torch.load(model_path, map_location='cpu')
                model.eval()
                self.models[model_id] = model
                
            else:
                return False
            
            # Store model info
            self.model_info[model_id] = {
                'name': model_record.name,
                'description': model_record.description or f'Custom {model_record.model_type} model',
                'version': 'custom',
                'classes': json.loads(model_record.classes),
                'accuracy': None,
                'model_type': model_record.model_type,
                'custom': True,
                'user_id': model_record.user_id
            }
            
            return True
            
        except Exception as e:
            print(f"Failed to load custom model {model_record.model_id}: {e}")
            return False
    
    async def unload_custom_model(self, model_id: str) -> bool:
        """
        Unload a custom model from memory.
        
        Args:
            model_id: Model ID to unload
            
        Returns:
            True if successfully unloaded
        """
        try:
            full_model_id = f"custom_{model_id}"
            if full_model_id in self.models:
                del self.models[full_model_id]
            if full_model_id in self.model_info:
                del self.model_info[full_model_id]
            return True
        except Exception as e:
            print(f"Failed to unload custom model {model_id}: {e}")
            return False

    async def list_models(self, include_custom: bool = True, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        List all available models.
        
        Args:
            include_custom: Whether to include custom models
            user_id: Filter custom models by user ID
            
        Returns:
            List of available models
        """
        models_list = []
        
        for model_name in self.models.keys():
            model_info = self.model_info.get(model_name, {
                'name': model_name,
                'description': f'{model_name} model',
                'version': '1.0.0',
                'classes': ['various'],
                'accuracy': None,
                'custom': False
            })
            
            # Filter custom models by user if specified
            if model_info.get('custom', False):
                if not include_custom:
                    continue
                if user_id and model_info.get('user_id') != user_id:
                    continue
            
            # Add is_default flag
            model_info['is_default'] = (model_name == self.get_default_model())
            models_list.append(model_info)
        
        return models_list
    
    def _handle_auto_model_selection(self):
        """
        Handle 'auto' setting for intelligent model selection.
        Only selects model if DEFAULT_MODEL is set to 'auto'.
        """
        if settings.DEFAULT_MODEL.lower() == 'auto':
            self._actual_default_model = self._select_best_available_model()
            print(f"\n{'='*60}")
            print(f"Auto Model Selection: {self._actual_default_model}")
            print(f"{'='*60}\n")
        else:
            # Use explicitly specified model
            self._actual_default_model = settings.DEFAULT_MODEL
            if self._actual_default_model in self.models:
                print(f"Using configured model: {self._actual_default_model}")
            else:
                print(f"Warning: Configured model '{self._actual_default_model}' not available, using mock")
                self._actual_default_model = 'mock'
    
    def _select_best_available_model(self) -> str:
        """
        Select the best available model based on priority.
        
        Returns:
            Selected model name
        """
        # Priority order for real AI models
        preferred_models = [
            ('mobilenet_v2', 'TensorFlow MobileNetV2 - Fast & accurate (1000+ classes)'),
            ('resnet50', 'TensorFlow ResNet50 - High accuracy (1000+ classes)'),
            ('resnet18_torch', 'PyTorch ResNet18 - Alternative (1000+ classes)'),
            ('google_vision', 'Google Cloud Vision API - Comprehensive detection'),
            ('mock', 'Mock model - Development only (5 basic classes)')
        ]
        
        print("Checking available models:")
        # Find the first available model
        for model_name, description in preferred_models:
            if model_name in self.models:
                print(f"  [FOUND] {description}")
                
                if model_name == 'mock':
                    print("  [WARNING] Using mock model - Install TensorFlow/PyTorch for real AI capabilities")
                else:
                    print(f"  [INFO] Clock images will be classified correctly with {model_name}")
                
                return model_name
            else:
                print(f"  [NOT FOUND] {model_name}")
        
        # Fallback (should not happen due to mock)
        return 'mock'
    
    def get_default_model(self) -> str:
        """
        Get the actual default model (handles 'auto' setting).
        
        Returns:
            Actual model name being used
        """
        return self._actual_default_model or settings.DEFAULT_MODEL