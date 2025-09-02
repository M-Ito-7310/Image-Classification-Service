from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Dict, Any
import sys
import platform
import psutil
import os
import asyncio

from app.core.config import settings
from app.services.cache_service import cache_service
from app.core.database import engine

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
    Detailed health check with system information and dependencies.
    """
    # System information
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Check database connectivity
    db_status = "unknown"
    try:
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check cache connectivity
    cache_stats = await cache_service.get_cache_stats()
    
    # Calculate overall health score
    health_score = 100
    if db_status != "connected":
        health_score -= 30
    if not cache_stats.get("enabled", False):
        health_score -= 10
    if memory.percent > 85:
        health_score -= 20
    if disk.used / disk.total > 0.9:
        health_score -= 15
    
    overall_status = "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy"
    
    return {
        "status": overall_status,
        "health_score": health_score,
        "timestamp": datetime.utcnow().isoformat(),
        "service": {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT
        },
        "dependencies": {
            "database": {
                "status": db_status,
                "url": settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else "N/A"
            },
            "cache": cache_stats
        },
        "system": {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": sys.version,
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(interval=1),
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
                "percentage": round((disk.used / disk.total) * 100, 2)
            }
        },
        "upload_directory": {
            "path": settings.UPLOAD_DIR,
            "exists": os.path.exists(settings.UPLOAD_DIR)
        }
    }

@router.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Application performance metrics for monitoring.
    """
    try:
        # Cache metrics
        cache_stats = await cache_service.get_cache_stats()
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # Process metrics
        process = psutil.Process()
        process_memory = process.memory_info()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "cache": cache_stats,
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            },
            "process": {
                "pid": process.pid,
                "memory_rss_mb": round(process_memory.rss / (1024**2), 2),
                "memory_vms_mb": round(process_memory.vms / (1024**2), 2),
                "cpu_percent": process.cpu_percent(),
                "num_threads": process.num_threads(),
                "create_time": datetime.fromtimestamp(process.create_time()).isoformat()
            }
        }
        
    except Exception as e:
        return {
            "error": f"Metrics collection failed: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        }

@router.get("/ping")
async def ping():
    """
    Simple ping endpoint.
    """
    return {"message": "pong", "timestamp": datetime.utcnow().isoformat()}