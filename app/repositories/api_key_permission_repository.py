from app.models.api_key_permission import ApiKeyPermission
from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.models.api_key import ApiKey

def give_permission_to_api_key(db: Session, api_key_id: int, permission_id: int) -> ApiKeyPermission:
    api_key_permission = ApiKeyPermission(api_key_id=api_key_id, permission_id=permission_id)
    db.add(api_key_permission)
    db.commit()
    db.refresh(api_key_permission)
    return api_key_permission

def check_permission_for_api_key(db: Session, api_key_id: int, permission_name: str) -> bool:
    permission = db.query(Permission).filter(Permission.name == permission_name).first()
    if not permission:
        return False
    api_key_permission = db.query(ApiKeyPermission).filter(
        ApiKeyPermission.api_key_id == api_key_id,
        ApiKeyPermission.permission_id == permission.id
    ).first()
    return api_key_permission is not None

def get_permissions_for_api_key(db: Session, api_key_id: int) -> list[Permission]:
    permissions = (
        db.query(Permission)
        .join(ApiKeyPermission, Permission.id == ApiKeyPermission.permission_id)
        .filter(ApiKeyPermission.api_key_id == api_key_id)
        .all()
    )
    return permissions

def remove_permission_from_api_key(db: Session, api_key_id: int, permission_id: int) -> None:
    db.query(ApiKeyPermission).filter(
        ApiKeyPermission.api_key_id == api_key_id,
        ApiKeyPermission.permission_id == permission_id
    ).delete()
    db.commit()
