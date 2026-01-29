# from fastapi import Depends, HTTPException,status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



# from sqlalchemy.orm import Session
# from jose import jwt

# from app.core.database import get_db
# from app.core.security import SECRET_KEY, ALGORITHM
# from app.models.user import User
# from app.models.user_session import UserSession
# from app.models.user_role import UserRole
# from app.models.user_user_role import UserUserRole
# from app.utils.token import hash_token

# security = HTTPBearer()

# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     db: Session = Depends(get_db)
# ):
#     try:
#         token = credentials.credentials
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#         if not user_id:
#             raise Exception()
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     session = db.query(UserSession).filter(
#         UserSession.token_hash == hash_token(token),
#         UserSession.is_active == True
#     ).first()

#     if not session:
#         raise HTTPException(status_code=401, detail="Session expired")

#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user



# def get_current_super_admin(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """
#     Allow only SUPER_ADMIN or USER_ADMIN
#     """

#     allowed_roles = ("SUPER_ADMIN", "USER_ADMIN")

#     has_access = (
#         db.query(UserRole)
#         .join(UserUserRole, UserUserRole.user_role_id == UserRole.id)
#         .filter(
#             UserUserRole.user_id == current_user.id,
#             UserRole.code.in_(allowed_roles),   # ✅ FIX
#             UserRole.is_active == True
#         )
#         .first()
#     )

#     if not has_access:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only super admin and user admin can perform this action"
#         )

#     return current_user


# #only department admin can create department and assign roles to users
# def require_department_admin(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """
#     Allow only DEPARTMENT_ADMIN
#     """

#     has_access = (
#         db.query(UserRole)
#         .join(UserUserRole, UserUserRole.user_role_id == UserRole.id)
#         .filter(
#             UserUserRole.user_id == current_user.id,
#             UserRole.code == "DEPARTMENT_ADMIN",
#             UserRole.is_active == True
#         )
#         .first()
#     )

#     if not has_access:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only department admin can perform this action"
#         )

#     return current_user


# #For assigning owner to the user deparment role
# from uuid import UUID
# from app.models.department_role import DepartmentRole     # ✅ REQUIRED
# from app.models.user_department import UserDepartment 
# def require_department_admin_or_owner(
#     department_id: UUID,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     """
#     Allow DEPARTMENT_ADMIN OR OWNER of the department
#     """

#     # 1️⃣ Check system-level DEPARTMENT_ADMIN
#     is_department_admin = (
#         db.query(UserRole)
#         .join(UserUserRole, UserUserRole.user_role_id == UserRole.id)
#         .filter(
#             UserUserRole.user_id == current_user.id,
#             UserRole.code == "DEPARTMENT_ADMIN",
#             UserRole.is_active == True
#         )
#         .first()
#     )

#     if is_department_admin:
#         return current_user

#     # 2️⃣ Check department-level OWNER
#     owner_role = db.query(DepartmentRole).filter(
#         DepartmentRole.code == "OWNER",
#         DepartmentRole.is_active == True
#     ).first()

#     if not owner_role:
#         raise HTTPException(
#             status_code=500,
#             detail="Owner role not configured"
#         )

#     is_owner = (
#         db.query(UserDepartment)
#         .filter(
#             UserDepartment.user_id == current_user.id,
#             UserDepartment.department_id == department_id,
#             UserDepartment.department_role_id == owner_role.id,
#             UserDepartment.is_active == True
#         )
#         .first()
#     )

#     if not is_owner:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only Department Admin or Department Owner can perform this action"
#         )

#     return current_user

#2nd one 
# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from sqlalchemy.orm import Session
# from jose import jwt
# from uuid import UUID

# from app.core.database import get_db
# from app.core.security import SECRET_KEY, ALGORITHM
# from app.utils.token import hash_token

# from app.models.user import User
# from app.models.user_session import UserSession
# from app.models.user_role import UserRole
# from app.models.user_user_role import UserUserRole
# from app.models.department_role import DepartmentRole
# from app.models.user_department import UserDepartment

# security = HTTPBearer()


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     db: Session = Depends(get_db),
# ):
#     token = credentials.credentials
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     session = db.query(UserSession).filter(
#         UserSession.token_hash == hash_token(token),
#         UserSession.is_active == True
#     ).first()

#     if not session:
#         raise HTTPException(status_code=401, detail="Session expired")

#     user = db.query(User).filter(
#         User.id == user_id,
#         User.is_active == True
#     ).first()

#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user

# # ------------------------------------------------
# # SUPER ADMIN OR USER ADMIN
# # ------------------------------------------------
# def get_current_super_admin(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     allowed_roles = ("SUPER_ADMIN", "USER_ADMIN")

#     has_access = (
#         db.query(UserRole)
#         .join(UserUserRole)
#         .filter(
#             UserUserRole.user_id == current_user.id,
#             UserRole.code.in_(allowed_roles),
#             UserRole.is_active == True
#         )
#         .first()
#     )

#     if not has_access:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only Super Admin or User Admin can perform this action"
#         )

#     return current_user


# # SYSTEM ROLE
# def require_department_admin(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     access = db.query(UserRole).join(UserUserRole).filter(
#         UserUserRole.user_id == current_user.id,
#         UserRole.code == "DEPARTMENT_ADMIN",
#         UserRole.is_active == True
#     ).first()

#     if not access:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only Department Admin can perform this action"
#         )

#     return current_user


# # DEPARTMENT OWNER ONLY
# def require_department_owner(
#     department_id: UUID,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     owner_role = db.query(DepartmentRole).filter(
#         DepartmentRole.code == "OWNER",
#         DepartmentRole.is_active == True
#     ).first()

#     is_owner = db.query(UserDepartment).filter(
#         UserDepartment.department_id == department_id,
#         UserDepartment.user_id == current_user.id,
#         UserDepartment.department_role_id == owner_role.id,
#         UserDepartment.is_active == True
#     ).first()

#     if not is_owner:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Only Department Owner can perform this action"
#         )

#     return current_user

#modified code
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt
from uuid import UUID

from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.utils.token import hash_token

from app.models.user import User
from app.models.user_session import UserSession
from app.models.user_role import UserRole
from app.models.user_user_role import UserUserRole
from app.models.department_role import DepartmentRole
from app.models.user_department import UserDepartment

security = HTTPBearer()

# ------------------------------------------------
# CURRENT USER
# ------------------------------------------------
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    session = db.query(UserSession).filter(
        UserSession.token_hash == hash_token(token),
        UserSession.is_active == True
    ).first()

    if not session:
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.query(User).filter(
        User.id == user_id,
        User.is_active == True
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# ------------------------------------------------
# SUPER ADMIN OR USER ADMIN
# ------------------------------------------------
def get_current_super_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    allowed_roles = ("SUPER_ADMIN", "USER_ADMIN")

    has_access = (
        db.query(UserRole)
        .join(UserUserRole)
        .filter(
            UserUserRole.user_id == current_user.id,
            UserRole.code.in_(allowed_roles),
            UserRole.is_active == True
        )
        .first()
    )

    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Super Admin or User Admin can perform this action"
        )

    return current_user


# ------------------------------------------------
# SYSTEM ROLE: DEPARTMENT ADMIN
# ------------------------------------------------
def require_department_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    role = db.query(UserRole).join(UserUserRole).filter(
        UserUserRole.user_id == current_user.id,
        UserRole.code == "DEPARTMENT_ADMIN",
        UserRole.is_active == True
    ).first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Department Admin can perform this action"
        )

    return current_user


# ------------------------------------------------
# DEPARTMENT ROLE: OWNER
# ------------------------------------------------
def require_department_owner(
    department_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    owner_role = db.query(DepartmentRole).filter(
        DepartmentRole.code == "OWNER",
        DepartmentRole.is_active == True
    ).first()

    if not owner_role:
        raise HTTPException(status_code=500, detail="Owner role not configured")

    is_owner = db.query(UserDepartment).filter(
        UserDepartment.department_id == department_id,
        UserDepartment.user_id == current_user.id,
        UserDepartment.department_role_id == owner_role.id,
        UserDepartment.is_active == True
    ).first()

    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Department Owner can perform this action"
        )

    return current_user
