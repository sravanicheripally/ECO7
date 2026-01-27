from sqlalchemy import Column, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class UserUserRole(Base):
    __tablename__ = "user_user_roles"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    user_role_id = Column(UUID(as_uuid=True), ForeignKey("auth.user_roles.id"), nullable=False)
    created_at = Column(TIMESTAMP)
