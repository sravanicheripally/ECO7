from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.department_role import DepartmentRole

router = APIRouter(
    prefix="/department-roles",
    tags=["Department Roles"]
)

# ------------------------------------------------
# GET ALL ROLES
# ------------------------------------------------
@router.get("/")
def get_all_roles(db: Session = Depends(get_db)):
    return db.query(DepartmentRole).filter(
        DepartmentRole.is_active == True
    ).all()


# ------------------------------------------------
# GET ROLE BY ID
# ------------------------------------------------
@router.get("/{role_id}")
def get_role(role_id: UUID, db: Session = Depends(get_db)):
    role = db.query(DepartmentRole).filter(
        DepartmentRole.id == role_id,
        DepartmentRole.is_active == True
    ).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role


# ------------------------------------------------
# CREATE ROLE
# ------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_role(
    name: str,
    code: str,
    is_default: bool = False,
    db: Session = Depends(get_db),
):
    exists = db.query(DepartmentRole).filter(
        (DepartmentRole.name == name) |
        (DepartmentRole.code == code)
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = DepartmentRole(
        name=name,
        code=code,
        is_default=is_default,
        is_active=True
    )

    db.add(role)
    db.commit()
    db.refresh(role)
    return role


# ------------------------------------------------
# UPDATE ROLE
# ------------------------------------------------
@router.put("/{role_id}")
def update_role(
    role_id: UUID,
    name: str | None = None,
    code: str | None = None,
    is_default: bool | None = None,
    db: Session = Depends(get_db),
):
    role = db.query(DepartmentRole).filter(
        DepartmentRole.id == role_id,
        DepartmentRole.is_active == True
    ).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if name is not None:
        role.name = name
    if code is not None:
        role.code = code
    if is_default is not None:
        role.is_default = is_default

    db.commit()
    db.refresh(role)
    return role


# ------------------------------------------------
# DELETE ROLE (SOFT DELETE)
# ------------------------------------------------
@router.delete("/{role_id}")
def delete_role(role_id: UUID, db: Session = Depends(get_db)):
    role = db.query(DepartmentRole).filter(
        DepartmentRole.id == role_id,
        DepartmentRole.is_active == True
    ).first()

    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    role.is_active = False
    db.commit()

    return {"message": "Role deleted successfully"}
