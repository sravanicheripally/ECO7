from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.models.user_role import UserRole
from app.models.user_user_role import UserUserRole

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserListItem,
)

router = APIRouter(prefix="/users", tags=["Users"])

# ------------------------------------------------
# GET SYSTEM USER ROLES
# ------------------------------------------------

@router.get("/roles")
def get_user_roles(db: Session = Depends(get_db)):
    return db.query(UserRole).filter(UserRole.is_active == True).all()


# ------------------------------------------------
# GET ALL USERS (WITH MULTIPLE ROLES)
# ------------------------------------------------
@router.get("", response_model=list[UserListItem])
def get_all_users(
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
):
    users_query = db.query(User)

    if not include_inactive:
        users_query = users_query.filter(User.is_active == True)

    users = users_query.all()
    response = []

    for user in users:
        roles = (
            db.query(UserRole)
            .join(UserUserRole, UserRole.id == UserUserRole.user_role_id)
            .filter(UserUserRole.user_id == user.id)
            .all()
        )

        response.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "username": user.username,
            "mobile": user.mobile,
            "is_active": user.is_active,
            "roles": [
                {
                    "id": role.id,
                    "name": role.name,
                    "code": role.code
                }
                for role in roles
            ]
        })

    return response



# ------------------------------------------------
# GET PARTICULAR USER
# ------------------------------------------------
@router.get("/{id}")
def get_user_by_id(id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    roles = (
        db.query(UserRole)
        .join(UserUserRole, UserRole.id == UserUserRole.user_role_id)
        .filter(UserUserRole.user_id == user.id)
        .all()
    )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "roles": [
            {
                "id": role.id,
                "name": role.name,
                "code": role.code
            }
            for role in roles
        ]
    }


# ------------------------------------------------
# CREATE USER (DEFAULT + MULTIPLE ROLES)
# ------------------------------------------------
@router.post("")
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):

    user = User(
        name=payload.name,
        email=payload.email,
        username=payload.username,
        password=hash_password(payload.password),
        is_active=True,
        created_at=datetime.utcnow(),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # DEFAULT ROLE (Departments)
    default_role = db.query(UserRole).filter(
        UserRole.code == "DEPARTMENTS"
    ).first()

    if not default_role:
        raise HTTPException(500, "Default role missing")

    # Collect all role IDs, ensuring default role is included and no duplicates
    role_ids_set = set(payload.user_role_ids or [])
    role_ids_set.add(default_role.id)

    # Add all roles
    for role_id in role_ids_set:
        db.add(UserUserRole(
            user_id=user.id,
            user_role_id=role_id
        ))

    db.commit()
    return {"id": user.id}



# ------------------------------------------------
# UPDATE USER DETAILS
# ------------------------------------------------
@router.put("/{id}")
def update_user(
    id: UUID,
    payload: UserUpdate,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    return {"message": "User updated successfully"}


# ------------------------------------------------
# SOFT DELETE USER
# ------------------------------------------------
@router.delete("/{id}")
def delete_user(id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User permanently deleted"}



# ------------------------------------------------
# ADD ROLE TO USER
# ------------------------------------------------
@router.post("/{id}/roles/{role_id}")
def add_user_role(
    id: UUID,
    role_id: UUID,
    db: Session = Depends(get_db),
):
    exists = db.query(UserUserRole).filter(
        UserUserRole.user_id == id,
        UserUserRole.user_role_id == role_id
    ).first()

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Role already assigned to user"
        )

    db.add(UserUserRole(
        user_id=id,
        user_role_id=role_id
    ))
    db.commit()

    return {"message": "Role assigned successfully"}


# ------------------------------------------------
# REMOVE ROLE FROM USER
# ------------------------------------------------
@router.delete("/{id}/roles/{role_id}")
def remove_user_role(
    id: UUID,
    role_id: UUID,
    db: Session = Depends(get_db),
):
    deleted = db.query(UserUserRole).filter(
        UserUserRole.user_id == id,
        UserUserRole.user_role_id == role_id
    ).delete()

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Role assignment not found"
        )

    db.commit()
    return {"message": "Role removed successfully"}


