from app.models.api_key import ApiKey
from pydantic import BaseModel
from datetime import datetime


class ApiKeyCreateRequest(BaseModel):
    name: str


class ApiKeyCreateResponse(BaseModel):
    id: int
    name: str
    api_key: str
    created_at: datetime


class ApiKeyResponse(BaseModel):
    id: int
    name: str
    active: bool
    created_at: datetime
    updated_at: datetime
    last_used_at: datetime | None
    expiry_date: datetime | None

    model_config = {
        "from_attributes": True
    }


class ApiKeyListResponse(BaseModel):
    api_keys: list[ApiKeyResponse]
    total: int