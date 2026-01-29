from pydantic import BaseModel, field_validator
from uuid import UUID
from typing import Optional
import re


class UserRoleCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_system_role: bool = False
    is_predefined: bool = False

    @field_validator('code', mode='before')
    @classmethod
    def validate_and_normalize_code(cls, v):
        """Normalize role code to UPPERCASE_WITH_UNDERSCORES format"""
        if not v:
            raise ValueError("Role code cannot be empty")
        
        # Convert to uppercase
        v = v.strip().upper()
        
        # Check if code contains only alphanumeric and underscores
        if not re.match(r'^[A-Z0-9_]+$', v):
            raise ValueError(
                "Role code must contain only uppercase letters, numbers, and underscores. "
                "Example: SUPER_ADMIN, DEPARTMENT_ADMIN"
            )
        
        # Check length
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Role code must be between 3 and 50 characters")
        
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate role name"""
        if not v or len(v.strip()) == 0:
            raise ValueError("Role name cannot be empty")
        
        if len(v) > 100:
            raise ValueError("Role name must be less than 100 characters")
        
        return v.strip()


class UserRoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class UserRoleResponse(BaseModel):
    id: UUID
    name: str
    code: str
    description: Optional[str]
    is_system_role: bool
    is_predefined: bool
    is_active: bool

    class Config:
        from_attributes = True
