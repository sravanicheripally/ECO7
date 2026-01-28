from sqlalchemy import Column, ForeignKey, TIMESTAMP, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class UserRolePermission(Base):
    __tablename__ = "user_role_permissions"
    __table_args__ = (
        UniqueConstraint("user_role_id", "permission_id", name="unique_role_permission"),
        {"schema": "auth"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_role_id = Column(UUID(as_uuid=True), ForeignKey("auth.user_roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("auth.user_permissions.id", ondelete="CASCADE"), nullable=False)
    
    # Timestamps
    created_at = Column(TIMESTAMP)
