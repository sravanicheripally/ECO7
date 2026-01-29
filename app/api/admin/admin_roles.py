from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_super_admin
from app.models.user import User
from app.models.user_role import UserRole
from app.schemas.user_role import (
    UserRoleCreate,
    UserRoleUpdate,
    UserRoleResponse
)

router = APIRouter(
    prefix="/admin/user-roles",
    tags=["Admin - User Roles"]
)

# ------------------------------------------------
# GET ALL USER ROLES (SUPER / USER ADMIN)
# ------------------------------------------------
@router.get("/", response_model=list[UserRoleResponse])
def get_all_roles(
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db),
):
    return (
        db.query(UserRole)
        .filter(UserRole.is_active == True)
        .all()
    )


# ------------------------------------------------
# GET SINGLE ROLE BY ID (SUPER / USER ADMIN)
# ------------------------------------------------
@router.get("/{role_id}", response_model=UserRoleResponse)
def get_role(
    role_id: UUID,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db),
):
    role = (
        db.query(UserRole)
        .filter(
            UserRole.id == role_id,
            UserRole.is_active == True
        )
        .first()
    )

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


# ------------------------------------------------
# CREATE ROLE (SUPER / USER ADMIN)
# ------------------------------------------------
@router.post(
    "/",
    response_model=UserRoleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_role(
    payload: UserRoleCreate,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db),
):
    exists = (
        db.query(UserRole)
        .filter(
            (UserRole.name == payload.name) |
            (UserRole.code == payload.code)
        )
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Role with same name or code already exists"
        )

    role = UserRole(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        is_system_role=payload.is_system_role,
        is_predefined=payload.is_predefined,
        is_active=True,
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


# ------------------------------------------------
# UPDATE ROLE (NON-SYSTEM ONLY)
# ------------------------------------------------
@router.put("/{role_id}", response_model=UserRoleResponse)
def update_role(
    role_id: UUID,
    payload: UserRoleUpdate,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db),
):
    role = (
        db.query(UserRole)
        .filter(
            UserRole.id == role_id,
            UserRole.is_active == True
        )
        .first()
    )

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.is_system_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System roles cannot be modified"
        )

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(role, field, value)

    db.commit()
    db.refresh(role)

    return role


# ------------------------------------------------
# DELETE ROLE (SOFT DELETE, NON-SYSTEM ONLY)
# ------------------------------------------------
@router.delete("/{role_id}", status_code=status.HTTP_200_OK)
def delete_role(
    role_id: UUID,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db),
):
    role = (
        db.query(UserRole)
        .filter(
            UserRole.id == role_id,
            UserRole.is_active == True
        )
        .first()
    )

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.is_system_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System roles cannot be deleted"
        )

    role.is_active = False
    db.commit()

    return {"message": "Role deleted successfully"}
