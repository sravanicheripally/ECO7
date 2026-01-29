from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class DocumentTypeRoleBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    role_level: int = 0
    is_predefined: bool = False
    is_active: bool = True


class DocumentTypeRoleCreate(DocumentTypeRoleBase):
    pass


class DocumentTypeRoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    role_level: Optional[int] = None
    is_predefined: Optional[bool] = None
    is_active: Optional[bool] = None


class DocumentTypeRoleResponse(DocumentTypeRoleBase):
    id: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
