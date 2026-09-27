from app.models.api_key_permission import ApiKeyPermission
from app.repositories.api_key_permission_repository import ApiKeyPermissionRepository


class ApiKeyPermissionService:
    def __init__(self, api_key_permission_repository: ApiKeyPermissionRepository):
        self.api_key_permission_repository = api_key_permission_repository

    def give_permission_to_api_key(self, api_key_id: int, permission_id: int) -> ApiKeyPermission:
        return self.api_key_permission_repository.give_permission_to_api_key(api_key_id, permission_id)

    def check_permission_for_api_key(self, api_key_id: int, permission_name: str) -> bool:
        return self.api_key_permission_repository.check_permission_for_api_key(api_key_id, permission_name)

    def get_permissions_for_api_key(self, api_key_id: int) -> list:
        return self.api_key_permission_repository.get_permissions_for_api_key(api_key_id)

    def remove_permission_from_api_key(self, api_key_id: int, permission_id: int) -> None:
        self.api_key_permission_repository.remove_permission_from_api_key(api_key_id, permission_id)



