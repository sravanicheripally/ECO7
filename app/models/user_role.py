from sqlalchemy import Column, String, Boolean, Text, TIMESTAMP, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (
        Index('idx_user_role_code', 'code'),  # Index for faster lookups
        CheckConstraint(
            "code ~ '^[A-Z0-9_]+$'",  # PostgreSQL regex: only uppercase letters, numbers, underscores
            name='ck_user_role_code_format'
        ),
        {"schema": "auth"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False)  # Case-sensitive unique constraint
    description = Column(Text)

    is_predefined = Column(Boolean, default=False)
    is_system_role = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
