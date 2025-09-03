"""
API monetization middleware for usage tracking and rate limiting.
"""

import json
import time
from typing import Optional
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.services.monetization_service import monetization_service


class MonetizationMiddleware(BaseHTTPMiddleware):
    """Middleware to handle API key validation, usage tracking, and rate limiting."""
    
    def __init__(self, app, exempt_paths: list = None):
        super().__init__(app)
        self.exempt_paths = exempt_paths or [
            "/docs",
            "/redoc", 
            "/openapi.json",
            "/api/v1/health",
            "/api/v1/billing/pricing",
            "/api/v1/billing/tiers"
        ]
    
    async def dispatch(self, request: Request, call_next):
        # Skip middleware for exempt paths
        if any(request.url.path.startswith(path) for path in self.exempt_paths):
            return await call_next(request)
        
        # Skip for non-API endpoints
        if not request.url.path.startswith("/api/v1/"):
            return await call_next(request)
        
        # Skip for billing endpoints (they handle their own auth)
        if request.url.path.startswith("/api/v1/billing/"):
            return await call_next(request)
        
        # Extract API key from header
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "API key required. Include X-API-Key header.",
                    "error_code": "API_KEY_MISSING"
                }
            )
        
        try:
            # Validate API key
            key_info = await monetization_service.validate_api_key(api_key)
            
            if not key_info.get("valid"):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "detail": key_info.get("error", "Invalid API key"),
                        "error_code": "API_KEY_INVALID"
                    }
                )
            
            # Check rate limits
            rate_limit_status = await monetization_service.check_rate_limits(api_key)
            
            if rate_limit_status.get("rate_limited"):
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": f"Rate limit exceeded. Limit: {rate_limit_status.get('limit')}/minute",
                        "error_code": "RATE_LIMIT_EXCEEDED",
                        "retry_after": rate_limit_status.get("retry_after", 60)
                    }
                )
            
            # Add API key info to request state for downstream handlers
            request.state.api_key_info = key_info
            request.state.rate_limit_info = rate_limit_status
            
            # Process request
            start_time = time.time()
            response = await call_next(request)
            processing_time = time.time() - start_time
            
            # Log usage after successful response
            if response.status_code < 500:  # Don't log server errors as usage
                await self._log_usage(
                    request=request,
                    api_key=api_key,
                    processing_time=processing_time,
                    success=response.status_code < 400
                )
            
            # Add rate limit headers to response
            response.headers["X-RateLimit-Limit"] = str(rate_limit_status.get("limit", 0))
            response.headers["X-RateLimit-Remaining"] = str(rate_limit_status.get("remaining", 0))
            response.headers["X-RateLimit-Reset"] = str(rate_limit_status.get("reset_time", 0))
            
            return response
            
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": f"Monetization middleware error: {str(e)}",
                    "error_code": "MIDDLEWARE_ERROR"
                }
            )
    
    async def _log_usage(
        self,
        request: Request,
        api_key: str,
        processing_time: float,
        success: bool
    ):
        """Log API usage for billing purposes."""
        try:
            # Determine service type based on endpoint
            service_type = self._get_service_type(request.url.path)
            
            # Get request size (approximate)
            request_size = len(str(request.url)) + sum(
                len(key) + len(value) for key, value in request.headers.items()
            )
            
            # Add body size if available
            if hasattr(request, 'body'):
                try:
                    body = await request.body()
                    request_size += len(body)
                except:
                    pass  # Body already consumed
            
            await monetization_service.log_api_usage(
                api_key=api_key,
                service_type=service_type,
                endpoint=request.url.path,
                request_size=request_size,
                processing_time=processing_time,
                success=success
            )
            
        except Exception as e:
            # Don't fail the request if usage logging fails
            print(f"Usage logging error: {e}")
    
    def _get_service_type(self, path: str) -> str:
        """Determine service type from API endpoint path."""
        if "/classification" in path:
            return "classification"
        elif "/multimodal" in path:
            return "multimodal"
        elif "/realtime" in path:
            return "realtime"
        elif "/models" in path:
            return "models"
        elif "/collaboration" in path:
            return "collaboration"
        elif "/marketplace" in path:
            return "marketplace"
        else:
            return "general"


class APIKeyDependency:
    """Dependency to extract validated API key info from request state."""
    
    def __call__(self, request: Request) -> dict:
        if not hasattr(request.state, 'api_key_info'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key validation required"
            )
        
        return request.state.api_key_info


# Create dependency instance
get_api_key_info = APIKeyDependency()