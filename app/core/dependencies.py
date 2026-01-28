from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



from sqlalchemy.orm import Session
from jose import jwt

from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user import User
from app.models.user_session import UserSession
from app.models.user_role import UserRole
from app.models.user_user_role import UserUserRole
from app.utils.token import hash_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise Exception()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    session = db.query(UserSession).filter(
        UserSession.token_hash == hash_token(token),
        UserSession.is_active == True
    ).first()

    if not session:
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user



def get_current_super_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Allow only SUPER_ADMIN or USER_ADMIN
    """

    allowed_roles = ("SUPER_ADMIN", "USER_ADMIN")

    has_access = (
        db.query(UserRole)
        .join(UserUserRole, UserUserRole.user_role_id == UserRole.id)
        .filter(
            UserUserRole.user_id == current_user.id,
            UserRole.code.in_(allowed_roles),   # ✅ FIX
            UserRole.is_active == True
        )
        .first()
    )

    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admin and user admin can perform this action"
        )

    return current_user


#only department admin can create department and assign roles to users
def require_department_admin(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Allow only DEPARTMENT_ADMIN
    """

    has_access = (
        db.query(UserRole)
        .join(UserUserRole, UserUserRole.user_role_id == UserRole.id)
        .filter(
            UserUserRole.user_id == current_user.id,
            UserRole.code == "DEPARTMENT_ADMIN",
            UserRole.is_active == True
        )
        .first()
    )

    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only department admin can perform this action"
        )

    return current_user

