
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.config.database import get_db
from app.models.permission import Permission
from app.repositories.api_key_repository import ApiKeyRepository
from app.repositories.api_key_permission_repository import ApiKeyPermissionRepository
from app.services.api_key_permission_service import ApiKeyPermissionService


router = APIRouter()


# Assign permission to API key
@router.post("/{api_key_id}/permissions/{permission_id}", status_code=status.HTTP_201_CREATED)
def assign_permission_to_api_key( api_key_id: int, permission_id: int,db: Session = Depends(get_db)):
    api_key_repository = ApiKeyRepository(db)
    api_key = api_key_repository.find_by_id(api_key_id)

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )

    permission = db.query(Permission).filter(Permission.id == permission_id).first()

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    repository = ApiKeyPermissionRepository(db)
    service = ApiKeyPermissionService(repository)

    if service.check_permission_for_api_key(api_key_id, permission.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Permission already assigned to this API key"
        )

    service.give_permission_to_api_key(api_key_id, permission_id)

    return {
        "message": "Permission assigned successfully",
        "api_key_id": api_key_id,
        "permission_id": permission_id,
        "permission_name": permission.name
    }


# Get permissions assigned to API key
@router.get("/{api_key_id}/permissions",status_code=status.HTTP_200_OK)
def get_api_key_permissions(api_key_id: int,db: Session = Depends(get_db)):
    api_key_repository = ApiKeyRepository(db)
    api_key = api_key_repository.find_by_id(api_key_id)

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )

    repository = ApiKeyPermissionRepository(db)
    service = ApiKeyPermissionService(repository)

    return service.get_permissions_for_api_key(api_key_id)


# Remove permission from API key
@router.delete("/{api_key_id}/permissions/{permission_id}",status_code=status.HTTP_200_OK)
def remove_permission_from_api_key(api_key_id: int,permission_id: int,db: Session = Depends(get_db)):
    api_key_repository = ApiKeyRepository(db)
    api_key = api_key_repository.find_by_id(api_key_id)

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )

    permission = db.query(Permission).filter(Permission.id == permission_id).first()

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found"
        )

    repository = ApiKeyPermissionRepository(db)
    service = ApiKeyPermissionService(repository)

    if not service.check_permission_for_api_key(api_key_id, permission.name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission assignment not found"
        )

    service.remove_permission_from_api_key(api_key_id, permission_id)

    return {
        "message": "Permission removed successfully",
        "api_key_id": api_key_id,
        "permission_id": permission_id
    }
