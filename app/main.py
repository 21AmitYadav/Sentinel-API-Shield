from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.config.database import Base, engine
from app.models.user import User
from app.models.user import User
from app.models.api_key import ApiKey
from app.models.permission import Permission
from app.models.api_key_permission import ApiKeyPermission
from app.routers.api_key_permissions import router as api_key_permission_router
from app.models.request_log import RequestLog
from app.routers.permissions import router as permission_router
import os

Base.metadata.create_all(bind=engine)

from app.middleware.logging_middleware import logging_middleware
from app.middleware.rate_limit_middleware import rate_limit_middleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sentinel API Shield",
    version="1.0.0",
)
app.middleware("http")(rate_limit_middleware)

app.middleware("http")(logging_middleware)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

app.include_router(
    permission_router,
    prefix="/api/v1/permissions",
    tags=["Permissions"]
)

app.include_router(
    api_key_permission_router,
    prefix="/api/v1/api-keys",
    tags=["API Key Permissions"]
)

@app.get("/")
def root():
    return {"message": "Welcome to the AI agent API!"}

