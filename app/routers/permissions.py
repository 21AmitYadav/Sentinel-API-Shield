
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.config.database import get_db
from app.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository
from app.services.permission_service import PermissionService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_permission(
    permission_request: dict,
    db: Session = Depends(get_db)
):
    repository = PermissionRepository(db)
    service = PermissionService(repository)

    permission = Permission(
        name=permission_request["name"],
        description=permission_request["description"]
    )

    return service.create_permission(permission)


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_permissions(
    db: Session = Depends(get_db)
):
    repository = PermissionRepository(db)
    service = PermissionService(repository)

    return service.get_all_permissions()
