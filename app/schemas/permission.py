from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserPermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    category: str = "general"
    module: Optional[str] = None
    is_active: bool = True

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
