from sqlalchemy import Column, String, Boolean, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class UserPermission(Base):
    __tablename__ = "user_permissions"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    
    # Categorization
    category = Column(String(50), default="general")
    module = Column(String(50))  # 'users', 'departments', 'documents', 'gis', 'etl'
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
