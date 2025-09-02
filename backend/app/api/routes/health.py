from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Dict, Any
import sys
import platform
import psutil
import os

from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring service status.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }

@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with system information.
    """
    # System information
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT
        },
        "system": {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": sys.version,
            "cpu_count": psutil.cpu_count(),
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percentage": memory.percent
            },
            "disk": {
                "total": disk.total,
                "free": disk.free,
                "used": disk.used,
                "percentage": (disk.used / disk.total) * 100
            }
        },
        "upload_directory": {
            "path": settings.UPLOAD_DIR,
            "exists": os.path.exists(settings.UPLOAD_DIR)
        }
    }

@router.get("/ping")
async def ping():
    """
    Simple ping endpoint.
    """
    return {"message": "pong"}