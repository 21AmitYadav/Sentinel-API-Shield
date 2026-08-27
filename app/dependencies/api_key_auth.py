from fastapi import Depends, HTTPException
from fastapi import Request
from app.config.database import get_db
from app.repositories.api_key_repository import ApiKeyRepository
from app.services.api_key_service import ApiKeyService
from app.models.api_key import ApiKey
from app.utils.api_key import hash_api_key

def get_api_key_service(request:Request,db=Depends(get_db)) -> ApiKey:
    api_key = request.headers.get("Authorization")
    if api_key is None or not api_key.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="API key is missing")
    api_key = hash_api_key(api_key.replace("Bearer ", ""))
    api_key_repository = ApiKeyRepository(db)
    api_key_service =  ApiKeyService(api_key_repository)
    data = api_key_service.get_api_key_by_hash(api_key)
    return data






