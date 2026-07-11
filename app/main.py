from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.config.database import Base, engine
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sentinel API Shield",
    version="1.0.0",
)


app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the AI agent API!"}

