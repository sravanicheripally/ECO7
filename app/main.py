from fastapi import FastAPI
from app.api import auth
from app.api.admin import admin_roles
from app.api.users import users
from app.core.database import Base, engine
from app.api.departments import router as department_router
from app.api.document_type_admin.document_type_role_admin import router as document_type_role_router
from app.api.document_type_admin.document_type_admin import router as  document_type_router


app = FastAPI(title="ECO7 GEO-DMS")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin_roles.router)
app.include_router(department_router)


app.include_router(document_type_router)
app.include_router(document_type_role_router)

# app.include_router(admin_permissions.router)
Base.metadata.create_all(bind=engine)


