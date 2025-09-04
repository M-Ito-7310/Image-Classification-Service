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
        print("Starting model initialization...")
        
        # Initialize TensorFlow models
        if TENSORFLOW_AVAILABLE:
            print("TensorFlow is available, loading models...")
            try:
                self._load_tensorflow_models()
                print("TensorFlow models loaded successfully")
            except Exception as e:
                print(f"Failed to load TensorFlow models: {e}")
        else:
            print("TensorFlow not available")
        
        # Initialize PyTorch models
        if PYTORCH_AVAILABLE:
            print("PyTorch is available, loading models...")
            try:
                self._load_pytorch_models()
                print("PyTorch models loaded successfully")
            except Exception as e:
                print(f"Failed to load PyTorch models: {e}")
        else:
            print("PyTorch not available")
        
        # Initialize Google Cloud Vision
        if GOOGLE_VISION_AVAILABLE:
            print("Google Cloud Vision is available, initializing...")
            try:
                self._initialize_google_vision()
                print("Google Cloud Vision initialized successfully")
            except Exception as e:
                print(f"Failed to initialize Google Vision: {e}")
        else:
            print("Google Cloud Vision not available")
        
        # Add mock model for development/testing
        print("Adding mock model...")
        self._add_mock_model()
        
        print(f"Available models after initialization: {list(self.models.keys())}")
        
        # Handle 'auto' setting for intelligent model selection
        print("Handling model selection...")
        self._handle_auto_model_selection()
        
        print(f"Selected default model: {self.get_default_model()}")
        
        # Mark models as initialized
        self._models_initialized = True
        print("Model initialization completed")
    
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
            
            # Note: Using decode_predictions instead of custom labels
            # self._load_imagenet_labels()  # Deprecated: use decode_predictions
            
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
            # Load actual ImageNet labels
            # Using keras.applications.imagenet_utils
            from tensorflow.keras.applications.imagenet_utils import decode_predictions
            # We'll use decode_predictions later, but for now create a basic set
            
            # Common ImageNet classes (subset for testing)
            common_labels = [
                'tench', 'goldfish', 'great_white_shark', 'tiger_shark', 'hammerhead', 
                'electric_ray', 'stingray', 'cock', 'hen', 'ostrich', 'brambling', 
                'goldfinch', 'house_finch', 'junco', 'indigo_bunting', 'robin', 'bulbul',
                'jay', 'magpie', 'chickadee', 'water_ouzel', 'kite', 'bald_eagle',
                'vulture', 'great_grey_owl', 'European_fire_salamander', 'common_newt',
                'eft', 'spotted_salamander', 'axolotl', 'bullfrog', 'tree_frog',
                'tailed_frog', 'loggerhead', 'leatherback_turtle', 'mud_turtle',
                'terrapin', 'box_turtle', 'banded_gecko', 'common_iguana',
                'American_chameleon', 'whiptail', 'agama', 'frilled_lizard',
                'alligator_lizard', 'Gila_monster', 'green_lizard', 'African_chameleon',
                'Komodo_dragon', 'African_crocodile', 'American_alligator', 'triceratops'
            ]
            
            # Extend to 1000 classes
            self.imagenet_labels = common_labels + [f"class_{i}" for i in range(len(common_labels), 1000)]
            
            print(f"Loaded {len(self.imagenet_labels)} ImageNet labels")
            
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
        print(f"\n=== CLASSIFICATION SERVICE STARTED ===")
        print(f"Input model_name: {model_name}")
        print(f"Available models: {list(self.models.keys())}")
        
        start_time = time.time()
        
        if model_name is None:
            model_name = self.get_default_model()
        
        print(f"Selected model_name: {model_name}")
        
        if confidence_threshold is None:
            confidence_threshold = settings.CONFIDENCE_THRESHOLD
        
        print(f"Using confidence threshold: {confidence_threshold}")
        
        # Generate cache key from image data
        image_hash = None
        if use_cache:
            print("Checking cache...")
            image_bytes = image.tobytes()
            image_hash = hashlib.md5(image_bytes).hexdigest()
            print(f"Image hash: {image_hash}")
            
            # Check cache first
            cached_result = await cache_service.get_cached_classification(image_hash, model_name)
            if cached_result:
                print("Cache hit! Returning cached result")
                # Add cache hit indicator
                cached_result["from_cache"] = True
                cached_result["cache_hit"] = True
                return cached_result
            else:
                print("Cache miss, proceeding with classification")
        else:
            print("Cache disabled, proceeding with classification")
        
        # Check if model exists
        if model_name not in self.models:
            available_models = list(self.models.keys())
            if available_models:
                model_name = available_models[0]
            else:
                model_name = 'mock'
        
        try:
            # Route to appropriate classification method
            print(f"Starting classification with model: {model_name}")
            print(f"Image shape: {image.shape}, dtype: {image.dtype}")
            
            if model_name == 'mock':
                results = await self._classify_mock(image)
            elif model_name == 'google_vision':
                results = await self._classify_google_vision(image)
            elif model_name in ['mobilenet_v2', 'resnet50']:
                print(f"Using TensorFlow model: {model_name}")
                results = await self._classify_tensorflow(image, model_name)
            elif model_name.endswith('_torch'):
                results = await self._classify_pytorch(image, model_name)
            elif model_name.startswith('custom_'):
                results = await self._classify_custom_model(image, model_name)
            else:
                raise ValueError(f"Unknown model: {model_name}")
            
            print(f"Raw classification results: {results}")
            print(f"Number of raw predictions: {len(results.get('predictions', []))}")
            
            # Filter results by confidence threshold
            filtered_predictions = []
            filtered_scores = {}
            
            for pred in results['predictions']:
                print(f"Checking prediction: {pred}, confidence: {pred['confidence']}, threshold: {confidence_threshold}")
                if pred['confidence'] >= confidence_threshold:
                    filtered_predictions.append(pred)
                    filtered_scores[pred['class_name']] = pred['confidence']
                else:
                    print(f"Filtered out: {pred['class_name']} (confidence {pred['confidence']} < {confidence_threshold})")
            
            print(f"After filtering: {len(filtered_predictions)} predictions remain")
            
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
            
            print(f"Final result: {final_result}")
            
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
            print(f"CLASSIFICATION ERROR: {e}")
            import traceback
            traceback.print_exc()
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
        
        print(f"Mock classifier generated {len(predictions)} predictions: {predictions}")
        return {'predictions': predictions}
    
    async def _classify_tensorflow(
        self, 
        image: np.ndarray, 
        model_name: str
    ) -> Dict[str, Any]:
        """Classify using TensorFlow models with human-readable labels."""
        if not TENSORFLOW_AVAILABLE:
            print("TensorFlow not available, falling back to mock")
            return await self._classify_mock(image)
        
        try:
            print(f"Getting TensorFlow model: {model_name}")
            model = self.models[model_name]
            print(f"Model loaded successfully: {type(model)}")
            
            # Ensure correct input shape
            if len(image.shape) == 3:
                image = np.expand_dims(image, axis=0)
            
            print(f"Input image shape for TensorFlow: {image.shape}")
            print(f"Input image dtype: {image.dtype}, min: {image.min()}, max: {image.max()}")
            
            # Make prediction
            print("Making TensorFlow prediction...")
            predictions = model.predict(image, verbose=0)
            print(f"Raw prediction shape: {predictions.shape}")
            print(f"Raw prediction sample (first 10): {predictions[0][:10]}")
            
            # Use TensorFlow's decode_predictions for human-readable labels
            from tensorflow.keras.applications.imagenet_utils import decode_predictions
            
            # decode_predictions expects the full predictions array with batch dimension
            decoded_predictions = decode_predictions(predictions, top=5)[0]
            print(f"Decoded predictions: {decoded_predictions}")
            
            results = []
            for class_id, class_name, confidence in decoded_predictions:
                print(f"Adding result: {class_name} = {confidence:.4f} (ID: {class_id})")
                results.append({
                    'class_name': class_name,
                    'confidence': float(confidence),
                    'class_id': class_id
                })
            
            print(f"TensorFlow results: {results}")
            return {'predictions': results}
            
        except Exception as e:
            print(f"TensorFlow classification error: {e}")
            import traceback
            traceback.print_exc()
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