from sqlalchemy import Column, String, Boolean, Text, TIMESTAMP, Index, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class UserPermission(Base):
    __tablename__ = "user_permissions"
    __table_args__ = (
        Index('idx_user_permission_code', 'code'),  # Index for faster lookups
        Index('idx_user_permission_category', 'category'),  # Index for filtering
        CheckConstraint(
            "code ~ '^[A-Z0-9_]+$'",  # PostgreSQL regex: only uppercase letters, numbers, underscores
            name='ck_user_permission_code_format'
        ),
        {"schema": "auth"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(100), unique=True, nullable=False)  # Case-sensitive unique constraint
    description = Column(Text)
    
    # Categorization
    category = Column(String(50), default="general")
    module = Column(String(50))  # 'users', 'departments', 'documents', 'gis', 'etl'
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
