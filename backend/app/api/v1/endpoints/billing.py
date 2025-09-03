"""
API monetization and billing endpoints.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status, Form, Query, Depends, Header
from pydantic import BaseModel, Field
from datetime import datetime

from app.services.monetization_service import monetization_service, SubscriptionTier
from app.utils.auth import get_api_key_info

router = APIRouter()

class CreateSubscriptionRequest(BaseModel):
    """Request model for creating subscription."""
    tier: SubscriptionTier = Field(..., description="Subscription tier")
    payment_method_id: Optional[str] = Field(None, description="Payment method identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tier": "professional",
                "payment_method_id": "pm_1234567890"
            }
        }

class APIKeyRequest(BaseModel):
    """Request model for API key generation."""
    name: str = Field(..., min_length=1, max_length=100, description="API key name")
    permissions: Optional[list] = Field(default=None, description="API key permissions")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Production API Key",
                "permissions": ["classification", "multimodal"]
            }
        }

@router.post("/subscription/create")
async def create_subscription(
    request: CreateSubscriptionRequest,
    user_id: str = Form(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Create a new subscription for user.
    
    Args:
        request: Subscription creation request
        user_id: User identifier
    
    Returns:
        Created subscription information
    """
    
    try:
        result = await monetization_service.create_subscription(
            user_id=user_id,
            tier=request.tier,
            payment_method_id=request.payment_method_id
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to create subscription")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create subscription: {str(e)}"
        )

@router.get("/subscription")
async def get_subscription_info(
    user_id: str = Query(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Get user's subscription information.
    
    Args:
        user_id: User identifier
    
    Returns:
        Subscription information
    """
    
    try:
        result = await monetization_service.get_subscription_info(user_id)
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get subscription info: {str(e)}"
        )

@router.get("/usage/analytics")
async def get_usage_analytics(
    user_id: str = Query(...),  # In production, this would come from authentication
    period: str = Query("current_month", pattern="^(current_month|last_month|last_7_days)$")
) -> Dict[str, Any]:
    """
    Get usage analytics for user.
    
    Args:
        user_id: User identifier
        period: Analytics period
    
    Returns:
        Usage analytics data
    """
    
    try:
        result = await monetization_service.get_usage_analytics(
            user_id=user_id,
            period=period
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get usage analytics: {str(e)}"
        )

@router.post("/api-key/generate")
async def generate_api_key(
    request: APIKeyRequest,
    user_id: str = Form(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Generate a new API key for user.
    
    Args:
        request: API key generation request
        user_id: User identifier
    
    Returns:
        Generated API key information
    """
    
    try:
        # Get user's subscription to generate key
        subscription_info = await monetization_service.get_subscription_info(user_id)
        
        if "error" in subscription_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valid subscription required to generate API key"
            )
        
        # Generate API key (this would typically be done through the subscription)
        result = await monetization_service._generate_api_key(
            user_id=user_id,
            subscription_id=subscription_info["subscription"]["subscription_id"],
            key_name=request.name
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to generate API key")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate API key: {str(e)}"
        )

@router.get("/pricing")
async def get_pricing_info() -> Dict[str, Any]:
    """
    Get pricing information for all subscription tiers.
    
    Returns:
        Pricing information
    """
    
    try:
        dashboard = await monetization_service.get_billing_dashboard()
        
        # Return public pricing info (remove admin statistics)
        return {
            "pricing_tiers": dashboard.get("pricing_tiers", {}),
            "service_pricing": dashboard.get("service_pricing", {}),
            "features_comparison": {
                "free": [
                    "1,000 requests/month included",
                    "Basic image classification",
                    "Standard models only",
                    "Community support",
                    "10 requests/minute limit"
                ],
                "basic": [
                    "10,000 requests/month included",
                    "All classification types",
                    "Custom model support",
                    "Email support",
                    "Usage analytics",
                    "60 requests/minute limit"
                ],
                "professional": [
                    "100,000 requests/month included",
                    "All features included",
                    "Priority support",
                    "Advanced analytics",
                    "Team collaboration",
                    "Custom integrations",
                    "300 requests/minute limit"
                ],
                "enterprise": [
                    "500,000 requests/month included",
                    "Unlimited features",
                    "24/7 dedicated support",
                    "Custom SLA",
                    "On-premise deployment",
                    "Dedicated account manager",
                    "1,000 requests/minute limit"
                ]
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get pricing info: {str(e)}"
        )

@router.get("/dashboard/admin")
async def get_billing_dashboard(
    admin_user_id: str = Query(...)  # In production, validate admin privileges
) -> Dict[str, Any]:
    """
    Get comprehensive billing dashboard (admin only).
    
    Args:
        admin_user_id: Administrator user ID
    
    Returns:
        Billing dashboard data
    """
    
    # In production, validate admin privileges
    try:
        result = await monetization_service.get_billing_dashboard()
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get billing dashboard: {str(e)}"
        )

@router.post("/usage/log")
async def log_api_usage(
    service_type: str = Form(...),
    endpoint: str = Form(...),
    request_size: int = Form(...),
    processing_time: float = Form(...),
    success: bool = Form(...),
    api_key: str = Header(..., alias="X-API-Key")
) -> Dict[str, Any]:
    """
    Log API usage for billing (internal endpoint).
    
    Args:
        service_type: Type of service used
        endpoint: API endpoint called
        request_size: Size of request
        processing_time: Processing time
        success: Whether request succeeded
        api_key: API key from header
    
    Returns:
        Usage logging confirmation
    """
    
    try:
        result = await monetization_service.log_api_usage(
            api_key=api_key,
            service_type=service_type,
            endpoint=endpoint,
            request_size=request_size,
            processing_time=processing_time,
            success=success
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to log usage")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log usage: {str(e)}"
        )

@router.get("/rate-limits/check")
async def check_rate_limits(
    api_key: str = Header(..., alias="X-API-Key")
) -> Dict[str, Any]:
    """
    Check current rate limit status for API key.
    
    Args:
        api_key: API key to check
    
    Returns:
        Rate limit status
    """
    
    try:
        result = await monetization_service.check_rate_limits(api_key)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check rate limits: {str(e)}"
        )

