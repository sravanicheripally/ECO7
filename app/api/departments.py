# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from uuid import UUID

# from app.core.database import get_db
# from app.models.department import Department
# from app.models.user_department import UserDepartment
# from app.models.department_role import DepartmentRole
# from app.models.user import User

# router = APIRouter(prefix="/departments", tags=["Departments"])

# #CREATE DEPARTMENT
# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_department(
#     name: str,
#     description: str | None = None,
#     db: Session = Depends(get_db),
# ):
#     department = Department(
#         name=name,
#         description=description,
#     )
#     db.add(department)
#     db.commit()
#     db.refresh(department)
#     return department

# #GET ALL DEPARTMENTS
# @router.get("/")
# def get_departments(db: Session = Depends(get_db)):
#     return db.query(Department).filter(Department.is_active == True).all()

# #GET SINGLE DEPARTMENT
# @router.get("/{department_id}")
# def get_department(department_id: UUID, db: Session = Depends(get_db)):
#     department = db.query(Department).filter(
#         Department.id == department_id,
#         Department.is_active == True
#     ).first()

#     if not department:
#         raise HTTPException(status_code=404, detail="Department not found")

#     return department

# #UPDATE DEPARTMENT
# @router.put("/{department_id}")
# def update_department(
#     department_id: UUID,
#     name: str | None = None,
#     description: str | None = None,
#     db: Session = Depends(get_db),
# ):
#     department = db.query(Department).filter(Department.id == department_id).first()

#     if not department:
#         raise HTTPException(status_code=404, detail="Department not found")

#     if name:
#         department.name = name
#     if description:
#         department.description = description

#     db.commit()
#     db.refresh(department)
#     return department

# #DELETE (SOFT DELETE) DEPARTMENT
# @router.delete("/{department_id}")
# def delete_department(department_id: UUID, db: Session = Depends(get_db)):
#     department = db.query(Department).filter(Department.id == department_id).first()

#     if not department:
#         raise HTTPException(status_code=404, detail="Department not found")

#     department.is_active = False
#     db.commit()

#     return {"message": "Department deactivated"}

# #ASSIGN USER TO DEPARTMENT
# @router.post("/{department_id}/assign-user")
# def assign_user_to_department(
#     department_id: UUID,
#     user_id: UUID,
#     db: Session = Depends(get_db),
# ):
#     # check department
#     department = db.query(Department).filter(
#         Department.id == department_id,
#         Department.is_active == True
#     ).first()

#     if not department:
#         raise HTTPException(status_code=404, detail="Department not found")

#     # check user
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # get default role (CONTRIBUTOR)
#     role = db.query(DepartmentRole).filter(
#         DepartmentRole.is_default == True,
#         DepartmentRole.is_active == True
#     ).first()

#     if not role:
#         raise HTTPException(status_code=500, detail="Default department role not configured")

#     # check existing assignment
#     existing = db.query(UserDepartment).filter(
#         UserDepartment.user_id == user_id,
#         UserDepartment.department_id == department_id
#     ).first()

#     if existing:
#         raise HTTPException(status_code=400, detail="User already assigned")

#     assignment = UserDepartment(
#         user_id=user_id,
#         department_id=department_id,
#         department_role_id=role.id
#     )

#     db.add(assignment)
#     db.commit()
#     db.refresh(assignment)

#     return {
#         "message": "User assigned to department",
#         "department_id": department_id,
#         "user_id": user_id,
#         "role": role.code
#     }


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.dependencies import require_department_admin

from app.models.department import Department
from app.models.user_department import UserDepartment
from app.models.department_role import DepartmentRole
from app.models.user import User

router = APIRouter(prefix="/departments", tags=["Departments"])


# ------------------------------------------------
# CREATE DEPARTMENT (DEPARTMENT_ADMIN ONLY)
# ------------------------------------------------
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


# ------------------------------------------------
# GET ALL DEPARTMENTS (READ ONLY)
# ------------------------------------------------
@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).filter(Department.is_active == True).all()


# ------------------------------------------------
# GET SINGLE DEPARTMENT (READ ONLY)
# ------------------------------------------------
@router.get("/{department_id}")
def get_department(department_id: UUID, db: Session = Depends(get_db)):
    department = db.query(Department).filter(
        Department.id == department_id,
        Department.is_active == True
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return department


# ------------------------------------------------
# UPDATE DEPARTMENT (DEPARTMENT_ADMIN ONLY)
# ------------------------------------------------
@router.put("/{department_id}")
def update_department(
    department_id: UUID,
    name: str | None = None,
    description: str | None = None,
    current_user: User = Depends(require_department_admin),
    db: Session = Depends(get_db),
):
    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    if name is not None:
        department.name = name
    if description is not None:
        department.description = description

    db.commit()
    db.refresh(department)
    return department


# ------------------------------------------------
# DELETE DEPARTMENT (SOFT DELETE) – DEPARTMENT_ADMIN ONLY
# ------------------------------------------------
@router.delete("/{department_id}")
def delete_department(
    department_id: UUID,
    current_user: User = Depends(require_department_admin),
    db: Session = Depends(get_db),
):
    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    department.is_active = False
    db.commit()

    return {"message": "Department deactivated successfully"}


# ------------------------------------------------
# ASSIGN USER TO DEPARTMENT (DEPARTMENT_ADMIN ONLY)
# ------------------------------------------------
@router.post("/{department_id}/assign-user")
def assign_user_to_department(
    department_id: UUID,
    user_id: UUID,
    current_user: User = Depends(require_department_admin),
    db: Session = Depends(get_db),
):
    # Check department
    department = db.query(Department).filter(
        Department.id == department_id,
        Department.is_active == True
    ).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    # Check user
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get default department role (CONTRIBUTOR)
    role = db.query(DepartmentRole).filter(
        DepartmentRole.is_default == True,
        DepartmentRole.is_active == True
    ).first()

    if not role:
        raise HTTPException(
            status_code=500,
            detail="Default department role not configured"
        )

    # Check existing assignment
    existing = db.query(UserDepartment).filter(
        UserDepartment.user_id == user_id,
        UserDepartment.department_id == department_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already assigned to this department"
        )

    assignment = UserDepartment(
        user_id=user_id,
        department_id=department_id,
        department_role_id=role.id,
        is_active=True
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return {
        "message": "User assigned to department successfully",
        "department_id": department_id,
        "user_id": user_id,
        "role": role.code
    }
