from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.user_role import UserRole
from app.schemas.user_role import (
    UserRoleCreate,
    UserRoleUpdate,
    UserRoleResponse
)

router = APIRouter(prefix="/admin/user-roles", tags=["Admin - User Roles"])


@router.get("", response_model=list[UserRoleResponse])
def get_all_roles(db: Session = Depends(get_db)):
    return db.query(UserRole).all()


@router.get("/{id}", response_model=UserRoleResponse)
def get_role(id: UUID, db: Session = Depends(get_db)):
    role = db.query(UserRole).filter(UserRole.id == id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("", response_model=UserRoleResponse)
def create_role(payload: UserRoleCreate, db: Session = Depends(get_db)):

    exists = db.query(UserRole).filter(
        (UserRole.name == payload.name) |
        (UserRole.code == payload.code)
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = UserRole(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        is_system_role=payload.is_system_role,
        is_predefined=payload.is_predefined,
        is_active=True
    )

    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.put("/{id}", response_model=UserRoleResponse)
def update_role(
    id: UUID,
    payload: UserRoleUpdate,
    db: Session = Depends(get_db)
):
    role = db.query(UserRole).filter(UserRole.id == id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.is_system_role:
        raise HTTPException(
            status_code=403,
            detail="System roles cannot be modified"
        )

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(role, field, value)

    db.commit()
    db.refresh(role)
    return role


@router.delete("/{id}")
def delete_role(id: UUID, db: Session = Depends(get_db)):
    role = db.query(UserRole).filter(UserRole.id == id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.is_system_role:
        raise HTTPException(
            status_code=403,
            detail="System roles cannot be deleted"
        )

    role.is_active = False
    db.commit()

    return {"message": "Role deleted successfully"}
