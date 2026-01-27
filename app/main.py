from fastapi import FastAPI
from app.api import auth, users, admin_roles

app = FastAPI(title="ECO7 GEO-DMS")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin_roles.router)
# app.include_router(admin_permissions.router)


