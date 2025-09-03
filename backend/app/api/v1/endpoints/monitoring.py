"""
Advanced monitoring endpoints for production observability.
"""

import time
import psutil
from typing import Dict, Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, func
import redis.asyncio as redis

from app.core.database import get_database
from app.services.cache_service import CacheService
from app.models.classification import ClassificationRecord
from app.models.users import User

router = APIRouter()

@router.get("/system")
async def get_system_metrics() -> Dict[str, Any]:
    """Get comprehensive system performance metrics."""
    
    # CPU and Memory metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Process-specific metrics
    process = psutil.Process()
    process_memory = process.memory_info()
    
    # Network metrics
    network = psutil.net_io_counters()
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": cpu_percent,
            "cpu_count": psutil.cpu_count(),
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
                "free": memory.free
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            }
        },
        "process": {
            "memory_rss": process_memory.rss,
            "memory_vms": process_memory.vms,
            "cpu_percent": process.cpu_percent(),
            "num_threads": process.num_threads(),
            "open_files": len(process.open_files())
        },
        "network": {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_recv": network.packets_recv
        }
    }

@router.get("/database")
async def get_database_metrics(db: AsyncSession = Depends(get_database)) -> Dict[str, Any]:
    """Get database performance and usage metrics."""
    
    try:
        # Connection and activity stats
        connection_query = text("""
            SELECT 
                count(*) as total_connections,
                count(*) FILTER (WHERE state = 'active') as active_connections,
                count(*) FILTER (WHERE state = 'idle') as idle_connections
            FROM pg_stat_activity
            WHERE backend_type = 'client backend'
        """)
        
        # Database size and table statistics
        size_query = text("""
            SELECT 
                pg_database_size(current_database()) as database_size,
                (SELECT count(*) FROM users) as user_count,
                (SELECT count(*) FROM classification_records) as classification_count,
                (SELECT count(*) FROM custom_models) as custom_model_count
        """)
        
        # Recent activity
        activity_query = text("""
            SELECT 
                COUNT(*) as classifications_last_hour
            FROM classification_records 
            WHERE created_at > NOW() - INTERVAL '1 hour'
        """)
        
        # Execute queries in parallel
        connection_result = await db.execute(connection_query)
        size_result = await db.execute(size_query)
        activity_result = await db.execute(activity_query)
        
        connections = connection_result.fetchone()
        sizes = size_result.fetchone()
        activity = activity_result.fetchone()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "connections": {
                "total": connections.total_connections,
                "active": connections.active_connections,
                "idle": connections.idle_connections
            },
            "storage": {
                "database_size_bytes": sizes.database_size,
                "user_count": sizes.user_count,
                "classification_count": sizes.classification_count,
                "custom_model_count": sizes.custom_model_count
            },
            "activity": {
                "classifications_last_hour": activity.classifications_last_hour
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database metrics collection failed: {str(e)}"
        )

@router.get("/cache")
async def get_cache_metrics() -> Dict[str, Any]:
    """Get Redis cache performance metrics."""
    
    cache_service = CacheService()
    
    try:
        # Get cache statistics
        stats = await cache_service.get_cache_stats()
        
        # Additional Redis info
        if cache_service.redis_client:
            info = await cache_service.redis_client.info()
            memory_info = await cache_service.redis_client.info("memory")
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "connected",
                "performance": stats,
                "memory": {
                    "used_memory": memory_info.get("used_memory", 0),
                    "used_memory_human": memory_info.get("used_memory_human", "0B"),
                    "used_memory_peak": memory_info.get("used_memory_peak", 0),
                    "memory_fragmentation_ratio": memory_info.get("mem_fragmentation_ratio", 0)
                },
                "connections": {
                    "connected_clients": info.get("connected_clients", 0),
                    "blocked_clients": info.get("blocked_clients", 0),
                    "total_connections_received": info.get("total_connections_received", 0)
                },
                "commands": {
                    "total_commands_processed": info.get("total_commands_processed", 0),
                    "instantaneous_ops_per_sec": info.get("instantaneous_ops_per_sec", 0)
                }
            }
        else:
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "disabled",
                "message": "Redis caching is not enabled"
            }
            
    except Exception as e:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "error",
            "error": str(e)
        }

