from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import (
    require_department_admin,
    require_department_owner,
)
from app.models.department import Department
from app.models.user import User
from app.models.user_department import UserDepartment
from app.models.department_role import DepartmentRole

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

# =========================================================
# CREATE DEPARTMENT (DEPARTMENT ADMIN ONLY)
# =========================================================
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_department(
    name: str,
    description: str | None = None,
    current_user: User = Depends(require_department_admin),
    db: Session = Depends(get_db),
):
    department = Department(
        name=name,
        description=description,
        is_active=True,
    )
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


# =========================================================
# GET ALL DEPARTMENTS (READ ONLY)
# =========================================================
@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).filter(Department.is_active == True).all()


# =========================================================
# GET DEPARTMENT BY ID (READ ONLY)
# =========================================================
@router.get("/{department_id}")
def get_department(department_id: UUID, db: Session = Depends(get_db)):
    department = db.query(Department).filter(
        Department.id == department_id,
        Department.is_active == True
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return department


# =========================================================
# DELETE DEPARTMENT (DEPARTMENT ADMIN ONLY)
# =========================================================
@router.delete("/{department_id}")
def delete_department(
    department_id: UUID,
    current_user: User = Depends(require_department_admin),
    db: Session = Depends(get_db),
):
    department = db.query(Department).filter(
        Department.id == department_id,
        Department.is_active == True
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    department.is_active = False
    db.commit()

    return {"message": "Department deleted successfully"}


# =========================================================
# ASSIGN OWNER TO DEPARTMENT (DEPARTMENT ADMIN ONLY)
# =========================================================
@router.put("/{department_id}/assign-owner", status_code=200)
def assign_department_owner(
    department_id: UUID,
    user_id: UUID,
    current_user: User = Depends(require_department_admin),
    db: Session = Depends(get_db),
):
    owner_role = db.query(DepartmentRole).filter(
        DepartmentRole.code == "OWNER",
        DepartmentRole.is_active == True
    ).first()

    if not owner_role:
        raise HTTPException(status_code=500, detail="Owner role not configured")

    assignment = db.query(UserDepartment).filter(
        UserDepartment.department_id == department_id,
        UserDepartment.user_id == user_id,
        UserDepartment.is_active == True
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="User must be assigned to department before becoming owner"
        )

    assignment.department_role_id = owner_role.id
    db.commit()

    return {
        "message": "User promoted to Department Owner",
        "department_id": department_id,
        "user_id": user_id
    }


