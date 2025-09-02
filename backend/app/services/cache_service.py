"""Redis caching service for performance optimization."""

import json
import hashlib
import logging
from typing import Any, Optional, Union, Dict, List
from datetime import datetime, timedelta
import redis.asyncio as redis
from redis.asyncio import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)

class CacheService:
    """Redis-based caching service for application performance optimization."""
    
    def __init__(self):
        self.redis_client: Optional[Redis] = None
        self.enabled = settings.CACHE_ENABLED
        
    async def connect(self) -> bool:
        """Connect to Redis server."""
        if not self.enabled:
            logger.info("Cache is disabled")
            return False
            
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                decode_responses=True,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            await self.redis_client.ping()
            logger.info("Connected to Redis cache successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.enabled = False
            return False
    
    async def disconnect(self):
        """Disconnect from Redis server."""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Disconnected from Redis cache")
    
    def _generate_key(self, prefix: str, identifier: Union[str, Dict, List]) -> str:
        """Generate cache key with consistent hashing."""
        if isinstance(identifier, (dict, list)):
            identifier = json.dumps(identifier, sort_keys=True)
        
        key_data = f"{prefix}:{identifier}"
        return f"ai_service:{hashlib.md5(key_data.encode()).hexdigest()}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.enabled or not self.redis_client:
            return None
            
        try:
            value = await self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
            
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL."""
        if not self.enabled or not self.redis_client:
            return False
            
        try:
            ttl = ttl or settings.CACHE_TTL
            await self.redis_client.setex(
                key, 
                ttl, 
                json.dumps(value, default=str)
            )
            return True
            
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.enabled or not self.redis_client:
            return False
            
        try:
            await self.redis_client.delete(key)
            return True
            
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.enabled or not self.redis_client:
            return False
            
        try:
            return bool(await self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Cache exists check error for key {key}: {e}")
            return False
    
    # Specialized caching methods for AI service
    
    async def cache_classification_result(
        self, 
        image_hash: str, 
        model_name: str, 
        result: Dict[str, Any],
        ttl: int = 3600  # 1 hour default
    ) -> bool:
        """Cache classification result."""
        key = self._generate_key("classification", f"{image_hash}:{model_name}")
        
        cache_data = {
            "result": result,
            "cached_at": datetime.utcnow().isoformat(),
            "model": model_name
        }
        
        return await self.set(key, cache_data, ttl)
    
    async def get_cached_classification(
        self, 
        image_hash: str, 
        model_name: str
    ) -> Optional[Dict[str, Any]]:
        """Get cached classification result."""
        key = self._generate_key("classification", f"{image_hash}:{model_name}")
        
        cached_data = await self.get(key)
        if cached_data:
            return cached_data.get("result")
        return None
    
    async def cache_model_metadata(
        self, 
        model_name: str, 
        metadata: Dict[str, Any],
        ttl: int = 1800  # 30 minutes default
    ) -> bool:
        """Cache model metadata."""
        key = self._generate_key("model_metadata", model_name)
        return await self.set(key, metadata, ttl)
    
    async def get_cached_model_metadata(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get cached model metadata."""
        key = self._generate_key("model_metadata", model_name)
        return await self.get(key)
    
    async def cache_user_stats(
        self, 
        user_id: int, 
        stats: Dict[str, Any],
        ttl: int = 600  # 10 minutes default
    ) -> bool:
        """Cache user statistics."""
        key = self._generate_key("user_stats", str(user_id))
        return await self.set(key, stats, ttl)
    
    async def get_cached_user_stats(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get cached user statistics."""
        key = self._generate_key("user_stats", str(user_id))
        return await self.get(key)
    
    async def invalidate_user_cache(self, user_id: int) -> bool:
        """Invalidate all cache entries for a user."""
        if not self.enabled or not self.redis_client:
            return False
            
        try:
            # Pattern matching for user-related keys
            pattern = f"ai_service:*user_stats*{user_id}*"
            keys = await self.redis_client.keys(pattern)
            
            if keys:
                await self.redis_client.delete(*keys)
                logger.info(f"Invalidated {len(keys)} cache entries for user {user_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Cache invalidation error for user {user_id}: {e}")
            return False
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        if not self.enabled or not self.redis_client:
            return {"enabled": False}
            
        try:
            info = await self.redis_client.info()
            
            return {
                "enabled": True,
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0)
                )
            }
            
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"enabled": True, "error": str(e)}
    
    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate percentage."""
        total = hits + misses
        if total == 0:
            return 0.0
        return round((hits / total) * 100, 2)

# Global cache service instance
cache_service = CacheService()

async def get_cache_service() -> CacheService:
    """Dependency to get cache service instance."""
    return cache_service

def cache_key_for_image(image_data: bytes, model_name: str) -> str:
    """Generate consistent cache key for image classification."""
    image_hash = hashlib.md5(image_data).hexdigest()
    return f"classification:{image_hash}:{model_name}"

def cache_key_for_user_history(user_id: int, page: int = 1, limit: int = 10) -> str:
    """Generate cache key for user classification history."""
    return f"user_history:{user_id}:page_{page}_limit_{limit}"