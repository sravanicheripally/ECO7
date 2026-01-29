import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
    Index
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from app.core.database import Base


class DocumentType(Base):
    __tablename__ = "document_types"
    __table_args__ = (
        Index("idx_doc_types_code", "code"),
        Index(
            "idx_doc_types_active",
            "is_active",
            postgresql_where=(Column("is_active") == True)
        ),
        {"schema": "dms"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    icon = Column(String(100))

    allowed_extensions = Column(ARRAY(Text))
    max_file_size_mb = Column(Integer, default=100)

    requires_approval = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id"),
        nullable=True
    )
    updated_by = Column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id"),
        nullable=True
    )
