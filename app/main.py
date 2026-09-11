from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.config.database import Base, engine
from app.models.user import User
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

@app.get("/")
def root():
    return {"message": "Welcome to the AI agent API!"}

