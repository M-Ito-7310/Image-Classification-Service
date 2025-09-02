# Deployment Guide - AI Image Classification Service

## Overview

This guide provides comprehensive instructions for deploying the AI Image Classification Service across different environments, from local development to production cloud deployment.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Development Deployment](#local-development-deployment)
- [Docker Production Deployment](#docker-production-deployment)
- [Cloud Deployment Options](#cloud-deployment-options)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring & Logging](#monitoring--logging)
- [Security Configuration](#security-configuration)
- [Scaling & Performance](#scaling--performance)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+), macOS 10.15+, Windows 10+
- **Memory**: 4GB RAM minimum, 8GB recommended for ML models
- **Storage**: 10GB available disk space
- **Network**: Stable internet connection for model downloads

### Required Software
- **Docker** 24.0+ and **Docker Compose** 2.20+
- **Node.js** 20.19+ or 22+ (for frontend development)
- **Python** 3.11+ (for backend development)
- **Git** for version control

### Cloud Requirements (Production)
- **Cloud Platform Account**: AWS, Google Cloud, or Azure
- **Domain Name**: For production deployment (optional)
- **SSL Certificate**: Let's Encrypt or commercial certificate

## Local Development Deployment

### Quick Start (Docker Compose)

1. **Clone and Setup**
   ```bash
   git clone https://github.com/M-Ito-7310/image-classification-service.git
   cd image-classification-service
   ```

2. **Environment Configuration**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit configuration (minimal setup)
   nano .env
   ```

3. **Start Services**
   ```bash
   # Start all services in background
   docker-compose up -d
   
   # Check service status
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   ```

4. **Verify Deployment**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Database**: postgresql://postgres:postgres@localhost:5432/image_classification

### Manual Development Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/image_classification"
export FASTAPI_ENV="development"

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Database Setup
```bash
# Start PostgreSQL with Docker
docker run --name postgres-dev \
  -e POSTGRES_DB=image_classification \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 -d postgres:15

# Run database migrations (when implemented)
cd backend
alembic upgrade head
```

## Docker Production Deployment

### Production Docker Compose

Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - FASTAPI_ENV=production
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/${DB_NAME}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Production Environment Variables

Create `.env.prod`:
```env
# Database Configuration
DB_NAME=image_classification_prod
DB_USER=postgres
DB_PASSWORD=your_secure_password_here

# API Configuration
FASTAPI_ENV=production
SECRET_KEY=your-very-secure-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# AI Service Configuration
GOOGLE_CLOUD_VISION_API_KEY=your_google_api_key
HUGGING_FACE_API_KEY=your_hf_api_key

# Security Configuration
CORS_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Performance Configuration
REDIS_URL=redis://redis:6379
MAX_WORKERS=4
MAX_FILE_SIZE=10485760

# Monitoring
LOG_LEVEL=INFO
ENABLE_METRICS=true
SENTRY_DSN=your_sentry_dsn_here
```

### Production Deployment Commands

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d --build

# Check service health
docker-compose -f docker-compose.prod.yml ps

# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Scale backend services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

## Cloud Deployment Options

### AWS Deployment

#### Option 1: ECS with Fargate

1. **Prepare ECR Repository**
   ```bash
   # Create ECR repositories
   aws ecr create-repository --repository-name image-classifier-frontend
   aws ecr create-repository --repository-name image-classifier-backend
   
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
   ```

2. **Build and Push Images**
   ```bash
   # Build images
   docker build -t image-classifier-frontend:latest ./frontend
   docker build -t image-classifier-backend:latest ./backend
   
   # Tag and push
   docker tag image-classifier-frontend:latest your-account.dkr.ecr.us-east-1.amazonaws.com/image-classifier-frontend:latest
   docker push your-account.dkr.ecr.us-east-1.amazonaws.com/image-classifier-frontend:latest
   ```

3. **ECS Task Definition** (`task-definition.json`):
   ```json
   {
     "family": "image-classifier",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "1024",
     "memory": "2048",
     "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
     "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "backend",
         "image": "your-account.dkr.ecr.us-east-1.amazonaws.com/image-classifier-backend:latest",
         "portMappings": [{"containerPort": 8000}],
         "environment": [
           {"name": "FASTAPI_ENV", "value": "production"},
           {"name": "DATABASE_URL", "value": "postgresql://..."}
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/image-classifier",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

#### Option 2: EC2 with Auto Scaling

1. **Launch Template**
   ```bash
   # Create launch template with user data
   aws ec2 create-launch-template \
     --launch-template-name image-classifier-template \
     --launch-template-data file://launch-template.json
   ```

2. **Auto Scaling Group**
   ```bash
   # Create auto scaling group
   aws autoscaling create-auto-scaling-group \
     --auto-scaling-group-name image-classifier-asg \
     --launch-template LaunchTemplateName=image-classifier-template \
     --min-size 2 --max-size 10 --desired-capacity 2
   ```

### Google Cloud Platform Deployment

#### Cloud Run Deployment

1. **Build and Deploy Backend**
   ```bash
   # Set project
   gcloud config set project your-project-id
   
   # Build and deploy backend
   cd backend
   gcloud run deploy image-classifier-backend \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --memory 2Gi \
     --cpu 1 \
     --max-instances 10
   ```

2. **Deploy Frontend to Firebase Hosting**
   ```bash
   cd frontend
   npm run build
   
   # Initialize Firebase
   firebase init hosting
   
   # Deploy
   firebase deploy
   ```

### Azure Deployment

#### Container Instances

1. **Create Resource Group**
   ```bash
   az group create --name image-classifier-rg --location eastus
   ```

2. **Deploy Container Group**
   ```bash
   az container create \
     --resource-group image-classifier-rg \
     --name image-classifier \
     --image your-registry.azurecr.io/image-classifier:latest \
     --dns-name-label image-classifier \
     --ports 80 8000
   ```

## Environment Configuration

### Environment Variables Reference

#### Core Application Settings
```env
# Application Environment
FASTAPI_ENV=development|staging|production
DEBUG=false
SECRET_KEY=your-secret-key

# Database Configuration
DATABASE_URL=postgresql://user:pass@host:port/db
DB_ECHO=false
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# Redis Configuration (Caching)
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=your-redis-password
REDIS_DB=0

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp,bmp
UPLOAD_FOLDER=/tmp/uploads

# AI Model Configuration
DEFAULT_MODEL=imagenet_mobilenet_v2
MODEL_CACHE_SIZE=2147483648  # 2GB
GPU_ENABLED=false
MODEL_DOWNLOAD_TIMEOUT=300
```

#### AI Service Integration
```env
# Google Cloud Vision API
GOOGLE_CLOUD_VISION_API_KEY=your_api_key
GOOGLE_CLOUD_PROJECT_ID=your_project_id

# Hugging Face
HUGGING_FACE_API_KEY=your_hf_api_key
HUGGING_FACE_MODEL_CACHE=/models/cache

# OpenAI (if used)
OPENAI_API_KEY=your_openai_key
```

#### Security Configuration
```env
# CORS Settings
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE
CORS_ALLOW_HEADERS=*

# JWT Authentication (Phase 3)
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
REFRESH_TOKEN_EXPIRATION_DAYS=30

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_PER_DAY=10000
```

#### Monitoring & Logging
```env
# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/var/log/app.log

# Monitoring Services
SENTRY_DSN=your_sentry_dsn
NEW_RELIC_LICENSE_KEY=your_newrelic_key
DATADOG_API_KEY=your_datadog_key

# Health Check Configuration
HEALTH_CHECK_TIMEOUT=30
HEALTH_CHECK_INTERVAL=60
```

## Database Setup

### PostgreSQL Production Setup

#### 1. Database Creation
```sql
-- Create database and user
CREATE DATABASE image_classification_prod;
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE image_classification_prod TO app_user;

-- Enable extensions
\c image_classification_prod
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";  -- For future vector operations
```

#### 2. Connection Pooling with pgbouncer
```ini
# pgbouncer.ini
[databases]
image_classification_prod = host=localhost port=5432 dbname=image_classification_prod

[pgbouncer]
pool_mode = transaction
listen_port = 6432
listen_addr = 0.0.0.0
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
logfile = /var/log/pgbouncer/pgbouncer.log
pidfile = /var/run/pgbouncer/pgbouncer.pid
admin_users = postgres
```

#### 3. Database Migrations (When Implemented)
```bash
# Create migration
cd backend
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head

# Production migration command
docker-compose exec backend alembic upgrade head
```

### Database Backup Strategy

#### 1. Automated Backups
```bash
#!/bin/bash
# backup-db.sh

DB_NAME="image_classification_prod"
BACKUP_DIR="/backups/postgresql"
DATE=$(date +"%Y%m%d_%H%M%S")

# Create backup
docker exec postgres-container pg_dump -U postgres $DB_NAME > "$BACKUP_DIR/backup_${DATE}.sql"

# Compress backup
gzip "$BACKUP_DIR/backup_${DATE}.sql"

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: backup_${DATE}.sql.gz"
```

#### 2. Backup Restoration
```bash
# Restore from backup
gunzip backup_20250901_120000.sql.gz
docker exec -i postgres-container psql -U postgres image_classification_prod < backup_20250901_120000.sql
```

## CI/CD Pipeline

### GitHub Actions Workflow

#### `.github/workflows/deploy.yml`
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install backend dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run backend tests
      run: |
        cd backend
        pytest tests/ -v --cov=app --cov-report=xml
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '20'
    
    - name: Install frontend dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm run test:unit
        npm run lint
        npm run type-check
    
    - name: Build frontend
      run: |
        cd frontend
        npm run build

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Login to Amazon ECR
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build and push backend image
      run: |
        cd backend
        docker build -t $ECR_REGISTRY/image-classifier-backend:$GITHUB_SHA .
        docker push $ECR_REGISTRY/image-classifier-backend:$GITHUB_SHA
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
    
    - name: Build and push frontend image
      run: |
        cd frontend
        docker build -t $ECR_REGISTRY/image-classifier-frontend:$GITHUB_SHA .
        docker push $ECR_REGISTRY/image-classifier-frontend:$GITHUB_SHA
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service \
          --cluster image-classifier-cluster \
          --service image-classifier-service \
          --force-new-deployment
```

### Deployment Scripts

#### `scripts/deploy.sh`
```bash
#!/bin/bash

set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}

echo "Deploying version $VERSION to $ENVIRONMENT environment..."

case $ENVIRONMENT in
  staging)
    docker-compose -f docker-compose.staging.yml down
    docker-compose -f docker-compose.staging.yml pull
    docker-compose -f docker-compose.staging.yml up -d
    ;;
  production)
    # Blue-green deployment
    docker-compose -f docker-compose.prod.yml up -d --scale backend=6
    sleep 30
    docker-compose -f docker-compose.prod.yml up -d --scale backend=3 --remove-orphans
    ;;
  *)
    echo "Unknown environment: $ENVIRONMENT"
    exit 1
    ;;
esac

echo "Deployment completed successfully!"
```

## Monitoring & Logging

### Application Monitoring

#### Health Check Endpoints
```python
# backend/app/api/v1/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import redis
import psutil

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    checks = {}
    
    # Database check
    try:
        db.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {e}"
    
    # Redis check
    try:
        r = redis.Redis.from_url("redis://localhost:6379")
        r.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {e}"
    
    # System metrics
    checks["system"] = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent
    }
    
    return {"status": "healthy", "checks": checks}
```

#### Prometheus Metrics
```python
# backend/app/middleware/metrics.py
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Request, Response
import time

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])

