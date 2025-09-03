"""
Team collaboration API endpoints for shared workspaces and projects.
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, status, Form, Query, Depends
from pydantic import BaseModel, Field

from app.services.collaboration_service import collaboration_service, UserRole, ProjectStatus
from app.services.security_service import FileSecurityService

router = APIRouter()

class CreateWorkspaceRequest(BaseModel):
    """Request model for creating workspace."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    settings: Optional[Dict[str, Any]] = Field(default=None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "AI Research Team",
                "description": "Collaborative workspace for AI research projects and image classification experiments",
                "settings": {
                    "allow_public_projects": False,
                    "require_approval_for_members": True,
                    "max_projects": 15,
                    "max_members": 25
                }
            }
        }

class CreateProjectRequest(BaseModel):
    """Request model for creating project."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    project_type: str = Field(default="classification", pattern="^(classification|detection|segmentation|custom)$")
    settings: Optional[Dict[str, Any]] = Field(default=None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Plant Species Classification",
                "description": "Project to classify different plant species using custom datasets",
                "project_type": "classification",
                "settings": {
                    "default_model": "imagenet_mobilenet_v2",
                    "auto_save_results": True,
                    "confidence_threshold": 0.7
                }
            }
        }

@router.post("/workspace/create")
async def create_workspace(
    request: CreateWorkspaceRequest,
    owner_id: str = Form(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Create a new collaboration workspace.
    
    Args:
        request: Workspace creation request
        owner_id: ID of workspace owner
    
    Returns:
        Created workspace information
    """
    
    try:
        result = await collaboration_service.create_workspace(
            name=request.name,
            description=request.description,
            owner_id=owner_id,
            settings=request.settings
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to create workspace")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create workspace: {str(e)}"
        )

