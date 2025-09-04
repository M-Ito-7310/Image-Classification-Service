# AI Image Classification Service / AI画像分類・認識サービス

[![Project Status](https://img.shields.io/badge/status-Phase%208%20Complete-brightgreen.svg)](https://github.com/M-Ito-7310/image-classification-service)
[![Python](https://img.shields.io/badge/python-3.12%2B-green.svg)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/vue.js-3.5-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-blue.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0%2B-blue.svg)](https://www.typescriptlang.org/)
[![Enterprise Ready](https://img.shields.io/badge/enterprise-ready-success.svg)](https://github.com/M-Ito-7310/image-classification-service)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Languages**: English | [日本語](#日本語版)

A production-ready AI-powered image classification service that provides intelligent single-image analysis capabilities with modern web technologies. Built with Vue.js 3 + TypeScript frontend and FastAPI backend, featuring real AI model integration, comprehensive authentication, and intuitive user interface design.

## Overview

This project demonstrates production-level AI/ML integration, modern web development practices, and scalable full-stack architecture. Built as a comprehensive portfolio project showcasing advanced development skills with real AI integration, secure authentication, multi-language support, and professional UI/UX design.

## Architecture Overview

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vue.js Web    │    │  FastAPI Server │    │   AI Services   │
│   Frontend      │◄──►│   Backend       │◄──►│  TensorFlow/    │
│                 │    │                 │    │  Google Cloud   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Static Assets  │    │   PostgreSQL    │    │   File Storage  │
│   (Nginx CDN)   │    │   Database      │    │    System       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Key Features

### 🔍 **Core Image Processing**
- **AI Classification**: TensorFlow and PyTorch model support with intelligent selection ✅ **IMPLEMENTED**
- **Single Image Processing**: Optimized workflow for individual image analysis ✅ **IMPLEMENTED**
- **Smart Image Preprocessing**: Automatic resizing, normalization, and validation ✅ **IMPLEMENTED**
- **Confidence Scoring**: Detailed prediction confidence with threshold filtering ✅ **IMPLEMENTED**
- **Custom Model Support**: Upload and manage custom trained models ✅ **IMPLEMENTED**
- **Result Caching**: Intelligent caching system for improved performance ✅ **IMPLEMENTED**
- **Security Validation**: Comprehensive file security scanning and validation ✅ **IMPLEMENTED**

### 📤 **Upload System**
- **Drag & Drop Interface**: Modern single-file upload with visual feedback ✅ **IMPLEMENTED**
- **Format Support**: JPEG, PNG, WebP, BMP image formats ✅ **IMPLEMENTED**
- **File Validation**: Size and security validation up to 10MB ✅ **IMPLEMENTED**
- **Image Preview**: Real-time image preview before processing ✅ **IMPLEMENTED**
- **Progress Tracking**: Upload and processing progress indicators ✅ **IMPLEMENTED**

### 📊 **Results & Analytics**
- **Interactive Results**: Visual classification results with confidence scores ✅ **IMPLEMENTED**
- **Classification History**: Persistent storage with user authentication ✅ **IMPLEMENTED**
- **Export Capabilities**: JSON and CSV export formats ✅ **IMPLEMENTED**
- **Processing Metrics**: Real-time processing time display ✅ **IMPLEMENTED**
- **Image Metadata**: Detailed file information and analysis ✅ **IMPLEMENTED**

### 🎨 **Modern User Interface**
- **Responsive Design**: Mobile-first design approach with Tailwind CSS ✅ **IMPLEMENTED**
- **Dark/Light Theme**: User preference theme switching ✅ **IMPLEMENTED**
- **Complete Internationalization**: Full Japanese and English interface with Vue I18n ✅ **IMPLEMENTED**
- **User Authentication**: JWT-based secure authentication system ✅ **IMPLEMENTED**
- **Modern Components**: Headless UI components with smooth transitions ✅ **IMPLEMENTED**
- **Accessibility**: Keyboard navigation and screen reader support ✅ **IMPLEMENTED**
- **Professional Design**: Clean, intuitive interface with visual feedback ✅ **IMPLEMENTED**

### 🔧 **System Management**
- **Model Management**: Upload, validate, and manage custom AI models ✅ **IMPLEMENTED**
- **User Profiles**: Personal settings and classification history ✅ **IMPLEMENTED**
- **System Monitoring**: Health checks and performance metrics ✅ **IMPLEMENTED**
- **Security Features**: File validation and threat detection ✅ **IMPLEMENTED**
- **Database Integration**: PostgreSQL with user data and history ✅ **IMPLEMENTED**
- **API Documentation**: Auto-generated OpenAPI/Swagger docs ✅ **IMPLEMENTED**

### 🔧 **Developer Features**
- **RESTful API**: Comprehensive API with OpenAPI/Swagger documentation ✅ **IMPLEMENTED**
- **Health Monitoring**: System health checks and performance metrics ✅ **IMPLEMENTED**
- **Containerized Deployment**: Docker and Docker Compose support ✅ **IMPLEMENTED**
- **Development Tools**: Hot reload, testing, and debugging utilities ✅ **IMPLEMENTED**
- **Type Safety**: Full TypeScript integration with strict typing ✅ **IMPLEMENTED**
- **Database Management**: PostgreSQL with migrations and indexing ✅ **IMPLEMENTED**
- **Security Middleware**: Multi-layer validation and authentication ✅ **IMPLEMENTED**

## Technology Stack

### Frontend Architecture
- **Framework**: Vue.js 3 with Composition API and TypeScript
- **Build System**: Vite 7.0 for fast development and optimized builds
- **Styling**: Tailwind CSS 3.4 with PostCSS and Autoprefixer
- **State Management**: Pinia for centralized state management
- **Routing**: Vue Router 4 for SPA navigation
- **Testing**: Vitest for unit testing, Playwright for E2E testing
- **Type Safety**: Full TypeScript integration with Vue TSC

### Backend Architecture
- **Framework**: Python FastAPI 0.115 with async/await support
- **API Documentation**: Auto-generated OpenAPI 3.0 documentation
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0 ORM and optimized indexing
- **Authentication**: JWT tokens with secure session management
- **File Handling**: Async file processing with multipart support
- **Validation**: Pydantic 2.10 for data validation and serialization
- **Caching**: Redis integration for performance optimization
- **Security**: Multi-layer security middleware with rate limiting

### AI/ML Integration
- **Deep Learning**: TensorFlow 2.18 and PyTorch 2.5 support with intelligent model selection
- **Computer Vision**: OpenCV 4.10 for advanced image preprocessing
- **Cloud AI**: Google Cloud Vision API integration with fallback support
- **Multi-modal AI**: Video, audio, and combined media classification
- **Image Processing**: Pillow 11.0 for format conversion and optimization
- **Model Management**: Dynamic model loading, custom model support, and marketplace
- **Performance**: GPU acceleration support with automatic optimization
- **Real-time Processing**: WebSocket-based streaming classification

### Infrastructure & DevOps
- **Containerization**: Docker and Docker Compose for development and production
- **Database**: PostgreSQL with connection pooling, migrations, and strategic indexing
- **Caching**: Redis for session storage, result caching, and real-time data
- **Reverse Proxy**: Nginx for static files and load balancing
- **Monitoring**: Enhanced health checks, system metrics, and comprehensive analytics dashboard
- **Environment Management**: Docker multi-stage builds for production deployment
- **Security**: Multi-layer security middleware, file validation, and threat detection
- **API Gateway**: Rate limiting, API key management, and usage tracking
- **Billing System**: Usage-based monetization with subscription tiers
- **Collaboration Tools**: Workspace management and team collaboration features

## Quick Start

### Prerequisites
- **Node.js** 22+ (recommended) or Node.js 20.19+
- **Python** 3.11 or higher
- **Docker** and Docker Compose (optional but recommended)
- **AI API Keys** (Google Cloud Vision API for cloud features)

### Installation

#### Option 1: Docker Development Environment (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/M-Ito-7310/image-classification-service.git
   cd image-classification-service
   ```

2. **Environment setup**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Configure your environment variables
   # Add your Google Cloud Vision API key if using cloud features
   ```

3. **Start with Docker Compose**
   ```bash
   # Start all services (frontend, backend, database)
   docker-compose up -d
   
   # Check service status
   docker-compose ps
   ```

4. **Access the application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Database**: localhost:5432 (PostgreSQL)

#### Option 2: Local Development Setup

1. **Backend setup**
   ```bash
   cd backend
   
   # Create Python virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start backend server
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend setup**
   ```bash
   cd frontend
   
   # Install Node.js dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

3. **Database setup** (Optional for basic functionality)
   ```bash
   # Using Docker for PostgreSQL
   docker run --name postgres-dev \
     -e POSTGRES_DB=image_classification \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -p 5432:5432 -d postgres:15
   ```

### Quick Test

1. **API Health Check**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

2. **Frontend Access**
   - Open http://localhost:3000 in your browser
   - Upload an image using the drag-and-drop interface
   - View classification results in real-time

## API Documentation

### Authentication
JWT-based authentication system with secure session management and API key support. Enterprise features require valid API keys.

### Core Endpoints

#### Image Classification
```http
POST /api/v1/classify
Content-Type: multipart/form-data

Parameters:
- file: Image file (required)
- model: Model name (optional, default: "auto")
- threshold: Confidence threshold (optional, default: 0.5)
```

#### Classification History
```http
GET /api/v1/history                  # Get user's classification history
GET /api/v1/history/{record_id}      # Get specific record
DELETE /api/v1/history/{record_id}   # Delete record
GET /api/v1/stats                   # Get classification statistics
```

#### User Authentication
```http
POST /api/v1/auth/register          # User registration
POST /api/v1/auth/login             # User login
GET /api/v1/auth/profile            # Get user profile
```

#### Model Management
```http
GET /api/v1/models                    # List available models
POST /api/v1/models/upload           # Upload custom model
GET /api/v1/models/custom            # List user's custom models
```


#### Health Check
```http
GET /api/v1/health                   # Basic health check
GET /api/v1/monitoring/health/detailed # Comprehensive health check
```

For complete API documentation, visit: http://localhost:8000/docs

## Project Structure

```
image-classification-service/
├── frontend/                 # Vue.js frontend application
│   ├── src/
│   │   ├── components/      # Vue components
│   │   │   ├── Upload/      # Single image upload system
│   │   │   ├── Results/     # Classification results display
│   │   │   ├── Auth/        # Authentication components
│   │   │   ├── Models/      # Model management UI
│   │   │   ├── Layout/      # Page layout components
│   │   │   └── Common/      # Reusable UI components
│   │   ├── views/           # Page components (11 total)
│   │   ├── stores/          # Pinia state management
│   │   ├── services/        # API service layer
│   │   ├── types/           # TypeScript type definitions
│   │   ├── i18n/           # Internationalization (ja/en)
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets
│   ├── tests/               # Frontend tests
│   └── package.json
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API routes (classification, models, history, health)
│   │   ├── core/           # Application configuration and settings
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── services/       # Business logic services
│   │   │   ├── classification_service.py  # AI classification logic
│   │   │   ├── image_service.py          # Image preprocessing
│   │   │   ├── security_service.py       # File security validation
│   │   │   └── cache_service.py          # Result caching
│   │   ├── routers/        # Authentication routes
│   │   └── utils/          # Utility functions
│   ├── tests/              # Backend tests
│   └── requirements.txt
├── docker/                   # Docker configuration files
│   ├── frontend.Dockerfile
│   ├── backend.Dockerfile
│   └── nginx.conf
├── docs/                     # Project documentation
│   ├── API.md              # API reference
│   ├── DEPLOYMENT.md       # Deployment guide
│   └── DEVELOPMENT.md      # Development guide
├── scripts/                  # Development and deployment scripts
├── docker-compose.yml       # Development environment setup
├── Makefile                 # Development commands
├── ROADMAP.md              # Development roadmap
└── README.md               # This file
```

## Development

### Backend Development
```bash
cd backend

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Code formatting
black .
isort .

# Type checking
mypy .

# Start development server
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend

# Development server with hot reload
npm run dev

# Type checking
npm run type-check

# Linting and formatting
npm run lint
npm run format

# Run unit tests
npm run test:unit

# Run E2E tests
npm run test:e2e

# Build for production
npm run build
```

### Development Commands (Makefile)
```bash
make dev          # Start development environment
make build        # Build all containers
make test         # Run all tests
make clean        # Clean up containers and volumes
make logs         # View application logs
```

## Environment Configuration

### Required Environment Variables
```env
# API Configuration
FASTAPI_ENV=development
API_HOST=0.0.0.0
API_PORT=8000

# Database Configuration  
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/image_classification

# AI Service Configuration
GOOGLE_CLOUD_VISION_API_KEY=your_api_key_here
HUGGING_FACE_API_KEY=your_hf_key_here

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp,bmp

# Security
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### Optional Configuration
```env
# Redis Cache (for production)
REDIS_URL=redis://localhost:6379

# Model Configuration
DEFAULT_MODEL=imagenet_mobilenet_v2
MODEL_CACHE_SIZE=2GB
GPU_ENABLED=false

# Monitoring
ENABLE_METRICS=true
LOG_LEVEL=INFO
```

## Testing

### Backend Testing
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# API tests
pytest tests/api/

# Coverage report
pytest --cov=app tests/
```

### Frontend Testing
```bash
# Unit tests with Vitest
npm run test:unit

# E2E tests with Playwright
npm run test:e2e

# Component testing
npm run test:component
```

## Performance & Monitoring

### Performance Metrics
- **API Response Time**: < 3 seconds for standard classification
- **Single Image Processing**: Optimized workflow with real-time feedback
- **Memory Usage**: Efficient for 2GB RAM minimum, optimized for 4GB+
- **File Processing**: Support for files up to 10MB with validation
- **Cache Performance**: Intelligent result caching for faster repeat queries
- **Database Performance**: PostgreSQL with optimized indexing

### Monitoring Features
- **Health Check Endpoints**: System status and dependency monitoring
- **Performance Metrics**: Response time and throughput tracking
- **Error Tracking**: Comprehensive error logging and reporting
- **Resource Monitoring**: CPU, memory, and GPU utilization
- **Cache Analytics**: Redis performance and hit rate monitoring
- **Security Monitoring**: File upload validation and threat detection

## Deployment

### Production Deployment

#### Docker Production Build
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

#### Cloud Deployment (AWS/GCP/Azure)
See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed cloud deployment guides.

### Environment-Specific Configurations
- **Development**: Hot reload, debug logging, development dependencies
- **Staging**: Production builds with debug symbols, test data
- **Production**: Optimized builds, security hardening, monitoring

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow TypeScript best practices for frontend development
- Use Python type hints and follow PEP 8 for backend development
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure Docker builds pass before submitting

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for detailed development phases and upcoming features.

**Current Status**: ✅ Core Production System - Single Image Classification (Complete)

### Development Progress
- ✅ **Phase 1**: Foundation and Architecture (100% Complete)
- ✅ **Phase 2**: AI Integration & UI Development (100% Complete)
- ✅ **Phase 3**: Core Features Implementation (100% Complete)
- ✅ **Phase 4**: Authentication & Security (100% Complete)
- ✅ **Phase 5**: Internationalization & UI Polish (100% Complete)
- ✅ **Optimization**: Simplified to Single Image Processing (100% Complete)

### Key Achievements
- 🎯 **Production-Ready Core**: Fully functional single image classification system
- 🔐 **Secure Authentication**: JWT-based user management with profile system
- 🌍 **Multi-Language Support**: Complete Japanese/English internationalization
- 🎨 **Professional UI/UX**: Modern, responsive design with dark/light themes
- ⚡ **Real AI Integration**: TensorFlow and PyTorch model support
- 📊 **Comprehensive Features**: History tracking, model management, export capabilities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Open an issue on GitHub
- Check the [API documentation](http://localhost:8000/docs) 
- Review the [development roadmap](./ROADMAP.md)
- Consult the [deployment guide](./docs/DEPLOYMENT.md)

---

## Documentation

For detailed development phases and roadmap, see [ROADMAP.md](./ROADMAP.md).

**日本語版ドキュメント**: [README.ja.md](./README.ja.md) | [ROADMAP.ja.md](./ROADMAP.ja.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.