from fastapi import HTTPException
from app.models.api_key import ApiKey
from app.repositories.api_key_repository import ApiKeyRepository
from app.schemas.api_key import ApiKeyCreateRequest, ApiKeyCreateResponse, ApiKeyResponse, ApiKeyListResponse
from app.utils.api_key import generate_api_key, hash_api_key

class ApiKeyService:

    def __init__(self, api_key_repository: ApiKeyRepository):
        self.api_key_repository = api_key_repository

    def create_api_key(self, user_id: int, api_key_request: ApiKeyCreateRequest) -> ApiKeyCreateResponse:
        # Generate a new API key and its hash it
        api_key = generate_api_key()
        key_hash = hash_api_key(api_key)
        api_key_model = ApiKey(
            user_id=user_id,
            name=api_key_request.name,
            key_hash=key_hash,
            active=True,
        )
        api_key_model = self.api_key_repository.create_api_key(api_key_model)
        return ApiKeyCreateResponse(
        id=api_key_model.id,
        name=api_key_model.name,
        api_key=api_key,
        created_at=api_key_model.created_at
)
    
    def list_api_keys(self, user_id: int) -> ApiKeyListResponse:
        api_keys = self.api_key_repository.find_api_keys_by_user_id(user_id)
        return ApiKeyListResponse(api_keys=[ApiKeyResponse.model_validate(api_key) for api_key in api_keys], total=len(api_keys))
    
    def revoke_api_key(self, api_key_id: int,user_id: int) -> None:
        api_key = self.api_key_repository.find_by_id(api_key_id)
        if not api_key:
            raise HTTPException(status_code=404, detail="API key not found")    
        if api_key.user_id != user_id:
            raise HTTPException(status_code=403, detail="You do not have permission to revoke this API key")

        self.api_key_repository.deactivate_api_key(api_key_id)



