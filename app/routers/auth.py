from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.api_key_auth import get_api_key_service
from app.dependencies.auth import get_current_user
from app.models.api_key import ApiKey
from app.models.user import User
from app.repositories.api_key_repository import ApiKeyRepository
from app.services.api_key_service import ApiKeyService
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth import RegisterRequest, RegisterResponse
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.api_key import ApiKeyCreateRequest, ApiKeyCreateResponse, ApiKeyListResponse
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

@router.post("/api-keys",response_model=ApiKeyCreateResponse,status_code=status.HTTP_201_CREATED)
def create_api_key(api_key_request: ApiKeyCreateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ApiKeyCreateResponse:
    api_key_repository = ApiKeyRepository(db)
    api_key_service = ApiKeyService(api_key_repository)
    return api_key_service.create_api_key(current_user.id, api_key_request)

@router.get("/api-keys",response_model=ApiKeyListResponse,status_code=status.HTTP_200_OK)
def list_api_keys(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> ApiKeyListResponse:
    api_key_repository = ApiKeyRepository(db)
    api_key_service = ApiKeyService(api_key_repository)
    return api_key_service.list_api_keys(current_user.id)

@router.delete("/api-keys/{api_key_id}",status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(api_key_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    api_key_repository = ApiKeyRepository(db)
    api_key_service = ApiKeyService(api_key_repository)
    api_key_service.revoke_api_key(api_key_id, current_user.id)

@router.get("/test/protected", status_code=status.HTTP_200_OK)
def test_protected_route(api_key: ApiKey = Depends(get_api_key_service)):
    return {
        "message": "You are authenticated",
        "user_id": api_key.user_id
    }


     