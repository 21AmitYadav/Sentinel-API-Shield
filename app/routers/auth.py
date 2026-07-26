from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, RegisterResponse
from app.schemas.auth import LoginRequest, LoginResponse
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
    
@router.post("/login",response_model=LoginResponse,status_code=status.HTTP_200_OK)
def login(login_request:LoginRequest,db:Session = Depends(get_db))->LoginResponse:
    repository = UserRepository(db)
    service = AuthService(repository)
    try:
        return service.login_user(login_request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
@router.get("/me",response_model=RegisterResponse,status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)) -> RegisterResponse:

    return current_user