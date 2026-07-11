from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, RegisterResponse
from app.config.database import get_db


router = APIRouter()


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(register_request: RegisterRequest, db:Session = Depends(get_db))->RegisterResponse:
    repository = UserRepository(db)
    service = AuthService(repository)
    try:
        return service.register_user(register_request)
    except ValueError as e:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
           detail=str(e)
        )