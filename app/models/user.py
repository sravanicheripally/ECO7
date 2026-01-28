from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    username = Column(String(255), nullable=False)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    mobile = Column(String, unique=True, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    deleted_at = Column(TIMESTAMP(timezone=False), nullable=True)
 
 

