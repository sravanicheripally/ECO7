from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class DocumentTypeBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    icon: Optional[str] = None
    allowed_extensions: Optional[List[str]] = None
    max_file_size_mb: int = 100
    requires_approval: bool = False
    is_active: bool = True


class DocumentTypeCreate(DocumentTypeBase):
    pass


class DocumentTypeUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    icon: Optional[str]
    allowed_extensions: Optional[List[str]]
    max_file_size_mb: Optional[int]
    requires_approval: Optional[bool]
    is_active: Optional[bool]


class DocumentTypeResponse(DocumentTypeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID]
    updated_by: Optional[UUID]

    class Config:
        from_attributes = True  # SQLAlchemy compatibility
