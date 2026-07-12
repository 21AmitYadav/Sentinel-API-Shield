from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.security.jwt_handler import decode_access_token

outh2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token:str=Depends(outh2_scheme),db:Session = Depends(get_db)) -> User:
    user_id = decode_access_token(token)


    
    user_repository = UserRepository(db)
    user = user_repository.find_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user











