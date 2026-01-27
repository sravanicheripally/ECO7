from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class UserRoleCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_system_role: bool = False
    is_predefined: bool = False


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
