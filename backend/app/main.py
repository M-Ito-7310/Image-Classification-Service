from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from pathlib import Path

from app.core.config import settings
from app.api.routes import classification, health, history, models
from app.routers import auth
from app.services.cache_service import cache_service
from app.core.database_indexes import optimize_database
from app.middleware.security import RateLimitMiddleware, SecurityHeadersMiddleware, RequestValidationMiddleware
from app.middleware.monetization import MonetizationMiddleware

# Ensure upload directory exists
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Image Classification Service...")
    print(f"Upload directory: {UPLOAD_DIR.absolute()}")
    
    # Initialize database optimization
    try:
        print("Optimizing database indexes...")
        optimize_database()
        print("Database optimization completed")
    except Exception as e:
        print(f"Database optimization warning: {e}")
    
    # Initialize cache service
    try:
        print("Connecting to Redis cache...")
        await cache_service.connect()
        print("Cache service initialized")
    except Exception as e:
        print(f"Cache service warning: {e}")
    
    # Initialize ML models here if needed
    
    yield
    
    # Shutdown
    print("Shutting down Image Classification Service...")
    
    # Cleanup cache connection
    try:
        await cache_service.disconnect()
        print("Cache service disconnected")
    except Exception as e:
        print(f"Cache disconnect warning: {e}")

# Create FastAPI application
app = FastAPI(
    title="Image Classification Service",
    description="AI-powered image classification and recognition API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add security middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestValidationMiddleware)
app.add_middleware(MonetizationMiddleware)
app.add_middleware(RateLimitMiddleware, calls_per_minute=60, calls_per_hour=1000)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(classification.router, prefix="/api/v1", tags=["classification"])
app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
app.include_router(auth.router, prefix="/api/v1", tags=["authentication"])
app.include_router(history.router, prefix="/api/v1", tags=["history"])

# Import monitoring router
from app.api.v1.endpoints.monitoring import router as monitoring_router
app.include_router(monitoring_router, prefix="/api/v1/monitoring", tags=["monitoring"])

# Import multi-modal router
from app.api.v1.endpoints.multimodal import router as multimodal_router
app.include_router(multimodal_router, prefix="/api/v1/multimodal", tags=["multimodal"])

# Import marketplace router
from app.api.v1.endpoints.marketplace import router as marketplace_router
app.include_router(marketplace_router, prefix="/api/v1/marketplace", tags=["marketplace"])

# Import real-time streaming router
from app.api.v1.endpoints.realtime import router as realtime_router
app.include_router(realtime_router, prefix="/api/v1/realtime", tags=["realtime"])

# Import collaboration router
from app.api.v1.endpoints.collaboration import router as collaboration_router
app.include_router(collaboration_router, prefix="/api/v1/collaboration", tags=["collaboration"])

# Import billing router
from app.api.v1.endpoints.billing import router as billing_router
app.include_router(billing_router, prefix="/api/v1/billing", tags=["billing"])

@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Welcome to Image Classification Service API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )