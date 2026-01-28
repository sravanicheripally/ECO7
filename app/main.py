from fastapi import FastAPI
from app.api import auth
from app.api.admin import admin_roles
from app.api.users import users

app = FastAPI(title="ECO7 GEO-DMS")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin_roles.router)
# app.include_router(admin_permissions.router)


