# AI Image Classification Service / AI画像分類・認識サービス

[![Project Status](https://img.shields.io/badge/status-Phase%203%20Complete-brightgreen.svg)](https://github.com/M-Ito-7310/image-classification-service)
[![Python](https://img.shields.io/badge/python-3.11%2B-green.svg)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/vue.js-3.5-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-blue.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Languages**: English | [日本語](#日本語版)

An AI-powered image classification and recognition web service that provides intelligent image analysis capabilities. Built with modern web technologies and production-ready architecture, featuring real-time image processing with multiple AI model support.

## Overview

This project demonstrates advanced AI/ML integration, modern web development practices, and scalable architecture design. Built as a comprehensive portfolio project showcasing full-stack development skills with AI integration, it combines cutting-edge machine learning technology with intuitive user interfaces.

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
- **Multi-Model AI Classification**: Support for TensorFlow, PyTorch, and Google Cloud Vision API
- **Real-time Processing**: Instant image analysis with streaming results
- **Batch Processing**: Multiple image classification with progress tracking ✅ **COMPLETED**
- **Smart Image Preprocessing**: Automatic resizing, normalization, and optimization ✅ **COMPLETED**
- **Confidence Scoring**: Detailed prediction confidence with threshold filtering
- **Custom Model Support**: Upload and use custom trained models ✅ **COMPLETED**
- **Webcam Integration**: Real-time camera capture and classification ✅ **COMPLETED** ✅ **COMPLETED**

### 📤 **Advanced Upload System**
- **Drag & Drop Interface**: Modern file upload experience with visual feedback
- **Multiple Format Support**: JPEG, PNG, WebP, BMP image formats
- **File Size Management**: Intelligent compression and size optimization
- **Preview System**: Real-time image preview before processing
- **Progress Tracking**: Upload and processing progress indicators

### 📊 **Results & Analytics**
- **Interactive Results Display**: Visual classification results with confidence meters
- **Classification History**: Persistent storage of analysis results
- **Export Capabilities**: JSON, CSV, and PDF export formats
- **Performance Metrics**: Processing time and accuracy statistics
- **Comparison Tools**: Side-by-side result comparison

### 🎨 **Modern User Interface**
- **Responsive Design**: Mobile-first design approach with Tailwind CSS
- **Dark/Light Theme**: User preference theme switching
- **Complete Internationalization**: Full Japanese and English interface with Vue I18n ✅ **COMPLETED**
- **User Authentication**: JWT-based secure authentication system ✅ **COMPLETED**
- **Real-time Updates**: WebSocket integration for live processing updates
- **Accessibility**: WCAG 2.1 AA compliance for inclusive design

### 🔧 **Developer Features**
- **RESTful API**: Comprehensive API with OpenAPI/Swagger documentation
- **Health Monitoring**: System health checks and performance metrics
- **Containerized Deployment**: Docker and Docker Compose support
- **Development Tools**: Hot reload, testing, and debugging utilities
- **CI/CD Ready**: GitHub Actions workflow and deployment automation

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
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0 ORM
- **Authentication**: JWT tokens with secure session management
- **File Handling**: Async file processing with multipart support
- **Validation**: Pydantic 2.10 for data validation and serialization

### AI/ML Integration
- **Deep Learning**: TensorFlow 2.18 and PyTorch 2.5 support
- **Computer Vision**: OpenCV 4.10 for image preprocessing
- **Cloud AI**: Google Cloud Vision API integration
- **Image Processing**: Pillow 11.0 for format conversion and optimization
- **Model Management**: Dynamic model loading and switching
- **Performance**: GPU acceleration support for faster inference

### Infrastructure & DevOps
- **Containerization**: Docker and Docker Compose for development
- **Database**: PostgreSQL with connection pooling and migrations
- **Reverse Proxy**: Nginx for static files and load balancing
- **Monitoring**: Health checks and performance metrics
- **Environment Management**: Docker multi-stage builds for production

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
Currently using development mode. JWT authentication will be implemented in Phase 3.

### Core Endpoints

#### Image Classification
```http
POST /api/v1/classify
Content-Type: multipart/form-data

Parameters:
- file: Image file (required)
- model: Model name (optional, default: "default")
- threshold: Confidence threshold (optional, default: 0.5)
```

**Response Example:**
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
  "processing_time": 1.23,
  "model_used": "imagenet_mobilenet_v2"
}
```

#### Model Management
```http
GET /api/v1/models
```

**Response:**
```json
{
  "available_models": [
    {
      "name": "imagenet_mobilenet_v2",
      "description": "MobileNet v2 trained on ImageNet",
      "classes": 1000,
      "input_size": [224, 224],
      "status": "active"
    }
  ]
}
```

#### Health Check
```http
GET /api/v1/health
```

For complete API documentation, visit: http://localhost:8000/docs

## Project Structure

```
image-classification-service/
├── frontend/                 # Vue.js frontend application
│   ├── src/
│   │   ├── components/      # Vue components
│   │   │   ├── Upload/      # Image upload components
│   │   │   ├── Results/     # Classification results display
│   │   │   ├── History/     # Classification history
│   │   │   └── Common/      # Reusable UI components
│   │   ├── views/           # Page components
│   │   ├── stores/          # Pinia state management
│   │   ├── services/        # API service layer
│   │   ├── types/           # TypeScript type definitions
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets
│   ├── tests/               # Frontend tests
│   └── package.json
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   │   └── v1/         # API version 1
│   │   ├── core/           # Application configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   ├── ai/         # AI/ML services
│   │   │   └── image/      # Image processing services
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
- **API Response Time**: < 2 seconds for standard classification
- **Batch Processing**: Support for up to 50 images simultaneously
- **Memory Usage**: Optimized for 4GB RAM minimum
- **GPU Acceleration**: Optional CUDA support for faster inference

### Monitoring Features
- **Health Check Endpoints**: System status and dependency monitoring
- **Performance Metrics**: Response time and throughput tracking
- **Error Tracking**: Comprehensive error logging and reporting
- **Resource Monitoring**: CPU, memory, and GPU utilization

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

**Current Status**: 🚀 Phase 3 - Advanced Features (In Progress)

### Development Progress
- ✅ **Phase 1**: Foundation and Architecture (100% Complete)
- ✅ **Phase 2**: AI Integration & UI Development (100% Complete)
- 🔄 **Phase 3**: Advanced Features (65% Complete - Authentication & I18n Done)
- ⏳ **Phase 4**: Production Optimization (Planned)
- ⏳ **Phase 5**: Deployment & Monitoring (Planned)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Open an issue on GitHub
- Check the [API documentation](http://localhost:8000/docs) 
- Review the [development roadmap](./ROADMAP.md)
- Consult the [deployment guide](./docs/DEPLOYMENT.md)

---

# 日本語版

## 概要

AIを活用した画像分類・認識Webサービスです。最新のWeb技術と本格的なアーキテクチャで構築され、複数のAIモデルに対応したリアルタイム画像処理機能を提供します。

## 主要機能

### 🔍 **画像処理機能**
- **マルチモデルAI分類**: TensorFlow、PyTorch、Google Cloud Vision APIに対応
- **リアルタイム処理**: 即座の画像解析とストリーミング結果表示
- **バッチ処理**: 複数画像の同時分類と進捗追跡
- **スマート前処理**: 自動リサイズ、正規化、最適化
- **信頼度スコア**: 詳細な予測信頼度と閾値フィルタリング

### 📤 **高度なアップロードシステム**
- **ドラッグ&ドロップ**: モダンなファイルアップロード体験
- **複数形式対応**: JPEG、PNG、WebP、BMP画像形式
- **ファイルサイズ管理**: インテリジェントな圧縮とサイズ最適化
- **プレビューシステム**: 処理前のリアルタイム画像プレビュー

### 📊 **結果・分析機能**
- **インタラクティブ結果表示**: 視覚的な分類結果と信頼度メーター
- **分類履歴**: 解析結果の永続化ストレージ
- **エクスポート機能**: JSON、CSV、PDFエクスポート形式
- **パフォーマンス指標**: 処理時間と精度統計

### 🎨 **モダンユーザーインターフェース**
- **レスポンシブデザイン**: Tailwind CSSによるモバイルファースト設計
- **ダーク/ライトテーマ**: ユーザー設定によるテーマ切り替え
- **多言語対応**: Vue I18nによる完全な日本語・英語インターフェース
- **リアルタイム更新**: WebSocket統合によるライブ処理更新

## 技術スタック

### フロントエンド
- **Vue.js 3** + Composition API + TypeScript
- **Vite 7.0** による高速開発・最適化ビルド
- **Tailwind CSS 3.4** + PostCSS
- **Pinia** による状態管理
- **Vue Router 4** によるSPAナビゲーション

### バックエンド
- **Python FastAPI 0.115** + 非同期処理
- **PostgreSQL 15+** + SQLAlchemy 2.0 ORM
- **JWT認証** によるセキュアなセッション管理
- **Pydantic 2.10** によるデータ検証

### AI/ML統合
- **TensorFlow 2.18** と **PyTorch 2.5** 対応
- **OpenCV 4.10** による画像前処理
- **Google Cloud Vision API** 統合
- **Pillow 11.0** による形式変換・最適化

## クイックスタート

### 前提条件
- **Node.js** 22+ または 20.19+
- **Python** 3.11 以上
- **Docker** と Docker Compose（推奨）

### インストール

#### Docker開発環境（推奨）

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/M-Ito-7310/image-classification-service.git
   cd image-classification-service
   ```

2. **Docker Composeで起動**
   ```bash
   docker-compose up -d
   ```

3. **アプリケーションへのアクセス**
   - **フロントエンド**: http://localhost:3000
   - **バックエンドAPI**: http://localhost:8000
   - **API文書**: http://localhost:8000/docs

## Troubleshooting / トラブルシューティング

### Backend Server Issues / バックエンドサーバーの問題

**Issue**: `uvicorn` command not recognized / `uvicorn` コマンドが認識されない
```bash
'uvicorn' は、内部コマンドまたは外部コマンド、操作可能なプログラムまたはバッチ ファイルとして認識されていません。
```

**Solution**: Use Python module execution / Pythonモジュール実行を使用
```bash
# Instead of: uvicorn main:app --reload
# Use: 
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Import Errors / インポートエラー

**Issue**: Module import errors / モジュールインポートエラー
```bash
ERROR:    Error loading ASGI app. Could not import module "main".
```

**Solution**: Ensure correct module path / 正しいモジュールパスを確認
- Use `app.main:app` not `main:app`
- Run from the `backend` directory / `backend` ディレクトリから実行

### Port Conflicts / ポート競合

**Issue**: Port already in use / ポートが既に使用中

**Solution**: Change port or kill existing process / ポートを変更するか既存プロセスを終了
```bash
# Change port / ポートを変更
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Find and kill process using port 8000 / ポート8000を使用しているプロセスを確認・終了
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID_NUMBER>
```

## 開発ロードマップ

詳細な開発フェーズと今後の機能については[ROADMAP.md](./ROADMAP.md)をご覧ください。

**現在の状況**: ✅ Phase 3 - 高度機能開発（100%完了）

### 🎯 **最新の実装状況** (2025年9月2日現在)

#### ✅ **完了済み機能**
- **AIモデル統合**: TensorFlow (MobileNetV2, ResNet50) + PyTorch (ResNet18) - 100%完了
- **REST API**: 全エンドポイント実装・テスト済み - 100%完了  
- **フロントエンド**: Vue.js 3 + TypeScript + Tailwind CSS - 100%完了
- **状態管理**: Pinia stores (upload, classification, error, settings) - 100%完了
- **コンポーネント**: Layout, Upload, Results, Views - 100%完了
- **エラーハンドリング**: 包括的エラー管理システム - 100%完了
- **国際化対応**: Vue I18n による完全な日英二言語対応 - 100%完了 ✅
- **ユーザー認証**: JWT認証とユーザー管理システム - 100%完了 ⭐NEW

#### ✅ **完了済み（Phase 3）**
- **カスタムモデル管理**: アップロード・検証・使用システム - 100%完了
- **バッチ処理機能**: 複数画像同時分類（最大10ファイル） - 100%完了
- **ウェブカメラ統合**: リアルタイム撮影・分類機能 - 100%完了
- **パフォーマンス最適化**: 画像圧縮・キャッシュ・メトリクス - 100%完了

#### 📊 **アクティブ機能**
- ✅ リアルタイム画像分類 (4モデル対応)
- ✅ 複数形式対応 (JPEG, PNG, WebP, BMP)
- ✅ 分類履歴管理
- ✅ 設定カスタマイズ
- ✅ エラー回復システム
- ✅ カスタムモデル管理システム
- ✅ バッチ処理（最大10ファイル同時）
- ✅ ウェブカメラリアルタイム分類
- ✅ 画像最適化・キャッシュシステム

## ライセンス

このプロジェクトはMITライセンスの下で公開されています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。