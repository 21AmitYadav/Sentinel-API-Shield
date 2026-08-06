from datetime import datetime, timedelta, timezone
import jwt
from app.config.config import settings

def create_access_token(userId : int)->str:

    current_time = datetime.now(timezone.utc)

    expire = current_time + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(userId),
        "exp": expire,
        "iat": current_time
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.jwt_algorithm)

    return token


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.jwt_algorithm])
    user_id = payload.get("sub")
    if user_id is None:
        raise ValueError("Token does not contain user ID")   
    return int(user_id)