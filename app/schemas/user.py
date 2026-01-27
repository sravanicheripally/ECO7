from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional,List


class UserRoleResponse(BaseModel):
    id: UUID
    name: str
    code: str

    class Config:
        from_attributes = True


class UserMeResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    username: str
    is_active: bool
    roles: list[UserRoleResponse]


    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    username: str
    password: str
    user_role_ids: Optional[List[UUID]] = []


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class UserRoleUpdate(BaseModel):
    user_role_id: UUID


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    username: str
    is_active: bool
    role_name: str
    role_code: str


class UserListItem(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    username: str
    is_active: bool
    role_name: str
    role_code: str

    class Config:
        from_attributes = True