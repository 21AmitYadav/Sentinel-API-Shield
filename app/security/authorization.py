from fastapi import Depends, HTTPException
from app.models.api_key import ApiKey
from app.repositories.api_key_permission_repository import ApiKeyPermissionRepository
from app.services.api_key_permission_service import ApiKeyPermissionService
from app.security.api_key_handler import get_current_api_key
from app.config.database import get_db
from sqlalchemy.orm import Session


def require_permission(permission_name: str):

    def permission_checker(api_key: ApiKey = Depends(get_current_api_key),db: Session = Depends(get_db)) -> ApiKey:

        repository = ApiKeyPermissionRepository(db)

        service = ApiKeyPermissionService(repository)

        has_permission = service.check_permission_for_api_key(
            api_key.id,
            permission_name
        )

        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail=f"Permission required: {permission_name}"
            )

        return api_key

    return permission_checker