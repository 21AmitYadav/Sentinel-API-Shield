from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.security.password import hash_password
from app.security.password import verify_password
from app.schemas.user import RegisterRequest, RegisterResponse
from app.schemas.auth import LoginRequest, LoginResponse
from app.security.jwt_handler import create_access_token


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    def register_user(self,register_request:RegisterRequest) -> RegisterResponse:
        existing_user = self.user_repository.find_user_by_email(register_request.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        hashed_password = hash_password(register_request.password)
        user = User(password_hash=hashed_password, full_name=register_request.full_name, email=register_request.email, role="user", status="active")   
        user = self.user_repository.create_user(user)
        return RegisterResponse.model_validate(user)
    
    def login_user(self, login_request: LoginRequest) -> LoginResponse:
        user = self.user_repository.find_user_by_email(login_request.email)
        if not user:
            raise ValueError("Invalid email or password")
        if not verify_password(login_request.password, user.password_hash):
            raise ValueError("Invalid email or password")
        # Here you would generate a JWT token or similar for the user
        access_token = create_access_token(user.id)
        return LoginResponse(access_token=access_token)