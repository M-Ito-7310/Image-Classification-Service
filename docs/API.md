# AI Image Classification Service - API Reference

## Overview

The AI Image Classification Service provides a RESTful API for uploading and classifying images using various AI/ML models. The API is built with FastAPI and provides comprehensive OpenAPI documentation, real-time processing, and support for multiple AI providers.

**Base URL**: `http://localhost:8000` (development)  
**API Version**: v1  
**Documentation**: `http://localhost:8000/docs` (Swagger UI)  
**OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Authentication

### Current Status
- **Development Mode**: No authentication required
- **Production**: JWT authentication will be implemented in Phase 3

### Future Authentication (Phase 3)
```http
Authorization: Bearer {jwt_token}
```

## Core Endpoints

### Health Check

#### GET `/api/v1/health`

Health check endpoint for system monitoring and dependency verification.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-01T12:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "ai_models": "healthy",
    "storage": "healthy"
  }
}
```

**Response Codes:**
- `200`: Service is healthy
- `503`: Service unavailable or dependencies unhealthy

---

### Image Classification

#### POST `/api/v1/classify`

Upload and classify an image using the specified AI model.

**Request:**
```http
POST /api/v1/classify
Content-Type: multipart/form-data

Form Data:
- file: [required] Image file (JPEG, PNG, WebP, BMP)
- model: [optional] Model name (default: "default") 
- threshold: [optional] Confidence threshold 0.0-1.0 (default: 0.5)
- max_results: [optional] Maximum number of results (default: 5)
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/classify" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.jpg" \
     -F "model=imagenet_mobilenet_v2" \
     -F "threshold=0.7"
```

**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "class_name": "Golden Retriever",
      "confidence": 0.89,
      "class_id": 207
    },
    {
      "class_name": "Labrador Retriever",
      "confidence": 0.76,
      "class_id": 208
    }
  ],
  "processing_time": 1.234,
  "model_used": "imagenet_mobilenet_v2",
  "image_metadata": {
    "filename": "image.jpg",
    "size": 1024000,
    "format": "JPEG",
    "dimensions": [1920, 1080]
  }
}
```

**Response Codes:**
- `200`: Classification successful
- `400`: Invalid file format or parameters
- `413`: File too large (>10MB)
- `422`: Validation error
- `500`: Internal server error

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "Unsupported file format. Supported formats: JPEG, PNG, WebP, BMP",
    "details": {
      "filename": "image.gif",
      "detected_format": "GIF"
    }
  }
}
```

---

### Model Management

#### GET `/api/v1/models`

Retrieve information about available AI models.

**Response:**
```json
{
  "available_models": [
    {
      "name": "imagenet_mobilenet_v2",
      "description": "MobileNet v2 trained on ImageNet dataset",
      "classes": 1000,
      "input_size": [224, 224],
      "status": "active",
      "accuracy": 0.854,
      "inference_time": 0.45,
      "categories": ["general_object_recognition"],
      "provider": "tensorflow"
    },
    {
      "name": "custom_model_1",
      "description": "Custom trained model for specific use case",
      "classes": 50,
      "input_size": [256, 256], 
      "status": "active",
      "accuracy": 0.92,
      "inference_time": 0.67,
      "categories": ["custom"],
      "provider": "pytorch"
    }
  ],
  "default_model": "imagenet_mobilenet_v2"
}
```

**Response Codes:**
- `200`: Models retrieved successfully
- `500`: Internal server error

---

#### GET `/api/v1/models/{model_name}`

Get detailed information about a specific model.

**Parameters:**
- `model_name`: Name of the model

**Response:**
```json
{
  "model": {
    "name": "imagenet_mobilenet_v2",
    "description": "MobileNet v2 trained on ImageNet dataset",
    "version": "2.1.0",
    "classes": 1000,
    "input_size": [224, 224],
    "status": "active",
    "accuracy": 0.854,
    "inference_time": 0.45,
    "categories": ["general_object_recognition"],
    "provider": "tensorflow",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-20T14:30:00Z",
    "metadata": {
      "training_dataset": "ImageNet-1k",
      "architecture": "MobileNetV2",
      "pretrained": true,
      "fine_tuned": false
    },
    "performance_metrics": {
      "top1_accuracy": 0.854,
      "top5_accuracy": 0.944,
      "f1_score": 0.847,
      "inference_time_ms": 450
    }
  }
}
```

**Response Codes:**
- `200`: Model information retrieved
- `404`: Model not found
- `500`: Internal server error

---

## Batch Processing (Phase 3)

### POST `/api/v1/classify/batch`

*Planned for Phase 3*

Upload and classify multiple images in a single request.

**Request:**
```http
POST /api/v1/classify/batch
Content-Type: multipart/form-data

