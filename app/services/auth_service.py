from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.security.password import hash_password
from app.schemas.user import RegisterRequest, RegisterResponse


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