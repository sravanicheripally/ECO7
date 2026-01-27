from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM,
)
from app.core.dependencies import get_current_user
from app.schemas.auth import LoginRequest
from app.schemas.user import UserMeResponse
from app.models.user import User
from app.models.user_session import UserSession
from app.utils.token import hash_token
from app.models.user_role import UserRole
from app.models.user_user_role import UserUserRole


# ----------------------------
# Router & Security
# ----------------------------
router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()

# ----------------------------
# LOGIN
# ----------------------------
@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    session = UserSession(
        user_id=user.id,
        token_hash=hash_token(access_token),
        refresh_token_hash=hash_token(refresh_token),
        is_active=True,
        refresh_expires_at=datetime.utcnow() + timedelta(days=7),
        created_at=datetime.utcnow(),
    )

    db.add(session)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

# ----------------------------
# LOGOUT
# ----------------------------
@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    session = db.query(UserSession).filter(
        UserSession.user_id == current_user.id,
        UserSession.token_hash == hash_token(token),
        UserSession.is_active == True,
    ).first()

    if session:
        session.is_active = False
        db.commit()

    return {"message": "Logged out successfully"}

# ----------------------------
# REFRESH TOKEN
# ----------------------------
@router.post("/refresh")
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    refresh_token = credentials.credentials

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    session = db.query(UserSession).filter(
        UserSession.refresh_token_hash == hash_token(refresh_token),
        UserSession.is_active == True,
    ).first()

    if not session:
        raise HTTPException(status_code=401, detail="Session expired")

    new_access_token = create_access_token({"sub": str(user_id)})
    session.token_hash = hash_token(new_access_token)
    db.commit()

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }

@router.get("/my_profile", response_model=UserMeResponse)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roles = (
        db.query(UserRole)
        .join(UserUserRole, UserRole.id == UserUserRole.user_role_id)
        .filter(UserUserRole.user_id == current_user.id)
        .all()
    )

    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "username": current_user.username,
        "is_active": current_user.is_active,
        "roles": roles
    }