@router.post("/workspace/{workspace_id}/members/add")
async def add_member_to_workspace(
    workspace_id: str,
    user_id: str = Form(...),
    role: UserRole = Form(...),
    invited_by: str = Form(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Add a member to workspace.
    
    Args:
        workspace_id: Workspace identifier
        user_id: User to add
        role: User role in workspace
        invited_by: User who sent the invitation
    
    Returns:
        Operation result
    """
    
    try:
        result = await collaboration_service.add_member_to_workspace(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
            invited_by=invited_by
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to add member")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add member: {str(e)}"
        )

@router.post("/workspace/{workspace_id}/project/create")
async def create_project(
    workspace_id: str,
    request: CreateProjectRequest,
    creator_id: str = Form(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Create a new project in workspace.
    
    Args:
        workspace_id: Workspace identifier
        request: Project creation request
        creator_id: User creating the project
    
    Returns:
        Created project information
    """
    
    try:
        result = await collaboration_service.create_project(
            workspace_id=workspace_id,
            name=request.name,
            description=request.description,
            creator_id=creator_id,
            project_type=request.project_type,
            settings=request.settings
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to create project")
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}"
        )

@router.get("/workspace/{workspace_id}")
async def get_workspace_info(
    workspace_id: str,
    user_id: str = Query(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Get detailed workspace information.
    
    Args:
        workspace_id: Workspace identifier
        user_id: User requesting the information
    
    Returns:
        Workspace information
    """
    
    try:
        result = await collaboration_service.get_workspace_info(
            workspace_id=workspace_id,
            requesting_user_id=user_id
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
            detail=f"Failed to get workspace info: {str(e)}"
        )

@router.get("/user/{user_id}/workspaces")
async def get_user_workspaces(
    user_id: str,
    requesting_user_id: str = Query(...)  # In production, validate this matches user_id or admin
) -> Dict[str, Any]:
    """
    Get workspaces where user is a member.
    
    Args:
        user_id: User identifier
        requesting_user_id: User making the request
    
    Returns:
        User's workspaces
    """
    
    # In production, validate that requesting_user_id matches user_id or has admin privileges
    if requesting_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only view own workspaces"
        )
    
    try:
        result = await collaboration_service.get_user_workspaces(user_id)
        
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
            detail=f"Failed to get user workspaces: {str(e)}"
        )

@router.get("/project/{project_id}")
async def get_project_info(
    project_id: str,
    user_id: str = Query(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Get detailed project information.
    
    Args:
        project_id: Project identifier
        user_id: User requesting the information
    
    Returns:
        Project information
    """
    
    try:
        result = await collaboration_service.get_project_info(
            project_id=project_id,
            requesting_user_id=user_id
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
            detail=f"Failed to get project info: {str(e)}"
        )

@router.get("/workspace/{workspace_id}/activities")
async def get_workspace_activities(
    workspace_id: str,
    user_id: str = Query(...),  # In production, this would come from authentication
    limit: int = Query(50, ge=1, le=100)
) -> Dict[str, Any]:
    """
    Get recent activities in workspace.
    
    Args:
        workspace_id: Workspace identifier
        user_id: User requesting activities
        limit: Maximum number of activities
    
    Returns:
        Recent activities
    """
    
    try:
        result = await collaboration_service.get_workspace_activities(
            workspace_id=workspace_id,
            requesting_user_id=user_id,
            limit=limit
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
            detail=f"Failed to get workspace activities: {str(e)}"
        )

@router.get("/roles")
async def get_available_roles() -> Dict[str, Any]:
    """
    Get available user roles and their permissions.
    
    Returns:
        Available roles and permissions
    """
    
    roles_info = [
        {
            "role": "owner",
            "name": "Owner",
            "description": "Full control over workspace and all projects",
            "permissions": ["All permissions"]
        },
        {
            "role": "admin",
            "name": "Administrator", 
            "description": "Manage workspace, projects, and members",
            "permissions": [
                "Create/edit/delete projects",
                "Invite/remove members",
                "Manage user roles",
                "Edit workspace settings",
                "View all projects"
            ]
        },
        {
            "role": "member",
            "name": "Member",
            "description": "Create and manage own projects, collaborate on shared projects",
            "permissions": [
                "Create projects",
                "Edit own projects", 
                "View shared projects",
                "Classify images",
                "Export results"
            ]
        },
        {
            "role": "viewer",
            "name": "Viewer",
            "description": "View projects and results only",
            "permissions": [
                "View projects",
                "View results",
                "Export results (read-only)"
            ]
        }
    ]
    
    return {
        "roles": roles_info,
        "default_role": "member"
    }

@router.get("/project/types")
async def get_project_types() -> Dict[str, Any]:
    """
    Get available project types and their descriptions.
    
    Returns:
        Available project types
    """
    
    project_types = [
        {
            "type": "classification",
            "name": "Image Classification",
            "description": "Classify images into predefined categories",
            "features": [
                "Single-label classification",
                "Multi-label classification",
                "Custom model support",
                "Batch processing"
            ]
        },
        {
            "type": "detection",
            "name": "Object Detection",
            "description": "Detect and locate objects within images",
            "features": [
                "Bounding box detection",
                "Multi-object detection",
                "Custom object classes",
                "Real-time processing"
            ]
        },
        {
            "type": "segmentation",
            "name": "Semantic Segmentation",
            "description": "Classify each pixel in an image",
            "features": [
                "Pixel-level classification",
                "Multi-class segmentation",
                "Medical image support",
                "Custom annotations"
            ]
        },
        {
            "type": "custom",
            "name": "Custom Project",
            "description": "Custom AI project with flexible configuration",
            "features": [
                "Custom workflows",
                "Multi-modal support",
                "Experimental features",
                "Research capabilities"
            ]
        }
    ]
    
    return {
        "project_types": project_types,
        "default_type": "classification"
    }

@router.get("/workspace/{workspace_id}/statistics")
async def get_workspace_statistics(
    workspace_id: str,
    user_id: str = Query(...)  # In production, this would come from authentication
) -> Dict[str, Any]:
    """
    Get workspace statistics and analytics.
    
    Args:
        workspace_id: Workspace identifier
        user_id: User requesting statistics
    
    Returns:
        Workspace statistics
    """
    
    try:
        # Get workspace info to access statistics
        workspace_info = await collaboration_service.get_workspace_info(
            workspace_id=workspace_id,
            requesting_user_id=user_id
        )
        
        if "error" in workspace_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=workspace_info["error"]
            )
        
        # Enhanced statistics
        statistics = workspace_info.get("statistics", {})
        
        # Add project type breakdown
        project_type_counts = {}
        total_classifications = 0
        
        for project in workspace_info.get("projects", []):
            project_type = project.get("type", "unknown")
            project_type_counts[project_type] = project_type_counts.get(project_type, 0) + 1
            total_classifications += project.get("statistics", {}).get("total_classifications", 0)
        
        enhanced_statistics = {
            **statistics,
            "project_type_breakdown": project_type_counts,
            "total_workspace_classifications": total_classifications,
            "average_classifications_per_project": (
                total_classifications / max(statistics.get("total_projects", 1), 1)
            ),
            "member_role_breakdown": self._get_member_role_breakdown(workspace_info.get("members", []))
        }
        
        return {
            "workspace_id": workspace_id,
            "statistics": enhanced_statistics,
            "generated_at": "2025-09-03T12:00:00Z"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get workspace statistics: {str(e)}"
        )

def _get_member_role_breakdown(members: List[Dict[str, Any]]) -> Dict[str, int]:
    """Get breakdown of member roles."""
    role_counts = {}
    for member in members:
        role = member.get("role", "unknown")
        role_counts[role] = role_counts.get(role, 0) + 1
    return role_counts

@router.get("/search/workspaces")
async def search_workspaces(
    query: str = Query(..., min_length=2),
    user_id: str = Query(...),  # In production, this would come from authentication
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
) -> Dict[str, Any]:
    """
    Search for workspaces accessible to user.
    
    Args:
        query: Search query
        user_id: User performing search
        page: Page number
        page_size: Results per page
    
    Returns:
        Search results
    """
    
    try:
        # Get user's workspaces
        user_workspaces_result = await collaboration_service.get_user_workspaces(user_id)
        
        if "error" in user_workspaces_result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=user_workspaces_result["error"]
            )
        
        # Filter workspaces by search query
        query_lower = query.lower()
        matching_workspaces = []
        
        for workspace in user_workspaces_result["workspaces"]:
            if (query_lower in workspace["name"].lower() or 
                query_lower in workspace["description"].lower()):
                matching_workspaces.append(workspace)
        
        # Pagination
        total_results = len(matching_workspaces)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_results = matching_workspaces[start_idx:end_idx]
        
        return {
            "query": query,
            "results": page_results,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_results": total_results,
                "total_pages": (total_results + page_size - 1) // page_size
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )