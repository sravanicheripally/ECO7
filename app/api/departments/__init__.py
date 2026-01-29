from .departments import router as departments_router
from .department_roles import router as department_roles_router

__all__ = [
    "departments_router",
    "department_roles_router",
]