async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    return response
```

### Logging Configuration

#### Structured Logging Setup
```python
# backend/app/core/logging.py
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging():
    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    logHandler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    return logger
```

#### Log Aggregation with Filebeat
```yaml
# filebeat.yml
filebeat.inputs:
- type: container
  paths:
    - /var/lib/docker/containers/*/*.log
  processors:
  - add_docker_metadata: ~

output.elasticsearch:
  hosts: ["elasticsearch:9200"]

setup.kibana:
  host: "kibana:5601"
```

## Security Configuration

### SSL/TLS Setup

#### Let's Encrypt with Certbot
```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Nginx SSL Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "strict-origin-when-cross-origin";
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Security Hardening

#### Docker Security
```dockerfile
# Use non-root user
FROM python:3.11-slim
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Security scanning
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Remove unnecessary packages
RUN apt-get autoremove -y && apt-get clean
```

#### Environment Security
```bash
# Set proper file permissions
chmod 600 .env
chmod 600 secrets/*

# Use Docker secrets for sensitive data
echo "db_password_here" | docker secret create db_password -
```

## Scaling & Performance

### Horizontal Scaling

#### Load Balancer Configuration (AWS ALB)
```json
{
  "Type": "AWS::ElasticLoadBalancingV2::LoadBalancer",
  "Properties": {
    "Name": "image-classifier-alb",
    "Type": "application",
    "Scheme": "internet-facing",
    "SecurityGroups": [{"Ref": "ALBSecurityGroup"}],
    "Subnets": [{"Ref": "PublicSubnet1"}, {"Ref": "PublicSubnet2"}]
  }
}
```

#### Auto Scaling Configuration
```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  backend:
    image: image-classifier-backend:latest
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
```

### Performance Optimization

#### Redis Caching Strategy
```python
# backend/app/services/cache.py
import redis
import json
from typing import Optional

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
    
    async def get_classification_cache(self, image_hash: str) -> Optional[dict]:
        cached = self.redis.get(f"classification:{image_hash}")
        if cached:
            return json.loads(cached)
        return None
    
    async def set_classification_cache(self, image_hash: str, result: dict, ttl: int = 3600):
        self.redis.setex(
            f"classification:{image_hash}",
            ttl,
            json.dumps(result)
        )
```

#### Database Query Optimization
```sql
-- Add indexes for performance
CREATE INDEX idx_classifications_created_at ON classifications(created_at);
CREATE INDEX idx_classifications_user_id ON classifications(user_id);
CREATE INDEX idx_classifications_model_name ON classifications(model_name);

-- Partitioning for large tables (if needed)
CREATE TABLE classifications_2025_09 PARTITION OF classifications 
FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');
```

## Troubleshooting

### Common Issues

#### 1. Container Memory Issues
```bash
# Check container memory usage
docker stats

# Increase memory limits
docker-compose up -d --scale backend=2
```

#### 2. Database Connection Issues
```bash
# Check database connectivity
docker-compose exec backend python -c "
from app.database import engine
try:
    engine.connect()
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
"
```

#### 3. Model Loading Issues
```bash
# Check model directory
docker-compose exec backend ls -la /models/

# Download models manually
docker-compose exec backend python -c "
from app.services.ai.model_loader import download_models
download_models()
"
```

### Performance Troubleshooting

#### 1. Slow API Responses
```bash
# Profile API endpoints
docker-compose exec backend python -m cProfile -s cumtime app/main.py

# Check database query performance
docker-compose exec db psql -U postgres -d image_classification_prod -c "
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;"
```

#### 2. High Memory Usage
```bash
# Monitor memory usage
docker-compose exec backend python -c "
import psutil
print(f'Memory usage: {psutil.virtual_memory().percent}%')
print(f'Available memory: {psutil.virtual_memory().available / 1024 / 1024 / 1024:.2f} GB')
"

# Check for memory leaks
docker-compose exec backend python -m memory_profiler app/main.py
```

### Log Analysis

#### Application Logs
```bash
# View application logs
docker-compose logs -f backend | grep ERROR

# Search for specific patterns
docker-compose logs backend | grep "classification" | tail -100

# Export logs for analysis
docker-compose logs --no-color backend > backend.log
```

#### System Monitoring
```bash
# Check system resources
docker system df
docker system prune -f

# Monitor container performance
docker exec backend top
docker exec backend iostat 1 5
```

## Maintenance

### Regular Maintenance Tasks

#### 1. System Updates
```bash
#!/bin/bash
# maintenance/update-system.sh

# Update base images
docker pull postgres:15
docker pull redis:7-alpine
docker pull nginx:alpine

# Rebuild application images
docker-compose build --no-cache

# Update dependencies
cd backend && pip list --outdated
cd frontend && npm audit
```

#### 2. Database Maintenance
```bash
#!/bin/bash
# maintenance/db-maintenance.sh

# Run database maintenance
docker-compose exec db psql -U postgres -d image_classification_prod -c "
VACUUM ANALYZE;
REINDEX DATABASE image_classification_prod;
"

# Update statistics
docker-compose exec db psql -U postgres -d image_classification_prod -c "
ANALYZE;
"
```

#### 3. Log Rotation
```bash
# /etc/logrotate.d/image-classifier
/var/log/image-classifier/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
}
```

### Backup and Recovery

#### Full System Backup
```bash
#!/bin/bash
# scripts/full-backup.sh

BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/$BACKUP_DATE"

mkdir -p $BACKUP_DIR

# Database backup
docker-compose exec db pg_dumpall -U postgres > $BACKUP_DIR/database.sql

# Application files backup
tar -czf $BACKUP_DIR/application.tar.gz \
    --exclude='*/node_modules' \
    --exclude='*/__pycache__' \
    --exclude='*/venv' \
    .

# Upload to cloud storage (if configured)
aws s3 cp $BACKUP_DIR/ s3://your-backup-bucket/$BACKUP_DATE/ --recursive

echo "Backup completed: $BACKUP_DIR"
```

---

## Support and Resources

### Documentation
- **API Reference**: [docs/API.md](./API.md)
- **Development Guide**: [README.md](../README.md)
- **Project Roadmap**: [ROADMAP.md](../ROADMAP.md)

### Monitoring Dashboards
- **Application**: http://localhost:3000/admin/dashboard
- **API Metrics**: http://localhost:8000/metrics
- **System Health**: http://localhost:8000/health

### Emergency Contacts
- **Technical Lead**: [Contact Information]
- **DevOps Team**: [Contact Information]
- **On-Call Engineer**: [Contact Information]

---

**Last Updated**: September 1, 2025  
**Version**: 1.0  
**Next Review**: Phase 4 (Production Optimization)

For the most current deployment procedures, always refer to the project repository and consult with the development team before making production changes.