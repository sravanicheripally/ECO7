from sqlalchemy import Column, Boolean, TIMESTAMP, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class UserSession(Base):
    __tablename__ = "user_sessions"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Access token (hashed)
    token_hash = Column(String(255), nullable=False)

    # ✅ ADD THESE TWO LINES (THIS WAS MISSING)
    refresh_token_hash = Column(String(255), nullable=True)
    refresh_expires_at = Column(TIMESTAMP, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP)
    last_activity_at = Column(TIMESTAMP)
