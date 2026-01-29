from pydantic import BaseModel, field_validator
from uuid import UUID
from typing import Optional
import re

class UserPermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    category: str = "general"
    module: Optional[str] = None
    is_active: bool = True

    @field_validator('code', mode='before')
    @classmethod
    def validate_and_normalize_code(cls, v):
        """Normalize permission code to UPPERCASE_WITH_UNDERSCORES format"""
        if not v:
            raise ValueError("Permission code cannot be empty")
        
        # Convert to uppercase
        v = v.strip().upper()
        
        # Check if code contains only alphanumeric and underscores
        if not re.match(r'^[A-Z0-9_]+$', v):
            raise ValueError(
                "Permission code must contain only uppercase letters, numbers, and underscores. "
                "Example: CREATE_USER, VIEW_REPORTS"
            )
        
        # Check length
        if len(v) < 3 or len(v) > 100:
            raise ValueError("Permission code must be between 3 and 100 characters")
        
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate permission name"""
        if not v or len(v.strip()) == 0:
            raise ValueError("Permission name cannot be empty")
        
        if len(v) > 100:
            raise ValueError("Permission name must be less than 100 characters")
        
        return v.strip()

    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        """Validate category"""
        if not v or len(v.strip()) == 0:
            raise ValueError("Category cannot be empty")
        
        # Convert to lowercase
        return v.strip().lower()

class UserPermissionCreate(UserPermissionBase):
    pass

class UserPermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    module: Optional[str] = None
    is_active: Optional[bool] = None

class UserPermissionResponse(UserPermissionBase):
    id: UUID

    class Config:
        from_attributes = True

class UserRolePermissionCreate(BaseModel):
    permission_id: UUID

class UserRolePermissionResponse(BaseModel):
    id: UUID
    user_role_id: UUID
    permission_id: UUID

    class Config:
        from_attributes = True
