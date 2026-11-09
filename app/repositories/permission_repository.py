
from sqlalchemy.orm import Session

from app.models.permission import Permission


class PermissionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_permission(self, permission: Permission) -> Permission:
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)

        return permission

    def get_permission_by_name(self, permission_name: str) -> Permission | None:
        return (
            self.db.query(Permission)
            .filter(Permission.name == permission_name)
            .first()
        )

    def get_all_permissions(self) -> list[Permission]:
        return self.db.query(Permission).all()
