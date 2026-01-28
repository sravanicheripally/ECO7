from fastapi import Depends, HTTPException
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
    """Verify that the current user has the SUPER_ADMIN role"""
    super_admin_role = db.query(UserRole).filter(
        UserRole.code == " Super Admin",
        UserRole.is_active == True
    ).first()

    if not super_admin_role:
        raise HTTPException(status_code=500, detail="Super admin role not found")

    has_super_admin = db.query(UserUserRole).filter(
        UserUserRole.user_id == current_user.id,
        UserUserRole.user_role_id == super_admin_role.id
    ).first()

    if not has_super_admin:
        raise HTTPException(
            status_code=403,
            detail="Only super admin can perform this action"
        )

    return current_user