Form Data:
- files: [required] Multiple image files
- model: [optional] Model name
- threshold: [optional] Confidence threshold
```

**Response:**
```json
{
  "success": true,
  "batch_id": "batch_12345",
  "total_images": 5,
  "results": [
    {
      "filename": "image1.jpg",
      "success": true,
      "predictions": [...],
      "processing_time": 1.234
    },
    {
      "filename": "image2.jpg", 
      "success": false,
      "error": "Invalid file format"
    }
  ],
  "summary": {
    "successful": 4,
    "failed": 1,
    "total_processing_time": 5.67
  }
}
```

---

## Classification History (Phase 3)

### GET `/api/v1/history`

*Planned for Phase 3 - Requires Authentication*

Retrieve classification history for the authenticated user.

**Query Parameters:**
- `limit`: Number of results (default: 20, max: 100)
- `offset`: Pagination offset (default: 0)
- `model`: Filter by model name
- `date_from`: Filter from date (ISO 8601)
- `date_to`: Filter to date (ISO 8601)

**Response:**
```json
{
  "history": [
    {
      "id": "hist_12345",
      "filename": "image.jpg",
      "model_used": "imagenet_mobilenet_v2",
      "predictions": [...],
      "processing_time": 1.234,
      "created_at": "2025-09-01T12:00:00Z"
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 20,
    "offset": 0,
    "has_next": true
  }
}
```

### GET `/api/v1/history/{classification_id}`

*Planned for Phase 3 - Requires Authentication*

Get detailed information about a specific classification result.

---

## User Management (Phase 3)

### POST `/api/v1/auth/register`

*Planned for Phase 3*

Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

### POST `/api/v1/auth/login`

*Planned for Phase 3*

Authenticate user and return JWT tokens.

**Request:**
```json
{
  "email": "user@example.com", 
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

---

## Error Handling

### Error Response Format

All API errors follow a consistent format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": {
      "additional": "context information"
    }
  },
  "request_id": "req_12345"
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_FILE_FORMAT` | 400 | Unsupported image format |
| `FILE_TOO_LARGE` | 413 | File exceeds size limit |
| `MODEL_NOT_FOUND` | 404 | Specified model not available |
| `PROCESSING_FAILED` | 500 | AI model processing error |
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `UNAUTHORIZED` | 401 | Invalid or missing authentication |
| `INSUFFICIENT_QUOTA` | 403 | User quota exceeded |

---

## Rate Limiting (Production)

### Current Limits (Development)
- No rate limiting in development mode

### Planned Limits (Production)
- **Free Tier**: 100 requests/hour, 500 requests/day
- **Premium Tier**: 1000 requests/hour, 10000 requests/day

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1693574400
```

---

## File Upload Specifications

### Supported Formats
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png) 
- **WebP** (.webp)
- **BMP** (.bmp)

### File Constraints
- **Maximum Size**: 10MB
- **Minimum Dimensions**: 32x32 pixels
- **Maximum Dimensions**: 4096x4096 pixels
- **Color Modes**: RGB, RGBA, Grayscale

### Image Processing
- Automatic format conversion to RGB
- Resizing to model input requirements
- EXIF data removal for privacy
- Optional preprocessing (normalization, augmentation)

---

## Model Information

### Available Models (Current)

#### imagenet_mobilenet_v2
- **Description**: Lightweight CNN for general object recognition
- **Classes**: 1,000 ImageNet categories
- **Input Size**: 224x224 pixels
- **Accuracy**: Top-1: 85.4%, Top-5: 94.4%
- **Inference Time**: ~450ms
- **Use Cases**: General purpose object classification

### Planned Models (Future Phases)

#### custom_models
- **Description**: User-uploaded custom trained models
- **Support**: TensorFlow SavedModel, PyTorch (.pt), ONNX
- **Validation**: Automatic model validation and testing

#### cloud_vision_api
- **Description**: Google Cloud Vision API integration
- **Features**: Label detection, object localization, OCR
- **Pricing**: Per-request pricing model

---

## SDK and Client Libraries (Future)

### Python SDK (Planned)
```python
from image_classifier import ImageClassifierClient

client = ImageClassifierClient(api_key="your_key")
result = client.classify("image.jpg", model="imagenet_mobilenet_v2")
```

### JavaScript SDK (Planned)
```javascript
import { ImageClassifierClient } from 'image-classifier-js';

const client = new ImageClassifierClient({ apiKey: 'your_key' });
const result = await client.classify(imageFile);
```

---

## Webhooks (Phase 4)

### Webhook Events (Planned)
- `classification.completed`: Image classification finished
- `batch.completed`: Batch processing finished  
- `model.updated`: Model status changed
- `user.quota_exceeded`: User reached quota limit

### Webhook Payload Example
```json
{
  "event": "classification.completed",
  "data": {
    "classification_id": "clf_12345",
    "user_id": "user_67890", 
    "results": {...},
    "timestamp": "2025-09-01T12:00:00Z"
  },
  "webhook_id": "wh_abc123"
}
```

---

## OpenAPI Specification

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### Download OpenAPI Schema
```bash
curl http://localhost:8000/openapi.json > openapi.json
```

---

## Testing the API

### Health Check Test
```bash
curl -X GET "http://localhost:8000/api/v1/health" \
     -H "accept: application/json"
```

### Image Classification Test
```bash
# Download sample image
curl -o sample.jpg "https://images.unsplash.com/photo-1518717758536-85ae29035b6d"

# Classify image
curl -X POST "http://localhost:8000/api/v1/classify" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sample.jpg"
```

### Model Information Test
```bash
curl -X GET "http://localhost:8000/api/v1/models" \
     -H "accept: application/json"
```

---

## Performance Metrics

### Response Time Targets
- **Health Check**: < 50ms
- **Model List**: < 200ms  
- **Image Classification**: < 3s (Phase 2), < 2s (Production)
- **Batch Processing**: < 30s for 10 images

### Throughput Targets
- **Concurrent Requests**: 50+ simultaneous classifications
- **Daily Processing**: 10,000+ images per day
- **Batch Size**: Up to 50 images per batch

---

## Support and Contact

### API Issues
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check comprehensive guides in `/docs`
- **Status Page**: Monitor service health and incidents

### Development Resources
- **Sample Code**: Examples in multiple programming languages
- **Postman Collection**: Pre-configured API requests
- **Testing Guide**: Comprehensive testing instructions

---

**API Version**: 1.0  
**Last Updated**: September 1, 2025  
**Next Major Update**: Phase 3 (Authentication & History)

For the most up-to-date API documentation, always refer to the interactive Swagger documentation at `http://localhost:8000/docs`.