@router.get("/application")
async def get_application_metrics(db: AsyncSession = Depends(get_database)) -> Dict[str, Any]:
    """Get application-specific performance metrics."""
    
    try:
        # Classification performance metrics
        performance_query = text("""
            SELECT 
                AVG(processing_time) as avg_processing_time,
                MIN(processing_time) as min_processing_time,
                MAX(processing_time) as max_processing_time,
                COUNT(*) as total_classifications,
                AVG(confidence) as avg_confidence
            FROM classification_records 
            WHERE created_at > NOW() - INTERVAL '24 hours'
        """)
        
        # Model usage statistics
        model_usage_query = text("""
            SELECT 
                model_name,
                COUNT(*) as usage_count,
                AVG(processing_time) as avg_processing_time,
                AVG(confidence) as avg_confidence
            FROM classification_records 
            WHERE created_at > NOW() - INTERVAL '24 hours'
            GROUP BY model_name
            ORDER BY usage_count DESC
        """)
        
        # Error statistics
        error_query = text("""
            SELECT 
                COUNT(*) as total_errors
            FROM classification_records 
            WHERE created_at > NOW() - INTERVAL '24 hours' 
            AND error_message IS NOT NULL
        """)
        
        performance_result = await db.execute(performance_query)
        model_usage_result = await db.execute(model_usage_query)
        error_result = await db.execute(error_query)
        
        performance = performance_result.fetchone()
        model_usage = model_usage_result.fetchall()
        errors = error_result.fetchone()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "performance": {
                "avg_processing_time": float(performance.avg_processing_time or 0),
                "min_processing_time": float(performance.min_processing_time or 0),
                "max_processing_time": float(performance.max_processing_time or 0),
                "total_classifications": performance.total_classifications or 0,
                "avg_confidence": float(performance.avg_confidence or 0)
            },
            "model_usage": [
                {
                    "model_name": row.model_name,
                    "usage_count": row.usage_count,
                    "avg_processing_time": float(row.avg_processing_time),
                    "avg_confidence": float(row.avg_confidence)
                }
                for row in model_usage
            ],
            "errors": {
                "total_errors_24h": errors.total_errors or 0,
                "error_rate": (errors.total_errors or 0) / max(performance.total_classifications or 1, 1) * 100
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Application metrics collection failed: {str(e)}"
        )

@router.get("/health/detailed")
async def get_detailed_health_check(db: AsyncSession = Depends(get_database)) -> Dict[str, Any]:
    """Comprehensive health check with dependency validation."""
    
    health_status = {
        "timestamp": datetime.utcnow().isoformat(),
        "status": "healthy",
        "services": {},
        "performance": {},
        "summary": {}
    }
    
    # Database health
    try:
        db_start = time.time()
        await db.execute(text("SELECT 1"))
        db_time = time.time() - db_start
        
        health_status["services"]["database"] = {
            "status": "healthy",
            "response_time": db_time,
            "message": "Database connection successful"
        }
    except Exception as e:
        health_status["services"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Redis health
    cache_service = CacheService()
    try:
        if cache_service.redis_client:
            redis_start = time.time()
            await cache_service.redis_client.ping()
            redis_time = time.time() - redis_start
            
            health_status["services"]["redis"] = {
                "status": "healthy",
                "response_time": redis_time,
                "message": "Redis connection successful"
            }
        else:
            health_status["services"]["redis"] = {
                "status": "disabled",
                "message": "Redis caching is not configured"
            }
    except Exception as e:
        health_status["services"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # System performance check
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    health_status["performance"] = {
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_available_gb": round(memory.available / (1024**3), 2)
    }
    
    # Performance warnings
    if cpu_percent > 80:
        health_status["status"] = "degraded"
        health_status["warnings"] = health_status.get("warnings", [])
        health_status["warnings"].append("High CPU usage detected")
    
    if memory.percent > 85:
        health_status["status"] = "degraded"
        health_status["warnings"] = health_status.get("warnings", [])
        health_status["warnings"].append("High memory usage detected")
    
    # Summary
    healthy_services = sum(1 for service in health_status["services"].values() 
                          if service.get("status") == "healthy")
    total_services = len(health_status["services"])
    
    health_status["summary"] = {
        "overall_status": health_status["status"],
        "healthy_services": f"{healthy_services}/{total_services}",
        "uptime": "Available via process monitoring",
        "last_check": datetime.utcnow().isoformat()
    }
    
    return health_status

@router.get("/dashboard")
async def get_monitoring_dashboard(db: AsyncSession = Depends(get_database)) -> Dict[str, Any]:
    """Get comprehensive dashboard data for monitoring interface."""
    
    try:
        # Get metrics from all endpoints
        system_metrics = await get_system_metrics()
        db_metrics = await get_database_metrics(db)
        cache_metrics = await get_cache_metrics()
        app_metrics = await get_application_metrics(db)
        health_check = await get_detailed_health_check(db)
        
        # Aggregate into dashboard format
        dashboard = {
            "timestamp": datetime.utcnow().isoformat(),
            "overview": {
                "status": health_check["status"],
                "total_classifications": app_metrics["performance"]["total_classifications"],
                "avg_processing_time": app_metrics["performance"]["avg_processing_time"],
                "error_rate": app_metrics["errors"]["error_rate"],
                "uptime": "Available via process monitoring"
            },
            "system": system_metrics["system"],
            "database": db_metrics,
            "cache": cache_metrics,
            "application": app_metrics,
            "health": health_check
        }
        
        return dashboard
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Dashboard data collection failed: {str(e)}"
        )