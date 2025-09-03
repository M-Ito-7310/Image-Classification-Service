"""
Team collaboration service for shared workspaces and projects.
Enables users to collaborate on AI classification projects.
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

from app.services.cache_service import CacheService
from app.core.config import settings


class UserRole(str, Enum):
    """User roles in workspace."""
    OWNER = "owner"
    ADMIN = "admin" 
    MEMBER = "member"
    VIEWER = "viewer"


class WorkspaceStatus(str, Enum):
    """Workspace status."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"


class ProjectStatus(str, Enum):
    """Project status."""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CollaborationService:
    """Service for managing team collaboration and shared workspaces."""
    
    def __init__(self):
        self.cache_service = CacheService()
        self.storage_path = Path(settings.MODEL_STORAGE_PATH) / "collaboration"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Data files
        self.workspaces_file = self.storage_path / "workspaces.json"
        self.projects_file = self.storage_path / "projects.json"
        self.activities_file = self.storage_path / "activities.json"
        
        # Load data
        self.workspaces = self._load_json_file(self.workspaces_file, {})
        self.projects = self._load_json_file(self.projects_file, {})
        self.activities = self._load_json_file(self.activities_file, [])
    
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
    
    async def create_workspace(
        self,
        name: str,
        description: str,
        owner_id: str,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new collaboration workspace.
        
        Args:
            name: Workspace name
            description: Workspace description
            owner_id: ID of workspace owner
            settings: Workspace settings
        
        Returns:
            Created workspace information
        """
        
        try:
            workspace_id = str(uuid.uuid4())
            
            workspace = {
                "workspace_id": workspace_id,
                "name": name,
                "description": description,
                "owner_id": owner_id,
                "status": WorkspaceStatus.ACTIVE,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "settings": settings or {
                    "allow_public_projects": False,
                    "require_approval_for_members": True,
                    "max_projects": 10,
                    "max_members": 20
                },
                "members": {
                    owner_id: {
                        "user_id": owner_id,
                        "role": UserRole.OWNER,
                        "joined_at": datetime.utcnow().isoformat(),
                        "permissions": ["all"]
                    }
                },
                "projects": [],
                "statistics": {
                    "total_projects": 0,
                    "active_projects": 0,
                    "total_classifications": 0,
                    "total_members": 1
                }
            }
            
            # Save workspace
            self.workspaces[workspace_id] = workspace
            self._save_json_file(self.workspaces_file, self.workspaces)
            
            # Log activity
            await self._log_activity(
                workspace_id=workspace_id,
                user_id=owner_id,
                action="workspace_created",
                details={"workspace_name": name}
            )
            
            # Cache workspace info
            await self.cache_service.set(
                f"workspace:{workspace_id}",
                json.dumps(workspace),
                ttl=3600
            )
            
            return {
                "success": True,
                "workspace": {
                    "workspace_id": workspace_id,
                    "name": name,
                    "description": description,
                    "status": workspace["status"],
                    "created_at": workspace["created_at"],
                    "member_count": 1,
                    "project_count": 0
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create workspace: {str(e)}"
            }
    
    async def add_member_to_workspace(
        self,
        workspace_id: str,
        user_id: str,
        role: UserRole,
        invited_by: str
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
            if workspace_id not in self.workspaces:
                return {"success": False, "error": "Workspace not found"}
            
            workspace = self.workspaces[workspace_id]
            
            # Check if user is already a member
            if user_id in workspace["members"]:
                return {"success": False, "error": "User is already a member"}
            
            # Check if inviter has permission
            if invited_by not in workspace["members"]:
                return {"success": False, "error": "Inviter is not a workspace member"}
            
            inviter_role = workspace["members"][invited_by]["role"]
            if inviter_role not in [UserRole.OWNER, UserRole.ADMIN]:
                return {"success": False, "error": "Insufficient permissions to invite members"}
            
            # Check member limit
            max_members = workspace["settings"].get("max_members", 20)
            if len(workspace["members"]) >= max_members:
                return {"success": False, "error": f"Workspace member limit ({max_members}) reached"}
            
            # Add member
            workspace["members"][user_id] = {
                "user_id": user_id,
                "role": role,
                "joined_at": datetime.utcnow().isoformat(),
                "invited_by": invited_by,
                "permissions": self._get_role_permissions(role)
            }
            
            workspace["updated_at"] = datetime.utcnow().isoformat()
            workspace["statistics"]["total_members"] = len(workspace["members"])
            
            # Save changes
            self._save_json_file(self.workspaces_file, self.workspaces)
            
            # Log activity
            await self._log_activity(
                workspace_id=workspace_id,
                user_id=invited_by,
                action="member_added",
                details={
                    "new_member": user_id,
                    "role": role
                }
            )
            
            # Update cache
            await self.cache_service.set(
                f"workspace:{workspace_id}",
                json.dumps(workspace),
                ttl=3600
            )
            
            return {
                "success": True,
                "message": f"User {user_id} added to workspace with role {role}",
                "member_info": workspace["members"][user_id]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to add member: {str(e)}"
            }
    
    def _get_role_permissions(self, role: UserRole) -> List[str]:
        """Get permissions for user role."""
        permissions_map = {
            UserRole.OWNER: ["all"],
            UserRole.ADMIN: [
                "create_project", "edit_project", "delete_project",
                "invite_members", "remove_members", "manage_roles",
                "view_all_projects", "edit_workspace_settings"
            ],
            UserRole.MEMBER: [
                "create_project", "edit_own_project", "view_projects",
                "classify_images", "view_results", "export_data"
            ],
            UserRole.VIEWER: [
                "view_projects", "view_results"
            ]
        }
        return permissions_map.get(role, [])
    
    async def create_project(
        self,
        workspace_id: str,
        name: str,
        description: str,
        creator_id: str,
        project_type: str = "classification",
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new project in workspace.
        
        Args:
            workspace_id: Workspace identifier
            name: Project name
            description: Project description
            creator_id: User creating the project
            project_type: Type of project
            settings: Project settings
        
        Returns:
            Created project information
        """
        
        try:
            if workspace_id not in self.workspaces:
                return {"success": False, "error": "Workspace not found"}
            
            workspace = self.workspaces[workspace_id]
            
            # Check creator permissions
            if creator_id not in workspace["members"]:
                return {"success": False, "error": "User is not a workspace member"}
            
            creator_permissions = workspace["members"][creator_id]["permissions"]
            if "create_project" not in creator_permissions and "all" not in creator_permissions:
                return {"success": False, "error": "Insufficient permissions to create project"}
            
            # Check project limit
            max_projects = workspace["settings"].get("max_projects", 10)
            if len(workspace["projects"]) >= max_projects:
                return {"success": False, "error": f"Workspace project limit ({max_projects}) reached"}
            
            project_id = str(uuid.uuid4())
            
            project = {
                "project_id": project_id,
                "workspace_id": workspace_id,
                "name": name,
                "description": description,
                "type": project_type,
                "creator_id": creator_id,
                "status": ProjectStatus.DRAFT,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "settings": settings or {
                    "default_model": "imagenet_mobilenet_v2",
                    "auto_save_results": True,
                    "allow_batch_processing": True,
                    "confidence_threshold": 0.5
                },
                "collaborators": {
                    creator_id: {
                        "user_id": creator_id,
                        "role": "owner",
                        "joined_at": datetime.utcnow().isoformat(),
                        "permissions": ["all"]
                    }
                },
                "classifications": [],
                "datasets": [],
                "models": [],
                "statistics": {
                    "total_classifications": 0,
                    "total_images": 0,
                    "avg_confidence": 0.0,
                    "last_activity": datetime.utcnow().isoformat()
                }
            }
            
            # Add project to workspace
            workspace["projects"].append(project_id)
            workspace["statistics"]["total_projects"] += 1
            workspace["statistics"]["active_projects"] += 1
            workspace["updated_at"] = datetime.utcnow().isoformat()
            
            # Save project
            self.projects[project_id] = project
            self._save_json_file(self.projects_file, self.projects)
            self._save_json_file(self.workspaces_file, self.workspaces)
            
            # Log activity
            await self._log_activity(
                workspace_id=workspace_id,
                project_id=project_id,
                user_id=creator_id,
                action="project_created",
                details={
                    "project_name": name,
                    "project_type": project_type
                }
            )
            
            # Cache project info
            await self.cache_service.set(
                f"project:{project_id}",
                json.dumps(project),
                ttl=3600
            )
            
            return {
                "success": True,
                "project": {
                    "project_id": project_id,
                    "name": name,
                    "description": description,
                    "type": project_type,
                    "status": project["status"],
                    "created_at": project["created_at"],
                    "creator_id": creator_id,
                    "workspace_id": workspace_id
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create project: {str(e)}"
            }
    
    async def get_workspace_info(
        self,
        workspace_id: str,
        requesting_user_id: str
    ) -> Dict[str, Any]:
        """
        Get detailed workspace information.
        
        Args:
            workspace_id: Workspace identifier
            requesting_user_id: User requesting the information
        
        Returns:
            Workspace information
        """
        
        try:
            # Check cache first
            cached_workspace = await self.cache_service.get(f"workspace:{workspace_id}")
            if cached_workspace:
                workspace = json.loads(cached_workspace)
            else:
                if workspace_id not in self.workspaces:
                    return {"error": "Workspace not found"}
                
                workspace = self.workspaces[workspace_id]
                
                # Cache for future requests
                await self.cache_service.set(
                    f"workspace:{workspace_id}",
                    json.dumps(workspace),
                    ttl=3600
                )
            
            # Check user permissions
            if requesting_user_id not in workspace["members"]:
                return {"error": "Access denied"}
            
            # Prepare response (remove sensitive info)
            response = {
                "workspace_id": workspace["workspace_id"],
                "name": workspace["name"],
                "description": workspace["description"],
                "status": workspace["status"],
                "created_at": workspace["created_at"],
                "updated_at": workspace["updated_at"],
                "statistics": workspace["statistics"],
                "settings": workspace["settings"],
                "members": []
            }
            
            # Add member information (without sensitive details)
            for user_id, member_info in workspace["members"].items():
                response["members"].append({
                    "user_id": user_id,
                    "role": member_info["role"],
                    "joined_at": member_info["joined_at"]
                })
            
            # Add project summaries
            response["projects"] = []
            for project_id in workspace["projects"]:
                if project_id in self.projects:
                    project = self.projects[project_id]
                    response["projects"].append({
                        "project_id": project["project_id"],
                        "name": project["name"],
                        "type": project["type"],
                        "status": project["status"],
                        "creator_id": project["creator_id"],
                        "updated_at": project["updated_at"],
                        "statistics": project["statistics"]
                    })
            
            return response
            
        except Exception as e:
            return {"error": f"Failed to get workspace info: {str(e)}"}
    
    async def get_user_workspaces(self, user_id: str) -> Dict[str, Any]:
        """
        Get workspaces where user is a member.
        
        Args:
            user_id: User identifier
        
        Returns:
            User's workspaces
        """
        
        try:
            user_workspaces = []
            
            for workspace_id, workspace in self.workspaces.items():
                if user_id in workspace["members"]:
                    member_info = workspace["members"][user_id]
                    
                    workspace_summary = {
                        "workspace_id": workspace_id,
                        "name": workspace["name"],
                        "description": workspace["description"],
                        "status": workspace["status"],
                        "user_role": member_info["role"],
                        "joined_at": member_info["joined_at"],
                        "member_count": len(workspace["members"]),
                        "project_count": len(workspace["projects"]),
                        "last_updated": workspace["updated_at"]
                    }
                    
                    user_workspaces.append(workspace_summary)
            
            # Sort by last updated
            user_workspaces.sort(key=lambda x: x["last_updated"], reverse=True)
            
            return {
                "workspaces": user_workspaces,
                "total_workspaces": len(user_workspaces)
            }
            
        except Exception as e:
            return {
                "error": f"Failed to get user workspaces: {str(e)}",
                "workspaces": []
            }
    
    async def get_project_info(
        self,
        project_id: str,
        requesting_user_id: str
    ) -> Dict[str, Any]:
        """
        Get detailed project information.
        
        Args:
            project_id: Project identifier
            requesting_user_id: User requesting the information
        
        Returns:
            Project information
        """
        
        try:
            # Check cache first
            cached_project = await self.cache_service.get(f"project:{project_id}")
            if cached_project:
                project = json.loads(cached_project)
            else:
                if project_id not in self.projects:
                    return {"error": "Project not found"}
                
                project = self.projects[project_id]
                
                # Cache for future requests
                await self.cache_service.set(
                    f"project:{project_id}",
                    json.dumps(project),
                    ttl=3600
                )
            
            # Check user access
            workspace_id = project["workspace_id"]
            if workspace_id not in self.workspaces:
                return {"error": "Associated workspace not found"}
            
            workspace = self.workspaces[workspace_id]
            if requesting_user_id not in workspace["members"]:
                return {"error": "Access denied"}
            
            # Prepare response
            response = {
                "project_id": project["project_id"],
                "workspace_id": project["workspace_id"],
                "name": project["name"],
                "description": project["description"],
                "type": project["type"],
                "status": project["status"],
                "creator_id": project["creator_id"],
                "created_at": project["created_at"],
                "updated_at": project["updated_at"],
                "settings": project["settings"],
                "statistics": project["statistics"],
                "collaborators": list(project["collaborators"].keys()),
                "recent_classifications": project["classifications"][-10:] if project["classifications"] else []
            }
            
            return response
            
        except Exception as e:
            return {"error": f"Failed to get project info: {str(e)}"}
    
    async def _log_activity(
        self,
        workspace_id: str,
        user_id: str,
        action: str,
        details: Optional[Dict[str, Any]] = None,
        project_id: Optional[str] = None
    ):
        """Log activity in workspace."""
        
        try:
            activity = {
                "activity_id": str(uuid.uuid4()),
                "workspace_id": workspace_id,
                "project_id": project_id,
                "user_id": user_id,
                "action": action,
                "details": details or {},
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.activities.append(activity)
            
            # Keep only last 1000 activities
            if len(self.activities) > 1000:
                self.activities = self.activities[-1000:]
            
            self._save_json_file(self.activities_file, self.activities)
            
        except Exception as e:
            print(f"Error logging activity: {e}")
    
    async def get_workspace_activities(
        self,
        workspace_id: str,
        requesting_user_id: str,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get recent activities in workspace.
        
        Args:
            workspace_id: Workspace identifier
            requesting_user_id: User requesting activities
            limit: Maximum number of activities
        
        Returns:
            Recent activities
        """
        
        try:
            # Check access
            if workspace_id not in self.workspaces:
                return {"error": "Workspace not found"}
            
            workspace = self.workspaces[workspace_id]
            if requesting_user_id not in workspace["members"]:
                return {"error": "Access denied"}
            
            # Filter activities for this workspace
            workspace_activities = [
                activity for activity in self.activities
                if activity["workspace_id"] == workspace_id
            ]
            
            # Sort by timestamp (newest first) and limit
            workspace_activities.sort(key=lambda x: x["timestamp"], reverse=True)
            workspace_activities = workspace_activities[:limit]
            
            return {
                "activities": workspace_activities,
                "total_activities": len(workspace_activities)
            }
            
        except Exception as e:
            return {
                "error": f"Failed to get workspace activities: {str(e)}",
                "activities": []
            }


# Global instance
collaboration_service = CollaborationService()