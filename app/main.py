from fastapi import FastAPI
from app.api import auth
from app.api.admin import admin_roles
from app.api.users import users
from app.core.database import Base, engine
from app.api.departments import departments_router, department_roles_router


app = FastAPI(title="ECO7 GEO-DMS")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin_roles.router)
app.include_router(departments_router)
app.include_router(department_roles_router)

# app.include_router(admin_permissions.router)
Base.metadata.create_all(bind=engine)


