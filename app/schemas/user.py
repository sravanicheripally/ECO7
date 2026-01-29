from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional, List


class UserRoleResponse(BaseModel):
    id: UUID
    name: str
    code: str

    class Config:
        from_attributes = True


class UserMeResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    username: str
    is_active: bool
    roles: List[UserRoleResponse]

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Response after successful login with user roles"""
    access_token: str
    refresh_token: str
    token_type: str
    user: UserMeResponse

    class Config:
        from_attributes = True


   



class UserCreate(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str
    mobile: Optional[str] = None
    user_role_ids: Optional[List[UUID]] = []


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    mobile: Optional[str] = None
    is_active: Optional[bool] = None


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
    name: str
    email: EmailStr
    username: str
    mobile: Optional[str]
    is_active: bool
    roles: List[UserRoleResponse]

    class Config:
        from_attributes = True
