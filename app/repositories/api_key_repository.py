from sqlalchemy.orm import Session
from app.models.api_key import ApiKey

class ApiKeyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_api_key(self, api_key: ApiKey) -> ApiKey:
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        return api_key  

    def find_api_key_by_hash(self, key_hash: str) -> ApiKey | None:
        return self.db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()

    def find_api_keys_by_user_id(self, user_id: int) -> list[ApiKey]:
        return self.db.query(ApiKey).filter(ApiKey.user_id == user_id).all()

    def deactivate_api_key(self, api_key_id:int) -> None:
        self.db.query(ApiKey).filter(ApiKey.id == api_key_id).update({"active": False})
        self.db.commit()

    def find_by_id(self, api_key_id: int) -> ApiKey | None:
        return (self.db.query(ApiKey)
        .filter(ApiKey.id == api_key_id)
        .first()
    )
