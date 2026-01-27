from pydantic import BaseModel
from uuid import UUID

class UserRoleResponse(BaseModel):
    id: UUID
    name: str
    code: str
    description: str | None
