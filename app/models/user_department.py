import uuid
from sqlalchemy import Column, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base


class UserDepartment(Base):
    __tablename__ = "user_departments"
    __table_args__ = {"schema": "auth"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("auth.departments.id"), nullable=False)
    department_role_id = Column(UUID(as_uuid=True), ForeignKey("auth.department_roles.id"), nullable=False)

    is_active = Column(Boolean, default=True)

    assigned_at = Column(DateTime, server_default=func.now())
    assigned_by = Column(UUID(as_uuid=True))
