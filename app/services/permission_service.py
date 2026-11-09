from fastapi import HTTPException, status

from app.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository


class PermissionService:

    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

    def create_permission(self, permission: Permission) -> Permission:

        existing_permission = self.permission_repository.get_permission_by_name(
            permission.name
        )

        if existing_permission:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Permission '{permission.name}' already exists"
            )

        return self.permission_repository.create_permission(permission)

    def get_all_permissions(self) -> list[Permission]:
        return self.permission_repository.get_all_permissions()

    def get_permission_by_name(self, permission_name: str) -> Permission:

        permission = self.permission_repository.get_permission_by_name(
            permission_name
        )

        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission '{permission_name}' not found"
            )

        return permission