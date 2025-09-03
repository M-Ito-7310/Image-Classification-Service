"""
API monetization service with usage-based billing and subscription management.
Enables monetization of AI classification services through API usage tracking.
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import hashlib
import secrets

from app.services.cache_service import CacheService
from app.core.config import settings


class SubscriptionTier(str, Enum):
    """Subscription tier levels."""
    FREE = "free"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class BillingStatus(str, Enum):
    """Billing status."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"
    PAST_DUE = "past_due"


class APIKeyStatus(str, Enum):
    """API key status."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"


class MonetizationService:
    """Service for API monetization and usage-based billing."""
    
    def __init__(self):
        self.cache_service = CacheService()
        self.storage_path = Path(settings.MODEL_STORAGE_PATH) / "monetization"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Data files
        self.subscriptions_file = self.storage_path / "subscriptions.json"
        self.api_keys_file = self.storage_path / "api_keys.json"
        self.usage_logs_file = self.storage_path / "usage_logs.json"
        self.billing_file = self.storage_path / "billing.json"
        
        # Load data
        self.subscriptions = self._load_json_file(self.subscriptions_file, {})
        self.api_keys = self._load_json_file(self.api_keys_file, {})
        self.usage_logs = self._load_json_file(self.usage_logs_file, [])
        self.billing_records = self._load_json_file(self.billing_file, {})
        
        # Pricing configuration
        self.pricing_config = self._get_pricing_config()
    
    def _load_json_file(self, file_path: Path, default_value: Any) -> Any:
        """Load JSON file or return default value."""
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
        return default_value
    
    def _save_json_file(self, file_path: Path, data: Any):
        """Save data to JSON file."""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving {file_path}: {e}")
    
    def _get_pricing_config(self) -> Dict[str, Any]:
        """Get pricing configuration for different tiers and services."""
        return {
            "tiers": {
                SubscriptionTier.FREE: {
                    "name": "Free Tier",
                    "monthly_cost": 0.00,
                    "included_requests": 1000,
                    "rate_limit_per_minute": 10,
                    "rate_limit_per_hour": 100,
                    "features": ["Basic classification", "Standard models", "Community support"],
                    "overage_cost_per_request": 0.01
                },
                SubscriptionTier.BASIC: {
                    "name": "Basic Plan",
                    "monthly_cost": 29.99,
                    "included_requests": 10000,
                    "rate_limit_per_minute": 60,
                    "rate_limit_per_hour": 1000,
                    "features": ["All classification types", "Custom models", "Email support", "Usage analytics"],
                    "overage_cost_per_request": 0.005
                },
                SubscriptionTier.PROFESSIONAL: {
                    "name": "Professional Plan",
                    "monthly_cost": 99.99,
                    "included_requests": 100000,
                    "rate_limit_per_minute": 300,
                    "rate_limit_per_hour": 5000,
                    "features": ["All features", "Priority support", "Advanced analytics", "Custom integrations", "Team collaboration"],
                    "overage_cost_per_request": 0.002
                },
                SubscriptionTier.ENTERPRISE: {
                    "name": "Enterprise Plan",
                    "monthly_cost": 299.99,
                    "included_requests": 500000,
                    "rate_limit_per_minute": 1000,
                    "rate_limit_per_hour": 20000,
                    "features": ["Unlimited features", "24/7 support", "Custom SLA", "On-premise deployment", "Dedicated account manager"],
                    "overage_cost_per_request": 0.001
                }
            },
            "services": {
                "image_classification": {"base_cost": 1, "complexity_multiplier": 1.0},
                "video_classification": {"base_cost": 3, "complexity_multiplier": 1.5},
                "audio_classification": {"base_cost": 2, "complexity_multiplier": 1.2},
                "batch_processing": {"base_cost": 1, "complexity_multiplier": 0.8},
                "real_time_streaming": {"base_cost": 5, "complexity_multiplier": 2.0},
                "custom_model_inference": {"base_cost": 2, "complexity_multiplier": 1.3}
            }
        }
    
    async def create_subscription(
        self,
        user_id: str,
        tier: SubscriptionTier,
        payment_method_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new subscription for user.
        
        Args:
            user_id: User identifier
            tier: Subscription tier
            payment_method_id: Payment method identifier
        
        Returns:
            Created subscription information
        """
        
        try:
            subscription_id = str(uuid.uuid4())
            
            tier_config = self.pricing_config["tiers"][tier]
            
            subscription = {
                "subscription_id": subscription_id,
                "user_id": user_id,
                "tier": tier,
                "status": BillingStatus.ACTIVE,
                "created_at": datetime.utcnow().isoformat(),
                "billing_cycle_start": datetime.utcnow().isoformat(),
                "billing_cycle_end": (datetime.utcnow() + timedelta(days=30)).isoformat(),
                "monthly_cost": tier_config["monthly_cost"],
                "included_requests": tier_config["included_requests"],
                "used_requests": 0,
                "overage_requests": 0,
                "payment_method_id": payment_method_id,
                "auto_renew": True,
                "features": tier_config["features"],
                "rate_limits": {
                    "per_minute": tier_config["rate_limit_per_minute"],
                    "per_hour": tier_config["rate_limit_per_hour"]
                }
            }
            
            # Save subscription
            self.subscriptions[subscription_id] = subscription
            self._save_json_file(self.subscriptions_file, self.subscriptions)
            
            # Generate initial API key
            api_key_result = await self._generate_api_key(user_id, subscription_id)
            
            # Cache subscription info
            await self.cache_service.set(
                f"subscription:{subscription_id}",
                json.dumps(subscription),
                ttl=3600
            )
            
            return {
                "success": True,
                "subscription": {
                    "subscription_id": subscription_id,
                    "tier": tier,
                    "status": subscription["status"],
                    "monthly_cost": subscription["monthly_cost"],
                    "included_requests": subscription["included_requests"],
                    "billing_cycle_end": subscription["billing_cycle_end"],
                    "features": subscription["features"]
                },
                "api_key": api_key_result.get("api_key") if api_key_result.get("success") else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create subscription: {str(e)}"
            }
    
    async def _generate_api_key(
        self,
        user_id: str,
        subscription_id: str,
        key_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate API key for user subscription.
        
        Args:
            user_id: User identifier
            subscription_id: Subscription identifier
            key_name: Optional key name
        
        Returns:
            Generated API key information
        """
        
        try:
            # Generate secure API key
            api_key = f"ak_{secrets.token_urlsafe(32)}"
            api_key_id = str(uuid.uuid4())
            
            key_record = {
                "api_key_id": api_key_id,
                "api_key": api_key,
                "user_id": user_id,
                "subscription_id": subscription_id,
                "name": key_name or f"API Key {datetime.utcnow().strftime('%Y-%m-%d')}",
                "status": APIKeyStatus.ACTIVE,
                "created_at": datetime.utcnow().isoformat(),
                "last_used": None,
                "total_requests": 0,
                "permissions": ["classification", "multimodal", "realtime"]
            }
            
            # Save API key
            self.api_keys[api_key] = key_record
            self._save_json_file(self.api_keys_file, self.api_keys)
            
            # Cache API key info
            await self.cache_service.set(
                f"api_key:{api_key}",
                json.dumps(key_record),
                ttl=7200  # 2 hours
            )
            
            return {
                "success": True,
                "api_key": api_key,
                "api_key_id": api_key_id,
                "permissions": key_record["permissions"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate API key: {str(e)}"
            }
    
    async def validate_api_key(self, api_key: str) -> Dict[str, Any]:
        """
        Validate API key and return associated information.
        
        Args:
            api_key: API key to validate
        
        Returns:
            Validation result with key information
        """
        
        try:
            # Check cache first
            cached_key = await self.cache_service.get(f"api_key:{api_key}")
            if cached_key:
                key_record = json.loads(cached_key)
            else:
                # Get from storage
                key_record = self.api_keys.get(api_key)
                if not key_record:
                    return {"valid": False, "error": "Invalid API key"}
                
                # Cache for future requests
                await self.cache_service.set(
                    f"api_key:{api_key}",
                    json.dumps(key_record),
                    ttl=7200
                )
            
            # Check key status
            if key_record["status"] != APIKeyStatus.ACTIVE:
                return {"valid": False, "error": f"API key is {key_record['status']}"}
            
            # Get subscription info
            subscription_id = key_record["subscription_id"]
            subscription = self.subscriptions.get(subscription_id)
            
            if not subscription:
                return {"valid": False, "error": "Associated subscription not found"}
            
            if subscription["status"] != BillingStatus.ACTIVE:
                return {"valid": False, "error": f"Subscription is {subscription['status']}"}
            
            return {
                "valid": True,
                "key_record": key_record,
                "subscription": subscription,
                "user_id": key_record["user_id"],
                "tier": subscription["tier"],
                "permissions": key_record["permissions"],
                "rate_limits": subscription["rate_limits"]
            }
            
        except Exception as e:
            return {"valid": False, "error": f"API key validation failed: {str(e)}"}
    
    async def log_api_usage(
        self,
        api_key: str,
        service_type: str,
        endpoint: str,
        request_size: int,
        processing_time: float,
        success: bool,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Log API usage for billing and analytics.
        
        Args:
            api_key: API key used
            service_type: Type of service (image_classification, etc.)
            endpoint: API endpoint called
            request_size: Size of request in bytes
            processing_time: Processing time in seconds
            success: Whether request was successful
            metadata: Additional metadata
        
        Returns:
            Usage logging result
        """
        
        try:
            # Validate API key
            key_validation = await self.validate_api_key(api_key)
            if not key_validation["valid"]:
                return {"success": False, "error": key_validation["error"]}
            
            key_record = key_validation["key_record"]
            subscription = key_validation["subscription"]
            
            # Calculate cost
            service_config = self.pricing_config["services"].get(service_type, {
                "base_cost": 1,
                "complexity_multiplier": 1.0
            })
            
            # Cost calculation based on request complexity
            base_cost = service_config["base_cost"]
            complexity_multiplier = service_config["complexity_multiplier"]
            
            # Factor in processing time and request size
            cost_multiplier = 1.0
            if processing_time > 5.0:  # Long processing
                cost_multiplier *= 1.5
            if request_size > 1024 * 1024:  # Large request (>1MB)
                cost_multiplier *= 1.2
            
            calculated_cost = base_cost * complexity_multiplier * cost_multiplier
            
            # Create usage log entry
            usage_entry = {
                "usage_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "api_key": api_key[:10] + "...",  # Masked for security
                "user_id": key_record["user_id"],
                "subscription_id": subscription["subscription_id"],
                "service_type": service_type,
                "endpoint": endpoint,
                "request_size": request_size,
                "processing_time": processing_time,
                "success": success,
                "cost": calculated_cost,
                "tier": subscription["tier"],
                "metadata": metadata or {}
            }
            
            # Add to usage logs
            self.usage_logs.append(usage_entry)
            
            # Keep only last 10000 entries to prevent excessive storage
            if len(self.usage_logs) > 10000:
                self.usage_logs = self.usage_logs[-10000:]
            
            self._save_json_file(self.usage_logs_file, self.usage_logs)
            
            # Update subscription usage
            subscription["used_requests"] += 1
            if subscription["used_requests"] > subscription["included_requests"]:
                subscription["overage_requests"] = (
                    subscription["used_requests"] - subscription["included_requests"]
                )
            
            self._save_json_file(self.subscriptions_file, self.subscriptions)
            
            # Update API key last used
            self.api_keys[api_key]["last_used"] = datetime.utcnow().isoformat()
            self.api_keys[api_key]["total_requests"] += 1
            self._save_json_file(self.api_keys_file, self.api_keys)
            
            # Update caches
            await self.cache_service.set(
                f"subscription:{subscription['subscription_id']}",
                json.dumps(subscription),
                ttl=3600
            )
            
            await self.cache_service.set(
                f"api_key:{api_key}",
                json.dumps(self.api_keys[api_key]),
                ttl=7200
            )
            
            return {
                "success": True,
                "usage_logged": True,
                "cost": calculated_cost,
                "remaining_requests": max(0, subscription["included_requests"] - subscription["used_requests"]),
                "overage_requests": subscription.get("overage_requests", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to log API usage: {str(e)}"
            }
    
    async def get_usage_analytics(
        self,
        user_id: str,
        period: str = "current_month"
    ) -> Dict[str, Any]:
        """
        Get usage analytics for user.
        
        Args:
            user_id: User identifier
            period: Analytics period (current_month, last_month, last_7_days)
        
        Returns:
            Usage analytics data
        """
        
        try:
            # Get user's subscription
            user_subscription = None
            for sub in self.subscriptions.values():
                if sub["user_id"] == user_id:
                    user_subscription = sub
                    break
            
            if not user_subscription:
                return {"error": "No active subscription found"}
            
            # Filter usage logs by period
            now = datetime.utcnow()
            if period == "current_month":
                start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            elif period == "last_month":
                last_month = now.replace(day=1) - timedelta(days=1)
                start_date = last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                end_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            elif period == "last_7_days":
                start_date = now - timedelta(days=7)
            else:
                start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Filter usage logs
            filtered_logs = []
            for log in self.usage_logs:
                if log["user_id"] != user_id:
                    continue
                
                log_time = datetime.fromisoformat(log["timestamp"])
                if period == "last_month":
                    if start_date <= log_time < end_date:
                        filtered_logs.append(log)
                else:
                    if log_time >= start_date:
                        filtered_logs.append(log)
            
            # Calculate analytics
            total_requests = len(filtered_logs)
            successful_requests = sum(1 for log in filtered_logs if log["success"])
            total_cost = sum(log["cost"] for log in filtered_logs)
            avg_processing_time = (
                sum(log["processing_time"] for log in filtered_logs) / max(total_requests, 1)
            )
            
            # Service type breakdown
            service_breakdown = {}
            for log in filtered_logs:
                service = log["service_type"]
                if service not in service_breakdown:
                    service_breakdown[service] = {"count": 0, "cost": 0}
                service_breakdown[service]["count"] += 1
                service_breakdown[service]["cost"] += log["cost"]
            
            # Daily usage breakdown
            daily_usage = {}
            for log in filtered_logs:
                date = log["timestamp"][:10]  # Extract date part
                if date not in daily_usage:
                    daily_usage[date] = {"requests": 0, "cost": 0}
                daily_usage[date]["requests"] += 1
                daily_usage[date]["cost"] += log["cost"]
            
            return {
                "period": period,
                "subscription_info": {
                    "tier": user_subscription["tier"],
                    "included_requests": user_subscription["included_requests"],
                    "used_requests": user_subscription["used_requests"],
                    "remaining_requests": max(0, user_subscription["included_requests"] - user_subscription["used_requests"]),
                    "overage_requests": user_subscription.get("overage_requests", 0)
                },
                "analytics": {
                    "total_requests": total_requests,
                    "successful_requests": successful_requests,
                    "success_rate": (successful_requests / max(total_requests, 1)) * 100,
                    "total_cost": round(total_cost, 4),
                    "average_processing_time": round(avg_processing_time, 3),
                    "service_breakdown": service_breakdown,
                    "daily_usage": daily_usage
                },
                "billing_estimate": {
                    "current_cycle_cost": user_subscription["monthly_cost"],
                    "overage_cost": user_subscription.get("overage_requests", 0) * self.pricing_config["tiers"][user_subscription["tier"]]["overage_cost_per_request"],
                    "total_estimated": user_subscription["monthly_cost"] + (user_subscription.get("overage_requests", 0) * self.pricing_config["tiers"][user_subscription["tier"]]["overage_cost_per_request"])
                }
            }
            
        except Exception as e:
            return {"error": f"Failed to get usage analytics: {str(e)}"}
    
    async def check_rate_limits(
        self,
        api_key: str,
        current_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Check if API key has exceeded rate limits.
        
        Args:
            api_key: API key to check
            current_time: Current time (defaults to now)
        
        Returns:
            Rate limit check result
        """
        
        if not current_time:
            current_time = datetime.utcnow()
        
        try:
            # Validate API key
            key_validation = await self.validate_api_key(api_key)
            if not key_validation["valid"]:
                return {"allowed": False, "error": key_validation["error"]}
            
            subscription = key_validation["subscription"]
            rate_limits = subscription["rate_limits"]
            
            # Check minute rate limit
            minute_key = f"rate_limit:{api_key}:minute:{current_time.strftime('%Y%m%d%H%M')}"
            minute_count = await self.cache_service.get(minute_key)
            minute_count = int(minute_count) if minute_count else 0
            
            if minute_count >= rate_limits["per_minute"]:
                return {
                    "allowed": False,
                    "error": "Per-minute rate limit exceeded",
                    "limit": rate_limits["per_minute"],
                    "current": minute_count,
                    "reset_time": (current_time + timedelta(minutes=1)).isoformat()
                }
            
            # Check hour rate limit
            hour_key = f"rate_limit:{api_key}:hour:{current_time.strftime('%Y%m%d%H')}"
            hour_count = await self.cache_service.get(hour_key)
            hour_count = int(hour_count) if hour_count else 0
            
            if hour_count >= rate_limits["per_hour"]:
                return {
                    "allowed": False,
                    "error": "Per-hour rate limit exceeded",
                    "limit": rate_limits["per_hour"],
                    "current": hour_count,
                    "reset_time": (current_time + timedelta(hours=1)).isoformat()
                }
            
            # Increment counters
            await self.cache_service.set(minute_key, str(minute_count + 1), ttl=60)
            await self.cache_service.set(hour_key, str(hour_count + 1), ttl=3600)
            
            return {
                "allowed": True,
                "rate_limits": {
                    "per_minute": {
                        "limit": rate_limits["per_minute"],
                        "remaining": rate_limits["per_minute"] - minute_count - 1
                    },
                    "per_hour": {
                        "limit": rate_limits["per_hour"],
                        "remaining": rate_limits["per_hour"] - hour_count - 1
                    }
                }
            }
            
        except Exception as e:
            return {"allowed": False, "error": f"Rate limit check failed: {str(e)}"}
    
    async def get_subscription_info(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's subscription information.
        
        Args:
            user_id: User identifier
        
        Returns:
            Subscription information
        """
        
        try:
            # Find user's subscription
            user_subscription = None
            for sub in self.subscriptions.values():
                if sub["user_id"] == user_id:
                    user_subscription = sub
                    break
            
            if not user_subscription:
                return {"error": "No subscription found"}
            
            # Get user's API keys
            user_api_keys = []
            for api_key, key_record in self.api_keys.items():
                if key_record["user_id"] == user_id:
                    user_api_keys.append({
                        "api_key_id": key_record["api_key_id"],
                        "name": key_record["name"],
                        "status": key_record["status"],
                        "created_at": key_record["created_at"],
                        "last_used": key_record["last_used"],
                        "total_requests": key_record["total_requests"],
                        "masked_key": api_key[:10] + "..." + api_key[-4:]
                    })
            
            return {
                "subscription": {
                    "subscription_id": user_subscription["subscription_id"],
                    "tier": user_subscription["tier"],
                    "status": user_subscription["status"],
                    "monthly_cost": user_subscription["monthly_cost"],
                    "included_requests": user_subscription["included_requests"],
                    "used_requests": user_subscription["used_requests"],
                    "overage_requests": user_subscription.get("overage_requests", 0),
                    "billing_cycle_start": user_subscription["billing_cycle_start"],
                    "billing_cycle_end": user_subscription["billing_cycle_end"],
                    "features": user_subscription["features"],
                    "rate_limits": user_subscription["rate_limits"]
                },
                "api_keys": user_api_keys,
                "pricing": self.pricing_config["tiers"][user_subscription["tier"]]
            }
            
        except Exception as e:
            return {"error": f"Failed to get subscription info: {str(e)}"}
    
    async def get_billing_dashboard(self) -> Dict[str, Any]:
        """
        Get billing dashboard with overall statistics.
        
        Returns:
            Billing dashboard data
        """
        
        try:
            # Calculate statistics
            total_subscriptions = len(self.subscriptions)
            active_subscriptions = sum(
                1 for sub in self.subscriptions.values() 
                if sub["status"] == BillingStatus.ACTIVE
            )
            
            # Tier breakdown
            tier_breakdown = {}
            total_monthly_revenue = 0
            
            for sub in self.subscriptions.values():
                if sub["status"] == BillingStatus.ACTIVE:
                    tier = sub["tier"]
                    if tier not in tier_breakdown:
                        tier_breakdown[tier] = {"count": 0, "revenue": 0}
                    tier_breakdown[tier]["count"] += 1
                    tier_breakdown[tier]["revenue"] += sub["monthly_cost"]
                    total_monthly_revenue += sub["monthly_cost"]
            
            # Usage statistics
            current_month = datetime.utcnow().strftime("%Y-%m")
            monthly_requests = 0
            monthly_overage = 0
            
            for log in self.usage_logs:
                if log["timestamp"].startswith(current_month):
                    monthly_requests += 1
            
            for sub in self.subscriptions.values():
                if sub["status"] == BillingStatus.ACTIVE:
                    monthly_overage += sub.get("overage_requests", 0)
            
            return {
                "overview": {
                    "total_subscriptions": total_subscriptions,
                    "active_subscriptions": active_subscriptions,
                    "total_monthly_revenue": round(total_monthly_revenue, 2),
                    "total_api_keys": len(self.api_keys),
                    "monthly_requests": monthly_requests,
                    "monthly_overage_requests": monthly_overage
                },
                "tier_breakdown": tier_breakdown,
                "pricing_tiers": self.pricing_config["tiers"],
                "service_pricing": self.pricing_config["services"]
            }
            
        except Exception as e:
            return {"error": f"Failed to get billing dashboard: {str(e)}"}


# Global instance
monetization_service = MonetizationService()