from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.api_key import ApiKey
from app.repositories.api_key_repository import ApiKeyRepository
from app.services.api_key_service import ApiKeyService
from app.utils.api_key import hash_api_key


def get_current_api_key(request: Request,db: Session = Depends(get_db)) -> ApiKey:
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="API key is missing"
        )

    api_key = authorization.replace("Bearer ", "", 1)

    key_hash = hash_api_key(api_key)

    repository = ApiKeyRepository(db)
    service = ApiKeyService(repository)

    return service.get_api_key_by_hash(key_hash)