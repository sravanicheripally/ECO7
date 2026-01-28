from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import get_current_super_admin
from app.models.user import User
from app.models.user_permission import UserPermission
from app.models.user_role_permission import UserRolePermission
from app.models.user_role import UserRole
from app.schemas.permission import (
    UserPermissionCreate,
    UserPermissionUpdate,
    UserPermissionResponse,
    UserRolePermissionCreate,
)

router = APIRouter(prefix="/admin/permissions", tags=["Admin - Permissions"])


# ====================================
# PERMISSIONS MANAGEMENT
# ====================================

@router.get("", response_model=list[UserPermissionResponse])
def get_all_permissions(
    category: str = None,
    module: str = None,
    db: Session = Depends(get_db),
):
    """Get all permissions with optional filtering"""
    query = db.query(UserPermission)
    
    if category:
        query = query.filter(UserPermission.category == category)
    
    if module:
        query = query.filter(UserPermission.module == module)
    
    return query.all()


@router.get("/{id}", response_model=UserPermissionResponse)
def get_permission(id: UUID, db: Session = Depends(get_db)):
    """Get a specific permission by ID"""
    permission = db.query(UserPermission).filter(UserPermission.id == id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.post("", response_model=UserPermissionResponse)
def create_permission(
    payload: UserPermissionCreate,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Create a new permission (Super Admin only)"""
    
    # Check if permission already exists
    exists = db.query(UserPermission).filter(
        (UserPermission.name == payload.name) |
        (UserPermission.code == payload.code)
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Permission already exists")

    permission = UserPermission(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        category=payload.category,
        module=payload.module,
        is_active=payload.is_active
    )

    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


@router.put("/{id}", response_model=UserPermissionResponse)
def update_permission(
    id: UUID,
    payload: UserPermissionUpdate,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Update a permission (Super Admin only)"""
    permission = db.query(UserPermission).filter(UserPermission.id == id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(permission, field, value)

    db.commit()
    db.refresh(permission)
    return permission


@router.delete("/{id}")
def delete_permission(
    id: UUID,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Soft delete a permission (Super Admin only)"""
    permission = db.query(UserPermission).filter(UserPermission.id == id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    permission.is_active = False
    db.commit()

    return {"message": "Permission deleted successfully"}


# ====================================
# ROLE PERMISSIONS MANAGEMENT
# ====================================

@router.get("/role/{role_id}", response_model=list[UserPermissionResponse])
def get_role_permissions(
    role_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all permissions assigned to a role"""
    role = db.query(UserRole).filter(UserRole.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permissions = (
        db.query(UserPermission)
        .join(UserRolePermission, UserPermission.id == UserRolePermission.permission_id)
        .filter(UserRolePermission.user_role_id == role_id)
        .all()
    )
    return permissions


@router.post("/role/{role_id}/assign", response_model=dict)
def assign_permission_to_role(
    role_id: UUID,
    payload: UserRolePermissionCreate,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Assign a permission to a role"""
    
    # Check if role exists
    role = db.query(UserRole).filter(UserRole.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Check if permission exists
    permission = db.query(UserPermission).filter(
        UserPermission.id == payload.permission_id
    ).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    # Check if permission is already assigned to this role
    exists = db.query(UserRolePermission).filter(
        UserRolePermission.user_role_id == role_id,
        UserRolePermission.permission_id == payload.permission_id
    ).first()

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Permission already assigned to this role"
        )

    # Assign permission to role
    role_permission = UserRolePermission(
        user_role_id=role_id,
        permission_id=payload.permission_id
    )

    db.add(role_permission)
    db.commit()

    return {"message": "Permission assigned to role successfully"}


@router.delete("/role/{role_id}/permissions/{permission_id}")
def remove_permission_from_role(
    role_id: UUID,
    permission_id: UUID,
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Remove a permission from a role"""
    
    role_permission = db.query(UserRolePermission).filter(
        UserRolePermission.user_role_id == role_id,
        UserRolePermission.permission_id == permission_id
    ).first()

    if not role_permission:
        raise HTTPException(status_code=404, detail="Permission assignment not found")

    db.delete(role_permission)
    db.commit()

    return {"message": "Permission removed from role successfully"}


@router.post("/role/{role_id}/assign-bulk", response_model=dict)
def assign_permissions_bulk(
    role_id: UUID,
    payload: dict,  # {"permission_ids": [uuid1, uuid2, ...]}
    current_user: User = Depends(get_current_super_admin),
    db: Session = Depends(get_db)
):
    """Assign multiple permissions to a role at once"""
    
    role = db.query(UserRole).filter(UserRole.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permission_ids = payload.get("permission_ids", [])
    if not permission_ids:
        raise HTTPException(status_code=400, detail="No permission IDs provided")

    # Remove all existing permissions for this role
    db.query(UserRolePermission).filter(
        UserRolePermission.user_role_id == role_id
    ).delete()

    # Add new permissions
    for permission_id in permission_ids:
        permission = db.query(UserPermission).filter(
            UserPermission.id == permission_id
        ).first()
        
        if not permission:
            continue

        role_permission = UserRolePermission(
            user_role_id=role_id,
            permission_id=permission_id
        )
        db.add(role_permission)

    db.commit()

    return {
        "message": "Permissions assigned to role successfully",
        "count": len(permission_ids)
    }