@router.get("/tiers")
async def get_subscription_tiers() -> Dict[str, Any]:
    """
    Get available subscription tiers with detailed information.
    
    Returns:
        Subscription tiers information
    """
    
    try:
        dashboard = await monetization_service.get_billing_dashboard()
        pricing_tiers = dashboard.get("pricing_tiers", {})
        
        # Format for public consumption
        formatted_tiers = []
        for tier_id, tier_info in pricing_tiers.items():
            formatted_tier = {
                "tier_id": tier_id,
                "name": tier_info["name"],
                "monthly_cost": tier_info["monthly_cost"],
                "included_requests": tier_info["included_requests"],
                "rate_limits": {
                    "per_minute": tier_info["rate_limit_per_minute"],
                    "per_hour": tier_info["rate_limit_per_hour"]
                },
                "features": tier_info["features"],
                "overage_cost": tier_info["overage_cost_per_request"],
                "recommended_for": {
                    "free": "Personal projects and experimentation",
                    "basic": "Small businesses and startups",
                    "professional": "Growing businesses and development teams", 
                    "enterprise": "Large organizations and high-volume applications"
                }.get(tier_id, "General use")
            }
            formatted_tiers.append(formatted_tier)
        
        return {
            "tiers": formatted_tiers,
            "currency": "USD",
            "billing_cycle": "monthly",
            "payment_methods": ["credit_card", "paypal", "bank_transfer"],
            "support_levels": {
                "free": "Community forums",
                "basic": "Email support (48h response)",
                "professional": "Priority email support (24h response)",
                "enterprise": "24/7 phone and email support (4h response)"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get subscription tiers: {str(e)}"
        )