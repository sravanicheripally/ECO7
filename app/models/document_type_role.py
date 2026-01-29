from sqlalchemy import (
    Column,
    String,
    Boolean,
    Text,
    Integer,
    TIMESTAMP,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class DocumentTypeRole(Base):
    __tablename__ = "document_type_roles"
    __table_args__ = (
        Index("idx_doctype_roles_code", "code"),
        {"schema": "dms"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Role Information
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)

    # Role Level
    role_level = Column(Integer, default=0)

    # Role Type / Status
    is_predefined = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
