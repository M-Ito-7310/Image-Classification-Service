"""Security middleware for API protection and rate limiting."""

import time
import hashlib
from typing import Dict, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from collections import defaultdict, deque
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware to prevent API abuse."""
    
    def __init__(self, app, calls_per_minute: int = 60, calls_per_hour: int = 1000):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.calls_per_hour = calls_per_hour
        
        # Storage for rate limiting (in production, use Redis)
        self.minute_calls: Dict[str, deque] = defaultdict(deque)
        self.hour_calls: Dict[str, deque] = defaultdict(deque)
        
        # Cleanup old entries periodically
        self.last_cleanup = time.time()
        self.cleanup_interval = 300  # 5 minutes
    
    def _get_client_id(self, request: Request) -> str:
        """Generate client identifier for rate limiting."""
        # Try to get user ID from authentication
        user_id = getattr(request.state, 'user_id', None)
        if user_id:
            return f"user_{user_id}"
        
        # Fall back to IP address
        client_ip = request.client.host if request.client else "unknown"
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        return f"ip_{client_ip}"
    
    def _cleanup_old_entries(self):
        """Clean up old rate limit entries."""
        current_time = time.time()
        
        # Only cleanup every 5 minutes
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
        
        minute_cutoff = current_time - 60
        hour_cutoff = current_time - 3600
        
        # Clean minute calls
        for client_id in list(self.minute_calls.keys()):
            calls = self.minute_calls[client_id]
            while calls and calls[0] < minute_cutoff:
                calls.popleft()
            if not calls:
                del self.minute_calls[client_id]
        
        # Clean hour calls
        for client_id in list(self.hour_calls.keys()):
            calls = self.hour_calls[client_id]
            while calls and calls[0] < hour_cutoff:
                calls.popleft()
            if not calls:
                del self.hour_calls[client_id]
        
        self.last_cleanup = current_time
    
    def _is_rate_limited(self, client_id: str) -> Optional[Dict[str, any]]:
        """Check if client is rate limited."""
        current_time = time.time()
        minute_cutoff = current_time - 60
        hour_cutoff = current_time - 3600
        
        # Get current calls for this client
        minute_calls = self.minute_calls[client_id]
        hour_calls = self.hour_calls[client_id]
        
        # Remove old calls
        while minute_calls and minute_calls[0] < minute_cutoff:
            minute_calls.popleft()
        while hour_calls and hour_calls[0] < hour_cutoff:
            hour_calls.popleft()
        
        # Check limits
        if len(minute_calls) >= self.calls_per_minute:
            return {
                "error": "Rate limit exceeded",
                "limit_type": "per_minute",
                "limit": self.calls_per_minute,
                "reset_time": int(minute_calls[0] + 60),
                "retry_after": int(minute_calls[0] + 60 - current_time)
            }
        
        if len(hour_calls) >= self.calls_per_hour:
            return {
                "error": "Rate limit exceeded", 
                "limit_type": "per_hour",
                "limit": self.calls_per_hour,
                "reset_time": int(hour_calls[0] + 3600),
                "retry_after": int(hour_calls[0] + 3600 - current_time)
            }
        
        return None
    
    def _record_call(self, client_id: str):
        """Record a new API call for rate limiting."""
        current_time = time.time()
        self.minute_calls[client_id].append(current_time)
        self.hour_calls[client_id].append(current_time)
    
    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        # Skip rate limiting for health checks and static files
        if request.url.path in ["/", "/health", "/api/v1/health"] or request.url.path.startswith("/uploads"):
            return await call_next(request)
        
        # Cleanup old entries periodically
        self._cleanup_old_entries()
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limits
        rate_limit_info = self._is_rate_limited(client_id)
        if rate_limit_info:
            logger.warning(f"Rate limit exceeded for client {client_id}: {rate_limit_info}")
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content=rate_limit_info,
                headers={
                    "Retry-After": str(rate_limit_info["retry_after"]),
                    "X-RateLimit-Limit": str(self.calls_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(rate_limit_info["reset_time"])
                }
            )
        
        # Record the call
        self._record_call(client_id)
        
        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add rate limit headers
        minute_calls = len(self.minute_calls[client_id])
        response.headers["X-RateLimit-Limit"] = str(self.calls_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, self.calls_per_minute - minute_calls))
        response.headers["X-Process-Time"] = str(round(process_time, 3))
        
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        # Content Security Policy
        if not request.url.path.startswith("/docs") and not request.url.path.startswith("/redoc"):
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: blob:; "
                "connect-src 'self' ws: wss:; "
                "font-src 'self'"
            )
        
        return response

class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Validate and sanitize incoming requests."""
    
    SUSPICIOUS_PATTERNS = [
        # SQL injection patterns
        r"('|(\\')|(;)|(\\)|(\-\-)|(\/\*))",
        # XSS patterns  
        r"(<script|javascript:|vbscript:|onload=|onerror=)",
        # Path traversal
        r"(\.\./|\.\.\\)",
        # Command injection
        r"(;|\||&|`|\$\()",
    ]
    
    MAX_REQUEST_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_HEADER_SIZE = 8192  # 8KB
    
    async def dispatch(self, request: Request, call_next):
        """Validate request before processing."""
        
        # Check request size
        if hasattr(request, 'headers'):
            content_length = request.headers.get('content-length')
            if content_length and int(content_length) > self.MAX_REQUEST_SIZE:
                return JSONResponse(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content={"detail": f"Request too large. Maximum size: {self.MAX_REQUEST_SIZE} bytes"}
                )
        
        # Check header sizes
        for name, value in request.headers.items():
            if len(f"{name}: {value}") > self.MAX_HEADER_SIZE:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Header too large"}
                )
        
        # Basic path validation
        if ".." in str(request.url.path) or "//" in str(request.url.path):
            logger.warning(f"Suspicious path detected: {request.url.path}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid request path"}
            )
        
        # Validate User-Agent (basic bot detection)
        user_agent = request.headers.get("user-agent", "").lower()
        if not user_agent or len(user_agent) < 10:
            logger.warning(f"Suspicious or missing User-Agent: {user_agent}")
            # Don't block but log for monitoring
        
        return await call_next(request)